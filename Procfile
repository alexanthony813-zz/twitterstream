web: python -u server.py; 
worker: celery -A tasks worker --loglevel=info; python -u consumer.py; 
