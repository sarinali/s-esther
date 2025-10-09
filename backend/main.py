from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import config
from routes.core import core_router
from routes.search import search_router
from services.logger_service import logger_service


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger_service.info("Starting application")
    config.validate_required_config()

    yield

    logger_service.info("Shutting down application")
    logger_service.info("Application shutdown complete")


app = FastAPI(
    title="S-Esther Backend API",
    description="Backend API for user profile search and scraping",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://s-esther.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router, prefix="/search", tags=["search"])
app.include_router(core_router, prefix="/core", tags=["core"])


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)