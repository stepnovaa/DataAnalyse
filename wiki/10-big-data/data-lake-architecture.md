# Data Lake — архитектура

## Что такое Data Lake

Централизованное хранилище сырых данных в нативном формате. Обычно на object storage (S3, GCS).

## Data Lake vs Data Warehouse

| | Data Lake | Data Warehouse |
|---|---|---|
| **Данные** | Сырые, неструктурированные | Обработанные, структурированные |
| **Схема** | Schema-on-read | Schema-on-write |
| **Пользователи** | Data Engineers, Scientists | Аналитики, BI |
| **Хранение** | Дешёвое (S3) | Дорогое (Snowflake) |
| **Запросы** | Сложные (Spark, Trino) | SQL (быстрые) |

> Data Lake + Data Warehouse = **Lakehouse**: сырые данные в озере + ACID и SQL поверх них.

## Медальонная архитектура (Medallion)

```
Bronze (сырые) → Silver (очищенные) → Gold (бизнес-уровень)
```

### Bronze (сырые данные)
- Данные как есть из источника
- Без трансформаций, append-only
- Полная история (никогда не удаляем)

### Silver (очищенные)
- Дедупликация, очистка, нормализация
- Объединение источников
- Пригодны для data science и ad-hoc анализа

### Gold (бизнес-уровень)
- Агрегированные, обогащённые
- Готовые для BI и отчётов
- Часто денормализованные (звезда/снежинка)

## Форматы данных

| Формат | Тип | Плюсы |
|--------|-----|-------|
| **CSV/JSON** | Строковый | Человекочитаемый, простой |
| **Parquet** | Колоночный | Сжатие, быстрые чтения по колонкам |
| **Avro** | Строковый | Схема, хорош для стриминга |
| **ORC** | Колоночный | Аналог Parquet для Hive |

**Всегда Parquet для аналитики.** Колоночное хранение + сжатие + предикатный pushdown.

## ACID поверх Data Lake

Обычный Data Lake не поддерживает транзакции (нельзя atomic UPDATE). Решения:

| Технология | Как работает |
|------------|-------------|
| **Delta Lake** | Паркет + transaction log (JSON) |
| **Apache Iceberg** | Паркет/ORC/AVRO + metadata layer |
| **Apache Hudi** | Паркет + timeline |

Все три добавляют: ACID-транзакции, time travel (запрос на момент времени), schema evolution.

## Современный Lakehouse-стек

```
S3 (хранение)
  +
Iceberg / Delta Lake (табличный формат, ACID)
  +
Trino / Spark (запросы и трансформации)
  +
dbt (моделирование)
  +
Superset / Metabase (BI)
```

## Связанные страницы

- [[../10-big-data/big-data-paradigm|Парадигма Big Data]]
- [[../11-data-engineering/data-warehouse-architecture|Архитектура хранилищ]]
- [[../10-big-data/spark-deep-dive|Spark]]
