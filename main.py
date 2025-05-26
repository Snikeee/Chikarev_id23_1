from fastapi import FastAPI, Depends, HTTPException
from app.api.endpoints import router as api_router


app = FastAPI(
    title="Image Binarization API",
    description="API для превращения изображений в черно-белые",
    version="1.0.0"
)

app.include_router(api_router)
