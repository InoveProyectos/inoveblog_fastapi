#!/usr/bin/env python

import os
from datetime import datetime, timedelta

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from passlib.context import CryptContext
import jwt


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = 'SECRET'
    ALGORITHM = "HS256"
    EXPIRE_MINUTES = 30

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=self.EXPIRE_MINUTES),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['sub']
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid user")
            return user_id
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)


# Create auth handler
auth_handler = AuthHandler()