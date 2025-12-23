release: flask db upgrade
web: gunicorn -w 1 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker --timeout 120 --bind 0.0.0.0:$PORT app:app
