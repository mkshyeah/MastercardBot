# Test Cases for Agentic Analyst Chatbot

This document contains a list of natural language queries to test the functionality of the chatbot.

---

## 1. Basic Metrics (Простые метрики)

*   `Total number of transactions in Q1 2024`
*   `What was the total revenue in KZT last year?`
*   `Show me the average check for all transactions`
*   `Calculate the overall decline rate` *(Note: uses synthetic data)*

---

## 2. Queries with Filters (Запросы с фильтрами)

*   `Total revenue in KZT for S1lk Pay in 2024`
*   `Number of transactions in Kazakhstan for October 2025`
*   `What is the average check in Almaty for mcc_category 'retail'?`
*   `Show all transactions for Nomad Market last week`
*   `Decline rate for transactions made with Apple Pay` *(Note: uses synthetic data)*

---

## 3. Queries with Grouping (Запросы с группировкой)

*   `Top 5 merchants by revenue in 2024`
*   `Show revenue by mcc_category`
*   `List the top 10 cities by number of transactions`
*   `Monthly revenue for 2025`
*   `What are the top 3 countries by total transaction amount?`

---

## 4. Ambiguous Queries (Неполные запросы для проверки уточнений)

*   `Show me revenue for S1lk Pay` -> (Bot should ask for a time period)
*   `Total transactions` -> (Bot should ask for a time period)
*   `Decline rate in Kazakhstan` -> (Bot should ask for a time period)

---

## 5. Complex Queries (Комбинированные запросы)

*   `Top 5 merchants by revenue in Kazakhstan for 2024`
*   `What was the monthly decline rate for S1lk Pay in Q1 2025?` *(Note: uses synthetic data)*
*   `Show me the average check by mcc_category in Almaty for the last month`

---

## 6. Multilingual Queries (Многоязычные запросы)

*   (RU) `Какая выручка у S1lk Pay за последний квартал?`
*   (RU) `Топ 5 мерчантов по количеству транзакций в Казахстане`
*   (KZ) `S1lk Pay үшін соңғы тоқсандағы кіріс қандай?` (Пример)