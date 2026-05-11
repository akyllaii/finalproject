from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY

pwd = CryptContext(
    schemes=["bcrypt"],
    bcrypt__rounds=12,
    deprecated="auto"
)

def hash_password(password: str):
    return pwd.hash(password[:72])

def verify(password, hashed):
    return pwd.verify(password[:72], hashed)

def create_token(data):
    payload = {
        "sub": data,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")