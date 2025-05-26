from celery import Celery
import redislite

redis_instance = redislite.Redis('/tmp/redis.db')

app = Celery(
    'image_binarization',
    broker=f'redis+socket://{redis_instance.socket_file}?db=0',
    backend=f'redis+socket://{redis_instance.socket_file}?db=0',
    include=['app.tasks.binarization_tasks']
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
    task_soft_time_limit=3300,
)