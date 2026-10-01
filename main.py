from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.database import Base, engine
from app.routers import auth, pages, planners


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


settings = get_settings()

app = FastAPI(
    title="PocketSmart AI",
    description="Budget-aware GenAI recommendation assistant for home, parties, and jewelry.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(planners.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "pocketsmart-ai", "ai_mode": "gemini" if settings.gemini_api_key and not settings.use_mock_ai else "fallback"}


@app.get("/startup")
def startup():
    return {"status": "initialized", "database": settings.database_url, "model": settings.gemini_model}
