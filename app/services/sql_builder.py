import json
import ast
from decimal import Decimal
import time # Добавьте этот импорт

# --- 1. ДОБАВЬ ЭТИ ИМПОРТЫ ---
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from app.database.connection import engine
# -----------------------------

# --- 1. УДАЛИ ЭТОТ ИМПОРТ, ОН БОЛЬШЕ НЕ НУЖЕН ---
# from langchain_core.prompts import PromptTemplate

from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
from langchain_experimental.sql import SQLDatabaseChain

from app.core.config import DATABASE_URL, OPENAI_API_KEY
from app.core.schemas import QueryRequest

# Инициализируем подключение к БД
db = SQLDatabase.from_uri(DATABASE_URL)

# Инициализируем LLM
llm = OpenAI(temperature=0, verbose=True, openai_api_key=OPENAI_API_KEY)

# --- 2. УДАЛИ `ANSWER_PROMPT` ---

# --- 3. УБЕРИ `prompt=ANSWER_PROMPT` ОТСЮДА ---
db_chain = SQLDatabaseChain.from_llm(
    llm,
    db,
    verbose=True,
    use_query_checker=True,
    return_intermediate_steps=True
)

# --- 4. ЗАМЕНИ ФУНКЦИЮ `run_full_chain` ---
def run_full_chain(query_request: QueryRequest) -> dict:
    start_time = time.time()
    print(f"\n[TIMING] --- Chain started ---")

    # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
    # Добавляем инструкцию прямо в конец вопроса пользователя
    enhanced_user_question = (
        f"{query_request.user_query}\n\n"
        "IMPORTANT: Your final answer MUST be in the same language as the original user question above."
    )
    
    # --- 2. ДОБАВЛЯЕМ ОБРАБОТКУ ОШИБОК ---
    try:
        chain_invoke_start = time.time()
        print("[TIMING] Calling LangChain/OpenAI...")
        chain_response = db_chain.invoke(enhanced_user_question)
        chain_invoke_end = time.time()
        print(f"[TIMING] LangChain/OpenAI call took: {chain_invoke_end - chain_invoke_start:.2f} seconds")
    except ProgrammingError as e:
        # Если LangChain сгенерировал невалидный SQL, ловим ошибку здесь
        return {
            "sql_query": "Invalid SQL generated",
            "result": [],
            "summary": f"Не удалось выполнить запрос. Возможно, он слишком сложный или неоднозначный. Попробуйте переформулировать. (Ошибка: {e.orig.msg})"
        }
    except Exception as e:
        # Ловим все остальные возможные ошибки (например, от OpenAI)
        return {
            "sql_query": "Error before SQL generation",
            "result": [],
            "summary": f"Произошла непредвиденная ошибка: {str(e)}"
        }
    # ------------------------------------


    sql_query = "SQL query not found."
    raw_result = []

    # Шаг 1: Извлекаем SQL-запрос из ответа LangChain
    if chain_response.get('intermediate_steps'):
        for step in chain_response['intermediate_steps']:
            if isinstance(step, dict) and 'sql_cmd' in step:
                sql_query = step['sql_cmd']
                break

    # Шаг 2: Если SQL-запрос найден, выполняем его еще раз, чтобы получить чистый результат
    if sql_query != "SQL query not found.":
        # Убедимся, что это только SELECT-запрос для безопасности
        if "SELECT" in sql_query.upper():
            try:
                db_exec_start = time.time()
                print("[TIMING] Re-executing SQL query against local DB...")
                Session = sessionmaker(bind=engine)
                with Session() as session:
                    result_proxy = session.execute(text(sql_query))
                    column_names = result_proxy.keys()
                    
                    # Собираем результат в виде списка словарей
                    raw_result = [
                        {key: (float(value) if isinstance(value, Decimal) else value) for key, value in zip(column_names, row)}
                        for row in result_proxy.fetchall()
                    ]
                db_exec_end = time.time()
                print(f"[TIMING] Local DB execution took: {db_exec_end - db_exec_start:.2f} seconds")
            except Exception as e:
                raw_result = [{"error": f"Failed to re-execute SQL: {str(e)}"}]

    total_end_time = time.time()
    print(f"[TIMING] Total chain execution took: {total_end_time - start_time:.2f} seconds")
    print("[TIMING] --- Chain finished ---\n")
    return {
        "sql_query": sql_query.replace('\n', ' ').strip(),
        "result": raw_result,
        "summary": str(chain_response.get('result', 'No summary generated.')).strip()
    }