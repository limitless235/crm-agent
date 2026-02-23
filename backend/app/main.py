from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://crm-productivity-agent.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

from app.core.middleware import rate_limit_middleware
@app.middleware("http")
async def add_rate_limit(request, call_next):
    return await rate_limit_middleware(request, call_next)

@app.get("/")
def read_root():
    return {"message": "AntiGravity AI Support API is running"}
