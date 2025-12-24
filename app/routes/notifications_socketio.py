# SocketIO event handlers for notifications
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app.models import Notification
from datetime import datetime
from .notifications import connected_users

def register_notification_socketio(socketio):
    @socketio.on('connect')
    def handle_connect():
        if current_user.is_authenticated:
            user_room = f'user_{current_user.id}'
            join_room(user_room)
            connected_users[request.sid] = current_user.id
            unread_count = Notification.query.filter_by(
                user_id=current_user.id,
                is_read=False
            ).count()
            emit('connected', {
                'message': 'Connected to notifications',
                'unread_count': unread_count
            })
            print(f'[NOTIFICATIONS] User {current_user.username} (ID: {current_user.id}) connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        if request.sid in connected_users:
            user_id = connected_users.pop(request.sid)
            leave_room(f'user_{user_id}')
            print(f'[NOTIFICATIONS] User ID {user_id} disconnected')

    @socketio.on('mark_read')
    def handle_mark_read(data):
        if not current_user.is_authenticated:
            return False
        try:
            notification_id = data.get('notification_id')
            notification = Notification.query.get(notification_id)
            if not notification or notification.user_id != current_user.id:
                return False
            notification.is_read = True
            notification.updated_at = datetime.utcnow()
            from app import db
            db.session.commit()
            emit('notification_read', {
                'notification_id': notification_id
            }, room=f'user_{current_user.id}')
            return True
        except Exception as e:
            print(f'[NOTIFICATIONS] Error marking read: {str(e)}')
            return False

    @socketio.on('get_unread_count')
    def handle_get_unread_count():
        if not current_user.is_authenticated:
            return
        try:
            unread_count = Notification.query.filter_by(
                user_id=current_user.id,
                is_read=False
            ).count()
            emit('unread_count_update', {
                'unread_count': unread_count
            })
        except Exception as e:
            print(f'[NOTIFICATIONS] Error getting unread count: {str(e)}')
