"""
Migration script to add 'order' column to the courses table.
Run with: flask db upgrade (if using Flask-Migrate), or as a standalone script if not using Alembic.
"""
from app import create_app, db
from sqlalchemy import Column, Integer

def add_order_column():
    app = create_app()
    with app.app_context():
        # Check if column already exists
        if not hasattr(db.Model.metadata.tables['courses'].c, 'order'):
            db.engine.execute('ALTER TABLE courses ADD COLUMN order INTEGER DEFAULT 0')
            print("Added 'order' column to courses table.")
        else:
            print("'order' column already exists.")

if __name__ == "__main__":
    add_order_column()
