release: flask db upgrade
web: gunicorn -w 1 --threads 4 --worker-tmp-dir /dev/shm --timeout 120 --bind 0.0.0.0:$PORT app:app
