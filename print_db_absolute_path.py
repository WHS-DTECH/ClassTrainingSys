# print_db_absolute_path.py
from app import create_app
import os

def print_db_absolute_path():
    app = create_app()
    with app.app_context():
        uri = app.config['SQLALCHEMY_DATABASE_URI']
        if uri.startswith('sqlite:///'):
            rel_path = uri.replace('sqlite:///', '', 1)
            abs_path = os.path.abspath(rel_path)
            print('SQLALCHEMY_DATABASE_URI:', uri)
            print('Absolute DB path:', abs_path)
        else:
            print('Non-SQLite DB URI:', uri)

if __name__ == "__main__":
    print_db_absolute_path()
