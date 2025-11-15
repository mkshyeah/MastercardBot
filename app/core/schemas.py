from pydantic import BaseModel
from typing import List, Optional, Any

# --- Схемы для фильтров ---
class Filter(BaseModel):
    field: str
    operator: str
    value: Any

# --- Схема для входящего запроса от NLP-модуля ---
class QueryRequest(BaseModel):
    metrics: List[str]
    group_by: Optional[List[str]] = None
    filters: Optional[List[Filter]] = None
    limit: Optional[int] = None
    user_query: str

# --- Схема для ответа от API ---
class QueryResponse(BaseModel):
    sql_query: str
    result: List[dict]
    summary: str

