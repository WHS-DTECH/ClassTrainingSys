#!/usr/bin/env python
"""
Script to add code_hash column to comment_feedback table
"""
import os
import sys

# Set database URL for local SQLite
os.environ['DATABASE_URL'] = 'sqlite:///instance/app.db'

from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Check if column exists
    inspector = db.inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('comment_feedback')]
    
    if 'code_hash' not in columns:
        print("Adding code_hash column to comment_feedback table...")
        with db.engine.connect() as conn:
            # Add the column
            conn.execute(text('ALTER TABLE comment_feedback ADD COLUMN code_hash VARCHAR(64) DEFAULT "unknown"'))
            # Update existing rows
            conn.execute(text('UPDATE comment_feedback SET code_hash = "unknown" WHERE code_hash IS NULL'))
            conn.commit()
        print("✓ code_hash column added successfully")
    else:
        print("✓ code_hash column already exists")
