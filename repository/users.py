from typing import TypeVar, Generic, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from authentication.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import Depends, requests, HTTPException, status
from fastapi.security import HTTPBearer, HTTPBasicCredentials

T = TypeVar('T')

class BaseRepo():
  @staticmethod
  def insert(db: Session, model: Generic[T]):
    db.add(model)
    db.commit()
    db.refresh(model)

class UserRepo(BaseRepo):
  @staticmethod
  def find_by_username(db: Session, model: Generic[T], username: str):
    return db.query(model).filter(model.username == username).first()
  
class JWTRepo():
  @staticmethod
  def generate_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
      expire = datetime.now() + expires_delta
    else:
      expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
  def decode_token(token: str):
    try:
      decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      return decode_token if decode_token['expire'] >= datetime.time() else None
    except:
     return{}
  
 