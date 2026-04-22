
from fastapi import Depends, Cookie, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        return jwt.decode(token, settings.jwt_access_secret, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=403, detail="Not authorized")

def verify_refresh_token(refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(401, detail="No refresh token")
    try:
        payload = jwt.decode(refresh_token, settings.jwt_refresh_secret, algorithms=["HS256"])
        return {"token": refresh_token, "sub": payload["sub"]}
    except JWTError:
        raise HTTPException(401, detail="Invalid refresh token")