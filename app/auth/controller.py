#!/usr/bin/env python
from fastapi import Depends, Response, HTTPException
from pydantic import BaseModel

from .models import AuthUser

from sqlalchemy.orm import Session
from back.database import get_database

from .AuthHandler import auth_handler

class AuthDetails(BaseModel):
    username: str
    password: str


class RegisterAuthDetails(BaseModel):
    username: str
    password: str


async def login(auth_details: AuthDetails, db: Session = Depends(get_database)):
    
    if (auth_user_data is None) or (not auth_handler.verify_password(auth_details.password, auth_user_data.password)):
        raise HTTPException(status_code=401, detail="Invalid username and/or password")

    token = auth_handler.encode_token(auth_user_data.id)
    return {"token": token, "token_type": "bearer"}

    