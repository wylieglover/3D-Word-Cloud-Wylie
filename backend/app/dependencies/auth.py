
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        return jwt.decode(token, settings.jwt_access_secret, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=403, detail="Not authorized")
    