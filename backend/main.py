from fastapi import FastAPI, Depends
from app.dependencies.auth import verify_token
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze, user
from app.core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(user.router)
app.include_router(analyze.router, prefix="/api", dependencies=[Depends(verify_token)])