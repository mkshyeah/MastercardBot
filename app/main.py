from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import connection, models

app = FastAPI(
    title="Agentic Analyst API",
    description="API for converting natural language to SQL queries.",
    version="0.1.0"
)

# Create DB tables on startup if they don't exist
models.Base.metadata.create_all(bind=connection.engine)

@app.get("/health", status_code=200, tags=["Health Check"])
def health_check():
    """
    Checks if the API is running.
    """
    return {"status": "ok"}