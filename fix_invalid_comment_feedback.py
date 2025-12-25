# Script to find and fix invalid comment_feedback section references
# Removes comment_feedback records with section_id not present in sections table

from app import create_app, db
from app.models import CommentFeedback, Section

app = create_app()

with app.app_context():
    valid_section_ids = {s.id for s in Section.query.all()}
    invalid_feedbacks = CommentFeedback.query.filter(~CommentFeedback.section_id.in_(valid_section_ids)).all()
    if invalid_feedbacks:
        print(f"Found {len(invalid_feedbacks)} invalid comment_feedback records. Deleting...")
        for feedback in invalid_feedbacks:
            db.session.delete(feedback)
        db.session.commit()
        print("Invalid comment_feedback records removed.")
    else:
        print("No invalid comment_feedback records found.")
