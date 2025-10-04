from fastapi import FastAPI
from contextlib import asynccontextmanager

from routes.search import search_router
from services.browser_service import service as browser_service
from services.logger_service import logger_service


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger_service.info("Starting application")

    try:
        browser_service.initialize()
        logger_service.info("Browser service initialized successfully")
    except Exception as e:
        logger_service.error(f"Failed to initialize browser service: {e}")
        raise

    yield

    logger_service.info("Shutting down application")
    browser_service.shutdown()
    logger_service.info("Application shutdown complete")


app = FastAPI(
    title="S-Esther Backend API",
    description="Backend API for user profile search and scraping",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(search_router, prefix="/search", tags=["search"])


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "browser_initialized": browser_service.is_initialized,
        "browser_logged_in": browser_service.is_logged_in
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)