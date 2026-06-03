# Apache Kafka

## Что такое Kafka

Распределённый **лог сообщений**. Не очередь (хотя можно использовать как очередь). Это commit log для потоков данных.

## Основные концепции

```
Producer → [Topic / Partition] → Consumer
```

| Компонент | Что это |
|-----------|---------|
| **Message** | Ключ + значение + timestamp + заголовки |
| **Topic** | Категория/канал сообщений (как таблица) |
| **Partition** | Часть топика (для параллелизма). Сообщения упорядочены внутри партиции |
| **Producer** | Пишет сообщения в топик |
| **Consumer** | Читает сообщения (в группе) |
| **Broker** | Сервер Kafka |
| **Offset** | Позиция сообщения в партиции (монотонно возрастает) |

## Почему Kafka быстрый

- **Последовательный I/O** (append-only), а не случайный
- **Zero-copy**: данные из диска в сеть без копирования в user-space
- **Батчинг**: producer и consumer группируют сообщения
- **Партиционирование**: параллелизм на уровне партиций

## Семантика доставки

| Уровень | Гарантия |
|---------|----------|
| **At most once** | Сообщение может потеряться |
| **At least once** (default) | Сообщение дойдёт, но может дублироваться |
| **Exactly once** | Идемпотентный producer + транзакции |

## Паттерны использования

### Pub/Sub

```
Сервис A → Kafka → Сервис B, C, D
```

Один producer, много consumer'ов. Каждый читает в своём темпе.

### Event Sourcing

```
Все изменения → Kafka (log) → Пересчитать состояние когда угодно
```

### Stream Processing

```
Kafka → Kafka Streams / Spark / Flink → Kafka / DB
```

Обработка потоков в реальном времени.

### CDC (Change Data Capture)

```
PostgreSQL WAL → Debezium → Kafka → Data Lake / DWH
```

Захват изменений в БД и передача в другие системы.

## Kafka Connect

Фреймворк для подключения внешних систем без кода:
- **Source connectors**: БД → Kafka (Debezium для MySQL/Postgres)
- **Sink connectors**: Kafka → S3, Elasticsearch, JDBC

## Когда Kafka

- Потоковая передача данных между сервисами
- Событийная архитектура (event-driven)
- Буфер между producer и consumer (разная скорость)
- Лог изменений (audit, event sourcing)

## Когда НЕ Kafka

- Простая очередь задач (RabbitMQ/Redis проще)
- RPC / request-response (gRPC/REST лучше)
- Мало данных (< 1000 msg/sec) — Kafka оверхед
- Нет компетенций в команде — администрировать сложно

## Связанные страницы

- [[../10-big-data/spark-streaming|Spark Streaming]]
- [[../10-big-data/big-data-paradigm|Парадигма Big Data]]
- [[../06-data-processing/working-with-apis|Работа с API]]
