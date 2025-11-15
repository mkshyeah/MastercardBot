import decimal
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List

from .database import connection, models
from .core import schemas # <-- Импортируем схемы
from .services import sql_builder # <-- Импортируем наш SQL-конструктор

app = FastAPI(
    title="Agentic Analyst API",
    description="API for converting natural language to SQL queries.",
    version="0.1.0"
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
        # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
        chain_result = sql_builder.run_full_chain(query_request)

        # "result" теперь будет списком словарей с одним элементом, чтобы соответствовать схеме
        response_result = [{"summary_result": chain_result["summary"]}]

        return schemas.QueryResponse(
            sql_query=chain_result["sql_query"],
            result=response_result,
            summary=chain_result["summary"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))