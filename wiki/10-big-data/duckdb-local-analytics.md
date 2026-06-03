# DuckDB — встроенная аналитика

## Что такое DuckDB

**Встраиваемая OLAP-база данных** (как SQLite, но для аналитики). Одна библиотека, ноль серверов, миллиарды строк на ноутбуке.

## DuckDB vs всё

| | DuckDB | SQLite | PostgreSQL | Spark |
|---|---|---|---|---|
| **Тип** | OLAP | OLTP | OLTP | Распределённый OLAP |
| **Сервер** | Нет | Нет | Да | Да |
| **Данные** | До ~100 ГБ | До ~1 ГБ | До ~ТБ | ТБ-ПБ |
| **Запросы** | Аналитика | CRUD | CRUD | Batch |
| **Формат** | Колоночный | Строковый | Строковый | Колоночный |
| **Установка** | `pip install duckdb` | Встроенная | Сервер | Кластер |

## Базовое использование

```python
import duckdb

# In-memory
conn = duckdb.connect()

# В файл
conn = duckdb.connect('analytics.db')

# Запрос к CSV/Parquet ПРЯМО НА ДИСКЕ
conn.execute('''
    SELECT category, SUM(amount) AS total
    FROM 'sales_2024.parquet'
    WHERE date >= '2024-01-01'
    GROUP BY category
    ORDER BY total DESC
''').fetchdf()
```

## Killer Features

### Прямые запросы к файлам

```sql
-- Parquet, CSV, JSON — без импорта!
SELECT * FROM 's3://bucket/data/*.parquet';
SELECT * FROM 'data_*.csv';
```

### Интеграция с Pandas/Polars

```python
# Pandas → DuckDB
duckdb.sql('SELECT * FROM df WHERE age > 30').to_df()  # polars
duckdb.sql('SELECT * FROM df WHERE age > 30').df()     # pandas

# DuckDB → Pandas
df_pandas = conn.execute('SELECT ...').fetchdf()
```

### Колоночное хранение + векторизация

Данные хранятся и обрабатываются по колонкам (как ClickHouse). Аналитические запросы (агрегации, фильтры) летают.

### Поддержка SQL

Почти полный стандарт SQL: оконные функции, CTE, correlated subqueries, `QUALIFY`, `PIVOT`, `LIST`, STRUCT types.

## Производительность

- **Parquet на диске**: авто-индексация (min/max в группах строк), предикатный pushdown, projection pushdown
- **В памяти**: векторизованный движок, JIT-компиляция выражений
- **Многопоточность**: автоматически

## Когда DuckDB

- Локальная аналитика на данных 1-100 ГБ
- Замена Pandas/Polars для сложных SQL-запросов
- Быстрый прототип до Spark
- Встраиваемая аналитика в Python-приложениях
- Запросы к Parquet/CSV без импорта

## Когда НЕ DuckDB

- OLTP (транзакции, concurrent writes) → PostgreSQL
- > 1 ТБ → Spark/Trino
- Multi-user server → ClickHouse/Trino
- Стриминг → Flink/Kafka

## DuckDB + MotherDuck

MotherDuck — облачный сервис поверх DuckDB. Локально + облачная синхронизация:

```sql
ATTACH 'md:' AS cloud;
SELECT * FROM cloud.orders;
```

## Связанные страницы

- [[../10-big-data/big-data-paradigm|Парадигма Big Data]]
- [[../06-data-processing/polars-modern-dataframes|Polars]]
- [[../10-big-data/spark-deep-dive|Spark]]
