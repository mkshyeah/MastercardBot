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
def execute_query(query_request: schemas.QueryRequest, db: Session = Depends(get_db)):
    """
    Принимает структурированный запрос, строит SQL, выполняет его и возвращает результат.
    """
    # Шаг 1: Построить SQL-запрос (пока с помощью заглушки)
    sql_query = sql_builder.build_sql_query(query_request)

    # Шаг 2: Выполнить SQL-запрос (ЗАГЛУШКА)
    # В реальности мы бы выполнили запрос, но пока БД загружается, вернем фейковый результат.
    # try:
    #     result_proxy = db.execute(text(sql_query))
    #     column_names = result_proxy.keys()
    #     result = [dict(zip(column_names, row)) for row in result_proxy.fetchall()]
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=f"Error executing SQL query: {e}")

    # Фейковый результат для тестирования
    result = [
        {"metric": "some_value", "group": "group_a"},
        {"metric": "another_value", "group": "group_b"}
    ]

    # Шаг 3: Сгенерировать текстовый саммари (пока заглушка)
    summary = f"Successfully executed query for: '{query_request.user_query}'"

    return schemas.QueryResponse(
        sql_query=sql_query,
        result=result,
        summary=summary
    )