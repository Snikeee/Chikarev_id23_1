from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.db import get_db
from app.models import User
from app.cruds import create_user, get_user_by_email, verify_password, create_access_token
from sqlalchemy.orm import Session
from io import BytesIO
from PIL import Image
import base64
from datetime import timedelta
from app.dependencies import get_current_user
from app.tasks.binarization_tasks import binarize_image_task
from celery.result import AsyncResult

router = APIRouter()

class ImageRequest(BaseModel):
    image: str
    algorithm: str

class ImageResponse(BaseModel):
    task_id: str

class TaskStatus(BaseModel):
    task_id: str
    status: str
    progress: float = None
    binarized_image: str = None
    error: str = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    token: str

    class Config:
        from_attributes = True

class UserInfo(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

@router.post("/binary_image", response_model=ImageResponse)
async def binary_image(request: ImageRequest, current_user: User = Depends(get_current_user)):
    try:
        # Постановка задачи на бинаризацию в очередь
        task = binarize_image_task.delay(request.image, request.algorithm)
        return {"task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/task/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str, current_user: User = Depends(get_current_user)):
    task_result = AsyncResult(task_id)
    response = {"task_id": task_id, "status": task_result.state}

    if task_result.state == "PROGRESS":
        response["progress"] = task_result.info.get("progress", 0)
    elif task_result.state == "SUCCESS":
        response.update(task_result.get())
    elif task_result.state == "FAILURE":
        response["error"] = task_result.info.get("error", "Неизвестная ошибка")

    return response

@router.post("/sign-up/", response_model=UserResponse)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    new_user = create_user(db, user.email, user.password)
    token = create_access_token({"sub": new_user.email}, expires_delta=timedelta(minutes=30))
    return {"id": new_user.id, "email": new_user.email, "token": token}

@router.post("/login/", response_model=UserResponse)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    token = create_access_token({"sub": db_user.email}, expires_delta=timedelta(minutes=30))
    return {"id": db_user.id, "email": db_user.email, "token": token}

@router.get("/users/me/", response_model=UserInfo)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}