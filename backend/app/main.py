from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.database.database import engine

from app.scheduler.reminder_scheduler import start_scheduler

from app.modules.applications.router import (
    router as application_router,
)
from app.modules.certificates.router import (
    router as certificate_router,
)
from app.modules.approvals.router import (
    router as approval_router,
)
from app.modules.notifications.router import (
    router as notification_router,
)
from app.auth.router import (
    router as auth_router,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Background Scheduler
    start_scheduler()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# Register all application routes
app.include_router(application_router)
app.include_router(certificate_router)
app.include_router(approval_router)
app.include_router(notification_router)
app.include_router(auth_router)


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