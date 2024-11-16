from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config import CONFIG
import jwt
import uuid
import logging

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return passwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_data: dict, expires_delta: timedelta = None, refresh: bool = False
) -> str:
    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expires_delta
        if expires_delta is not None
        else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, key=CONFIG.JWT_SECRET_KEY, algorithm=CONFIG.JWT_ALGORITHM
    )

    return token


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            jwt=token, key=CONFIG.JWT_SECRET_KEY, algorithms=[CONFIG.JWT_ALGORITHM]
        )
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
