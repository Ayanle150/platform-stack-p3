import os
from fastapi import FastAPI
from app.routers import health, items

app = FastAPI(
    title="Platform API",
    version="1.0.0",
    description="Backend API service for Platform Stack P3",
)

app.include_router(health.router)
app.include_router(items.router)


@app.get("/")
def root():
    return {
        "service": "api",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "local"),
    }
