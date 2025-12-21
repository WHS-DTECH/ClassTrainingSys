# print_db_path.py
from app import create_app
from flask_sqlalchemy import SQLAlchemy

def print_db_uri():
    app = create_app()
    with app.app_context():
        print('SQLALCHEMY_DATABASE_URI:', app.config['SQLALCHEMY_DATABASE_URI'])

if __name__ == "__main__":
    print_db_uri()
