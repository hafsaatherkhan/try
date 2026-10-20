import os

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import NullPool

app = FastAPI(title="Vercel Deployment Spike")


@app.get("/health")
def health():
    return {"status": "ok", "service": "fastapi"}


@app.get("/health/db")
def database_health():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise HTTPException(
            status_code=503,
            detail="Database configuration missing",
        )

    try:
        engine = create_engine(database_url, poolclass=NullPool)
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return {"status": "ok", "database": "connected"}
        finally:
            engine.dispose()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        )