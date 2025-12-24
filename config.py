import os
from sqlalchemy.pool import NullPool

class Config:
    DEBUG = True  # TEMP: Enable debug for /admin/export-db route
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database URL with SSL configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_F47xzVPyGQCb@ep-old-sea-a7k7s3p8-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
    # Ensure SSL mode is set for PostgreSQL
    if SQLALCHEMY_DATABASE_URI.startswith('postgresql') and 'sslmode=' not in SQLALCHEMY_DATABASE_URI:
        if '?' in SQLALCHEMY_DATABASE_URI:
            SQLALCHEMY_DATABASE_URI += '&sslmode=require'
        else:
            SQLALCHEMY_DATABASE_URI += '?sslmode=require'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Determine if we're on Render (production) or local
    IS_RENDER = os.environ.get('RENDER') == 'true'
    
    if IS_RENDER:
        # On Render: Use NullPool to avoid connection pooling issues
        # Each request gets a fresh connection, avoiding stale connection timeouts
        SQLALCHEMY_ENGINE_OPTIONS = {
            'poolclass': NullPool,  # Disable connection pooling
            'connect_args': {
                'connect_timeout': 10,
                'keepalives': 1,
                'keepalives_idle': 20,
                'keepalives_interval': 5,
                'keepalives_count': 3
            }
        }
    else:
        # Local development: Use standard connection pooling
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
