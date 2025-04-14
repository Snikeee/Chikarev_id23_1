from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(
    title="Image Binarization API",
    description="API для превращения изображений в черно-белые",
    version="1.0.0"
)

app.include_router(endpoints.router)