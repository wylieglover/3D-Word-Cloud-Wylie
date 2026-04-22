from fastapi import Request, FastAPI, Depends
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.dependencies.auth import verify_token
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze, auth
from app.core.config import settings
from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

app.include_router(auth.router, prefix="/api")
app.include_router(analyze.router, prefix="/api", dependencies=[Depends(verify_token)])