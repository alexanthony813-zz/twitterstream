web: python server.py; 
worker: celery -A tasks worker --loglevel=info; 
consume: python consumer.py;
queue: python tasks.py;
