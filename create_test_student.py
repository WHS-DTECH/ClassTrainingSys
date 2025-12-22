#!/usr/bin/env python
"""
Script to add a test student user for testing
"""
import os
import sys

os.environ['DATABASE_URL'] = 'sqlite:///instance/app.db'

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Check if student already exists
    student = User.query.filter_by(username='student1').first()
    
    if not student:
        print("Creating test student user...")
        student = User(
            username='student1',
            email='student1@example.com',
            first_name='Test',
            last_name='Student',
            role='student'
        )
        student.set_password('password123')
        db.session.add(student)
        db.session.commit()
        print(f"✓ Student user created: student1 / password123")
    else:
        print(f"✓ Student user already exists: student1")
        # Reset password just in case
        student.set_password('password123')
        db.session.commit()
        print(f"  Password reset to: password123")
