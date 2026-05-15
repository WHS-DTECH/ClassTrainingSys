import os
from sqlalchemy.pool import NullPool

class Config:
    DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database URL with SSL configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///instance/app.db')
    # Ensure SSL mode is set for PostgreSQL
    if SQLALCHEMY_DATABASE_URI.startswith('postgresql') and 'sslmode=' not in SQLALCHEMY_DATABASE_URI:
        if '?' in SQLALCHEMY_DATABASE_URI:
            SQLALCHEMY_DATABASE_URI += '&sslmode=require'
        else:
            SQLALCHEMY_DATABASE_URI += '?sslmode=require'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Determine if we're on Render (production) or local
    IS_RENDER = os.environ.get('RENDER') == 'true'

    # OAuth and session hardening
    GOOGLE_OAUTH_ALLOWED_DOMAINS = [
        domain.strip().lower()
        for domain in os.environ.get('GOOGLE_OAUTH_ALLOWED_DOMAINS', '').split(',')
        if domain.strip()
    ]
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', '1' if IS_RENDER else '0') == '1'
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE
    
    if SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
        # SQLite does not support PostgreSQL-specific connect args.
        SQLALCHEMY_ENGINE_OPTIONS = {}
    elif IS_RENDER:
        # On Render: Use NullPool to avoid connection pooling issues.
        SQLALCHEMY_ENGINE_OPTIONS = {
            'poolclass': NullPool,
            'connect_args': {
                'connect_timeout': 10,
                'keepalives': 1,
                'keepalives_idle': 20,
                'keepalives_interval': 5,
                'keepalives_count': 3
            }
        }
    else:
        # Local development with PostgreSQL: standard pooling.
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': 5,
            'pool_recycle': 1800,
            'pool_pre_ping': True,
            'max_overflow': 10,
            'connect_args': {
                'connect_timeout': 10,
                'keepalives': 1,
                'keepalives_idle': 30,
                'keepalives_interval': 10,
                'keepalives_count': 5
            }
        }

    # File Uploads
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # Pagination
    ITEMS_PER_PAGE = 20

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
