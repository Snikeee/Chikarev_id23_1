from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from app.services.binarization import binarize_image
from app.db import get_db
from app.models import User
from app.cruds import create_user, get_user_by_email, verify_password, create_access_token
from sqlalchemy.orm import Session
from io import BytesIO
from PIL import Image
import base64
from datetime import timedelta
from app.dependencies import get_current_user

router = APIRouter()


class ImageRequest(BaseModel):
    image: str
    algorithm: str


class ImageResponse(BaseModel):
    binarized_image: str


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
async def binary_image(request: ImageRequest):
    try:
        image_data = base64.b64decode(request.image)
        image = Image.open(BytesIO(image_data))
        binarized = binarize_image(image, request.algorithm)
        buffered = BytesIO()
        binarized.save(buffered, format="PNG")
        binarized_base64 = base64.b64encode(buffered.getvalue()).decode()
        return {"binarized_image": binarized_base64}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sign-up/", response_model=UserResponse)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user.email, user.password)
    token = create_access_token({"sub": new_user.email}, expires_delta=timedelta(minutes=30))
    return {"id": new_user.id, "email": new_user.email, "token": token}


@router.post("/login/", response_model=UserResponse)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": db_user.email}, expires_delta=timedelta(minutes=30))
    return {"id": db_user.id, "email": db_user.email, "token": token}


@router.get("/users/me/", response_model=UserInfo)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}
