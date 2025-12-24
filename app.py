
from app import create_app, socketio

app = create_app()

# Register SocketIO event handlers only in web context
from app.routes.notifications_socketio import register_notification_socketio
register_notification_socketio(socketio)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)

