import decimal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List, Optional, Any

from .database import connection, models
from .core import schemas # <-- Импортируем схемы
from .services import sql_builder # <-- Импортируем наш SQL-конструктор

app = FastAPI(
    title="Agentic Analyst API",
    description="API for converting natural language to SQL queries.",
    version="0.1.0"
)

# Настройка CORS
origins = [
    "http://localhost",
    "http://localhost:5173",  # Адрес фронтенда Vite
    "http://localhost:3000",  # Адрес фронтенда (если Create React App)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Функция для получения сессии БД
def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health", status_code=200, tags=["Health Check"])
def health_check():
    """
    Checks if the API is running.
    """
    return {"status": "ok"}

@app.post("/query", response_model=schemas.QueryResponse, tags=["Query"])
def execute_query(query_request: schemas.QueryRequest):
    """
    Принимает текстовый запрос, запускает LangChain-цепочку и возвращает результат.
    """
    try:
        chain_result = sql_builder.run_full_chain(query_request)

        return schemas.QueryResponse(
            sql_query=chain_result["sql_query"],
            result=chain_result["result"],
            summary=chain_result["summary"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))