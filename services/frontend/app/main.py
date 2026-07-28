import os
from fastapi import FastAPI
from app.routers import health, pages

app = FastAPI(
    title="Platform Frontend",
    version="1.0.0",
    description="Frontend service for Platform Stack P3",
)

app.include_router(health.router)
app.include_router(pages.router)


@app.get("/info")
def info():
    return {
        "service": "frontend",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "local"),
        "api_url": os.getenv("API_URL", "http://api:8000"),
    }
