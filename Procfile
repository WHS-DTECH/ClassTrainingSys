
release: flask db upgrade
web: gunicorn -k eventlet -w 1 --worker-tmp-dir /dev/shm --timeout 120 --bind 0.0.0.0:$PORT app:app
