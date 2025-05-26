from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.db import get_db
from app.cruds import get_user_by_email
from app.models import User
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(f"Token: {token}")  # Отладочный вывод
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"Payload: {payload}")  # Отладочный вывод
        email: str = payload.get("sub")
        if email is None:
            print("No email in token")  # Отладочный вывод
            raise credentials_exception
    except JWTError as e:
        print(f"JWT Error: {str(e)}")  # Отладочный вывод
        raise credentials_exception

    user = get_user_by_email(db, email)
    if user is None:
        print(f"User not found for email: {email}")  # Отладочный вывод
        raise credentials_exception
    return user
