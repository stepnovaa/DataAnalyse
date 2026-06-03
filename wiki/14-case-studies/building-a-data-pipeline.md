# Кейс: Построение дата-пайплайна

## Бизнес-контекст

Нужно построить пайплайн: сырые данные из API → витрина в DWH → дашборд. Данные обновляются ежедневно.

## Архитектура

```
Google Sheets API → Python ETL → BigQuery (staging) → dbt → BigQuery (marts) → Metabase
                         ↑                              ↑
                    Airflow DAG                   dbt Cloud job
```

## Этап 1: Extract (Python + API)

```python
# extract_sales.py
import requests
import pandas as pd
from google.oauth2 import service_account
import pandas_gbq

def extract_from_api(date):
    resp = requests.get(
        'https://api.example.com/v1/sales',
        params={'date': date, 'limit': 1000},
        headers={'Authorization': f'Bearer {API_KEY}'}
    )
    resp.raise_for_status()
    return pd.DataFrame(resp.json()['data'])
```

## Этап 2: Load (сырые данные в BigQuery)

```python
def load_to_bigquery(df, table_name):
    pandas_gbq.to_gbq(
        df, f'raw.{table_name}',
        project_id='my-project',
        if_exists='append'
    )

# Airflow DAG
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

with DAG('sales_pipeline', schedule_interval='@daily',
         start_date=datetime(2024, 1, 1), catchup=False):

    extract_load = PythonOperator(
        task_id='extract_load',
        python_callable=lambda: load_to_bigquery(
            extract_from_api('{{ ds }}'),
            'sales_raw'
        )
    )
```

## Этап 3: Transform (dbt)

```sql
-- models/staging/stg_sales.sql
WITH source AS (
    SELECT * FROM {{ source('raw', 'sales_raw') }}
),
cleaned AS (
    SELECT
        id AS sale_id,
        customer_id,
        product_id,
        CAST(amount AS NUMERIC) AS amount,
        CAST(created_at AS TIMESTAMP) AS sale_timestamp,
        DATE(created_at) AS sale_date,
        status
    FROM source
    WHERE amount > 0
      AND customer_id IS NOT NULL
)
SELECT * FROM cleaned;

-- models/marts/fct_daily_sales.sql
{{
    config(materialized='table')
}}
SELECT
    sale_date,
    product_id,
    COUNT(*) AS total_sales,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_order_value,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM {{ ref('stg_sales') }}
GROUP BY sale_date, product_id;
```

### schema.yml (тесты)

```yaml
models:
  - name: stg_sales
    columns:
      - name: sale_id
        tests: [unique, not_null]
      - name: amount
        tests: [not_null]
      - name: customer_id
        tests: [not_null, relationships: {to: ref('stg_customers'), field: 'customer_id'}]

  - name: fct_daily_sales
    columns:
      - name: total_revenue
        tests:
          - dbt_utils.accepted_range: {min_value: 0}
```

## Этап 4: Дашборд (Metabase)

1. Подключаем Metabase к BigQuery
2. Создаём вопрос: `SELECT * FROM marts.fct_daily_sales WHERE sale_date >= today - 30`
3. Строим:
   - Line chart: revenue over time
   - Bar chart: top products by revenue
   - KPI: total revenue (today), avg order value
4. Собираем дашборд

## Этап 5: Мониторинг и алерты

```yaml
# dbt tests run daily
# Airflow alert on DAG failure
# Elementary / Monte Carlo для observability
```

## Чему учит кейс

1. **ELT, не ETL**: грузим сырые данные, трансформируем в DWH (dbt)
2. **Разделение ответственности**:
   - Airflow — оркестрация (запустить в нужное время)
   - Python — extract/load (API → DWH)
   - dbt — трансформации (SQL + тесты)
   - Metabase — визуализация
3. **Тесты — не роскошь**: они спасают, когда API меняет формат, а ты об этом не знаешь
4. **Инкрементальность**: `if_exists='append'`, а не перезаписывать всю таблицу каждый день

## Связанные страницы

- [[../06-data-processing/etl-vs-elt|ETL vs ELT]]
- [[../11-data-engineering/dbt-transformations|dbt]]
- [[../06-data-processing/data-pipelines-orchestration|Оркестрация]]
- [[../08-visualization/dashboard-design|Дизайн дашбордов]]
