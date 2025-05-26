uvicorn main:app --reload
celery -A app.tasks.celery_config worker --loglevel=info
для запуска
