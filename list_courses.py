import os
from app import create_app, db
from app.models import Course

app = create_app()

def list_courses():
    with app.app_context():
        courses = Course.query.all()
        for course in courses:
            print(f"ID: {course.id} | Title: {course.title}")

if __name__ == "__main__":
    list_courses()
