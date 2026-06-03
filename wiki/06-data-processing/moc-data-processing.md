# Обработка данных

> **Map of Content.** Данные редко приходят чистыми. Этот раздел — о том, как превратить сырьё в рабочий материал для анализа.

## Страницы раздела

- [[06-data-processing/etl-vs-elt|ETL vs ELT]] — эволюция парадигм, инструменты, когда что
- [[06-data-processing/data-cleaning|Очистка данных]] — пропуски, дубликаты, выбросы, валидация, стандартизация
- [[06-data-processing/data-wrangling-python|Data Wrangling — Python]] — pandas: filter, transform, merge, pivot, melt
- [[06-data-processing/polars-modern-dataframes|Polars — современные датафреймы]] — ленивые вычисления, преимущества над pandas
- [[06-data-processing/data-pipelines-orchestration|Оркестрация пайплайнов]] — Airflow, Prefect, Dagster
- [[06-data-processing/data-quality-and-testing|Качество данных и тестирование]] — Great Expectations, dbt tests, мониторинг
- [[06-data-processing/working-with-apis|Работа с API]] — REST, GraphQL, аутентификация, пагинация, rate limits

## Ключевые вопросы

- Сколько времени аналитик реально тратит на очистку данных? (Спойлер: 60-80%)
- Polars vs Pandas: когда пора мигрировать?
- Как автоматизировать проверки качества, чтобы спать спокойно?
