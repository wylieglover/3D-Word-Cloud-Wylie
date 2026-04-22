from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from sqlalchemy import select
from app.schemas.auth import AuthRequest, AuthResponse
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models.auth import User, Session
from app.dependencies.auth import verify_refresh_token
from datetime import datetime, timedelta, timezone
from app.core.config import settings

router = APIRouter(prefix="/auth")

@router.post("/register", response_model=AuthResponse)
async def register(request: AuthRequest, response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(409, detail="Email already registered")
    
    hashed_password = hash_password(request.password)
    user_model = User(email=request.email, password=hashed_password)
    db.add(user_model)
    await db.commit()
    await db.refresh(user_model)

    access_token = create_access_token(str(user_model.id))
    refresh_token = create_refresh_token(str(user_model.id))

    session = Session(
        user_id=user_model.id,
        refresh_token=refresh_token,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_refresh_expire_minutes)
    )
    db.add(session)
    await db.commit()

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.environment == "production",
        samesite="strict",
        max_age=settings.jwt_refresh_expire_minutes * 60
    )

    return AuthResponse(email=user_model.email, access_token=access_token)

@router.post("/login", response_model=AuthResponse)
async def login(request: AuthRequest, response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(401, detail="Invalid credentials")
    
    if not verify_password(request.password, user.password):
        raise HTTPException(401, detail="Invalid credentials")
    
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    session = Session(
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_refresh_expire_minutes)
    )
    db.add(session)
    await db.commit()

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.environment == "production",
        samesite="strict",
        max_age=settings.jwt_refresh_expire_minutes * 60
    )

    return AuthResponse(email=user.email, access_token=access_token)

@router.post("/refresh")
async def refresh(response: Response, db: AsyncSession = Depends(get_db), payload: dict = Depends(verify_refresh_token)):
    result = await db.execute(select(Session).where(Session.refresh_token == payload["token"]))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(401, detail="Invalid session")
    
    if session.expires_at < datetime.now(timezone.utc):
        raise HTTPException(401, detail="Session expired")

    access_token = create_access_token(str(session.user_id))
    return {"access_token": access_token}

@router.post("/logout")
async def logout(response: Response, db: AsyncSession = Depends(get_db), payload: dict = Depends(verify_refresh_token)):
    result = await db.execute(select(Session).where(Session.refresh_token == payload["token"]))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(401, detail="Invalid session")

    await db.delete(session)
    await db.commit()

    response.delete_cookie("refresh_token")
    return {"detail": "Logged out"}