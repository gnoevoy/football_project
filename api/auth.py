from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import text
from dotenv import load_dotenv
from pathlib import Path
import sys
import os

PROJECT_DIR = Path(__file__).parent.parent
sys.path.append(str(PROJECT_DIR))

from utils.connections import engine

load_dotenv(".credentials")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
secret_key = os.getenv("SECRET_KEY")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_name: str


class User(BaseModel):
    user_id: int
    user_name: str
    disabled: bool


class UserInDB(User):
    hashed_password: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_data_from_db(user_name):
    with engine.connect() as conn:
        user = conn.execute(text("SELECT * FROM users WHERE user_name = :user_name"), {"user_name": user_name})
        data = user.mappings().all()
    return data[0] if data else None


def get_user_data(user_data):
    if user_data:
        return UserInDB(**user_data)


def authenticate_user(user_name, password):
    data = get_user_data_from_db(user_name)
    user = get_user_data(data)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        token_user_name = payload.get("sub")
        if token_user_name is None:
            raise credential_exception

        token_data = TokenData(user_name=token_user_name)
    except JWTError:
        raise credential_exception

    data = get_user_data_from_db(token_data.user_name)
    user = get_user_data(data)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


def generate_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.user_name}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
