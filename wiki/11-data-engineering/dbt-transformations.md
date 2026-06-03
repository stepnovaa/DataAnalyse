# dbt — трансформации как код

## Что такое dbt

**Data Build Tool** — инструмент для трансформации данных в хранилище. Пишешь SQL SELECT'ы, dbt собирает из них таблицы и представления. Весь код — в git.

## Философия

> «Analytics Engineering» — аналитик, который работает как инженер: код, git, тесты, CI/CD.

## Как работает dbt

```
Сырые данные (sources.yml)
    ↓
Staging модели (stg_*.sql) — минимальная очистка
    ↓
Intermediate модели (int_*.sql) — объединения
    ↓
Mart модели (dim_*, fct_*) — готовые таблицы для BI
```

## Базовая модель

```sql
-- models/marts/fct_orders.sql
{{
    config(materialized='table')
}}

SELECT
    order_id,
    customer_id,
    order_date,
    amount,
    status
FROM {{ ref('stg_orders') }}
WHERE status != 'cancelled'
```

- `{{ ref('name') }}` — ссылка на другую модель (dbt сам выстроит порядок выполнения)
- `{{ config(...) }}` — настройки материализации

## Материализация

| Тип | Что |
|-----|-----|
| **view** | Представление. Всегда актуально, но медленно |
| **table** | Физическая таблица. Быстро, но надо перестраивать |
| **incremental** | Только новые данные. Для больших таблиц |
| **ephemeral** | Как CTE, не материализуется |

```sql
-- Инкрементальная модель
{{ config(materialized='incremental', unique_key='order_id') }}

SELECT * FROM {{ source('raw', 'orders') }}
{% if is_incremental() %}
WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
```

## Тесты

```yaml
# models/schema.yml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: amount
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
      - name: status
        tests:
          - accepted_values:
              values: ['new', 'processed', 'shipped']
```

Запуск: `dbt test` — проверяет все тесты.

## Документация

```yaml
models:
  - name: fct_orders
    description: 'Заказы с суммой и статусом. Одна строка = один заказ.'
    columns:
      - name: order_id
        description: 'Первичный ключ заказа'
```

`dbt docs generate` → интерактивная документация с lineage.

## Jinja и макросы

dbt использует Jinja для динамического SQL:

```sql
-- Макрос
{% macro percent_of_total(column) %}
    {{ column }} * 100.0 / SUM({{ column }}) OVER ()
{% endmacro %}

-- Использование
SELECT category, revenue, {{ percent_of_total('revenue') }} AS pct
```

## dbt + CI/CD

См. [[../11-data-engineering/ci-cd-for-data|CI/CD для данных]].

## Связанные страницы

- [[../11-data-engineering/data-warehouse-architecture|Архитектура хранилищ]]
- [[../06-data-processing/data-quality-and-testing|Качество данных]]
- [[../06-data-processing/etl-vs-elt|ETL vs ELT]]
