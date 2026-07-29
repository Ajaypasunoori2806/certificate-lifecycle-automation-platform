from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.database.database import engine
from app.modules.applications.router import router as application_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# Register all application routes
app.include_router(application_router)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/health/database")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "connected",
            "database": settings.DB_NAME,
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
        }