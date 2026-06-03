# Real-Time аналитика

## Что это

Аналитика, где данные доступны через **секунды** (не часы) после события. Дашборд обновляется автоматически, алерт срабатывает мгновенно.

## Batch vs Real-Time

| | Batch | Real-Time |
|---|---|---|
| **Задержка** | Часы (ETL ночью) | Секунды |
| **Запросы** | Сложные, на больших данных | Простые, предрасчитанные |
| **Пользователь** | Аналитик | Оператор, алерт, dashboard |
| **Пример** | Месячный отчёт | Детектор мошенничества при платеже |

## Инструменты

### ClickHouse

OLAP-база данных для real-time аналитики:

```sql
CREATE TABLE events (
    timestamp DateTime,
    event_type String,
    user_id UInt64,
    properties Nested(key String, value String)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp)
ORDER BY (event_type, timestamp);

-- Запрос за 50ms на миллиардах строк
SELECT event_type, COUNT() AS cnt
FROM events
WHERE timestamp >= now() - INTERVAL 1 HOUR
GROUP BY event_type
ORDER BY cnt DESC;
```

**Ключевое**: колоночное хранение, векторизация, сжатие, партиционирование.

### Materialize

Streaming SQL-база данных. Поддерживает PostgreSQL wire protocol:

```sql
-- Материализованное представление, обновляется мгновенно
CREATE MATERIALIZED VIEW hourly_stats AS
SELECT
    date_trunc('hour', timestamp) AS hour,
    event_type,
    COUNT(*) AS cnt
FROM events
GROUP BY hour, event_type;
```

Данные в представлении всегда актуальны — не надо перестраивать.

### Apache Druid

Для massive-scale real-time аналитики (рекламные платформы, телеком).

### Tinybird

Managed-сервис поверх ClickHouse. Для стартапов и SMB.

## Lambda и Kappa архитектуры

### Lambda
```
Данные → [Batch Layer (Spark)] → DWH (раз в час)
       → [Speed Layer (Flink)] → Real-time API (мгновенно)
```
Минус: две кодовые базы.

### Kappa
```
Данные → Kafka → Streaming (Flink/kSQL) → Serving Layer
```
Всё — streaming. Проще, но сложные пересчёты истории — проблема.

## Когда real-time

- Алерты (аномалии, падения метрик)
- Operational дашборды (доставка еды, такси, logistics)
- Fraud detection (при платеже)
- A/B-тесты с мгновенной обратной связью
- Персонализация (рекомендации в реальном времени)

## Когда НЕ real-time

- Месячные/квартальные отчёты
- Глубокий ad-hoc анализ (нужен полный DWH)
- Данные, которые обновляются раз в сутки (нет смысла)

## Связанные страницы

- [[../10-big-data/kafka-data-streaming|Kafka]]
- [[../10-big-data/spark-streaming|Spark Streaming]]
- [[../10-big-data/data-lake-architecture|Data Lake]]
