from app.core.schemas import QueryRequest

def build_sql_query(query_request: QueryRequest) -> str:
    """
    ЭТО ЗАГЛУШКА!
    В будущем здесь будет вызов LangChain.
    Пока что она просто генерирует примерный SQL для демонстрации.
    """
    metrics = ", ".join(query_request.metrics)
    
    # --- ИЗМЕНЕНИЕ: Инициализируем переменные здесь ---
    group_by_clause = ""
    limit_clause = ""
    where_clause = ""

    if query_request.group_by:
        group_by_clause = "GROUP BY " + ", ".join(query_request.group_by)
    
    if query_request.limit:
        limit_clause = f"LIMIT {query_request.limit}"
        
    # Очень упрощенная логика фильтров для примера
    if query_request.filters:
        filter_parts = []
        for f in query_request.filters:
            # В реальности здесь будет сложная обработка
            if isinstance(f.value, str):
                filter_parts.append(f"{f.field} {f.operator} '{f.value}'")
            else:
                filter_parts.append(f"{f.field} {f.operator} {f.value}")
        if filter_parts:
            where_clause = "WHERE " + " AND ".join(filter_parts)

    # Собираем все вместе
    sql_query = f"""
    SELECT {metrics}
    FROM transactions t
    LEFT JOIN merchants m ON t.merchant_id = m.id
    {where_clause}
    {group_by_clause}
    {limit_clause};
    """.strip()
    
    return sql_query