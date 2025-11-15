from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
from langchain_experimental.sql import SQLDatabaseChain # <-- ВАШ ПРАВИЛЬНЫЙ ИМПОРТ

from app.core.config import DATABASE_URL, OPENAI_API_KEY
from app.core.schemas import QueryRequest

# Инициализируем подключение к БД
db = SQLDatabase.from_uri(DATABASE_URL)

# Инициализируем LLM
llm = OpenAI(temperature=0, verbose=True, openai_api_key=OPENAI_API_KEY)

# Создаем цепочку, которая будет делать ВСЮ работу
db_chain = SQLDatabaseChain.from_llm(
    llm,
    db,
    verbose=True,
    use_query_checker=True,
    return_intermediate_steps=True
)

def run_full_chain(query_request: QueryRequest) -> dict:
    user_question = query_request.user_query
    result = db_chain.invoke(user_question)

    sql_query = "SQL query not found."
    # Проходим по всем промежуточным шагам
    if result.get('intermediate_steps'):
        for step in result['intermediate_steps']:
            # Ищем шаг, который является словарем и содержит ключ 'sql_cmd'
            if isinstance(step, dict) and 'sql_cmd' in step:
                sql_query = step['sql_cmd']
                break # Нашли, выходим из цикла

    # Формируем красивый и чистый ответ
    return {
        "sql_query": sql_query.replace('\n', ' ').strip(),
        "summary": str(result.get('result', 'No summary generated.')).strip()
    }