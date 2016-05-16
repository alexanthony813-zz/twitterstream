web: python server.py; 
worker: celery -A tasks worker --loglevel=info; 
consume: python clock.py
queue: python tasks.py
