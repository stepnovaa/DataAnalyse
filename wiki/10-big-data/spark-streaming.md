# Spark Structured Streaming

## Batch vs Streaming

| | Batch | Streaming |
|---|---|---|
| **Данные** | Фиксированный набор | Непрерывный поток |
| **Обработка** | Периодически (раз в час/день) | Непрерывно |
| **Задержка** | Минуты/часы | Секунды/миллисекунды |
| **Пример** | Дневной отчёт | Детектор мошенничества |

## Structured Streaming

Высокоуровневый API на основе Spark SQL. Пишешь batch-код — Spark делает его streaming.

```python
# Чтение из Kafka
df = spark.readStream \
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'localhost:9092') \
    .option('subscribe', 'events') \
    .load()

# Обработка (тот же код что и для batch!)
from pyspark.sql.functions import from_json, col
parsed = df.select(from_json(col('value').cast('string'), schema).alias('data'))
result = parsed.groupBy('data.category').count()

# Запись
query = result.writeStream \
    .outputMode('complete') \
    .format('console') \
    .start()

query.awaitTermination()
```

## Оконные операции

```python
from pyspark.sql.functions import window

windowed = events.groupBy(
    window('timestamp', '10 minutes', '5 minutes'),  # окно 10 мин, шаг 5 мин
    'event_type'
).count()
```

- **Tumbling window**: фиксированный размер, без перекрытия
- **Sliding window**: размер + шаг, перекрываются
- **Session window**: динамический размер по активности

## Watermarks

```python
events.withWatermark('timestamp', '10 minutes')
```

Watermark — порог «опоздания» данных. Данные старше watermark отбрасываются. Позволяет освобождать состояние.

## Output Modes

| Режим | Поведение |
|-------|-----------|
| **Append** | Только новые строки (для простых трансформаций) |
| **Complete** | Полный результат каждый раз (для агрегаций без watermark) |
| **Update** | Только изменённые строки (для агрегаций с watermark) |

## Exactly-Once семантика

Spark Structured Streaming гарантирует exactly-once при использовании:
- Kafka + offset tracking в checkpoint
- File sink (идемпотентная запись)

## Kafka Integration

```python
df = spark.readStream.format('kafka')
    .option('kafka.bootstrap.servers', '...')
    .option('subscribe', 'topic')
    .option('startingOffsets', 'latest')
    .load()
```

См. [[../10-big-data/kafka-data-streaming|Kafka]].

## Когда Spark Streaming

- Уже используешь Spark для batch
- Нужна унификация batch и streaming кода
- Высокая пропускная способность (> 100k events/sec)

## Альтернативы

- **Apache Flink** — настоящий streaming (event-by-event), ниже latency
- **Kafka Streams** — лёгкая streaming-библиотека (Java)
- **RisingWave** — streaming SQL база данных

## Связанные страницы

- [[../10-big-data/spark-deep-dive|Spark Deep Dive]]
- [[../10-big-data/kafka-data-streaming|Kafka]]
- [[../10-big-data/big-data-paradigm|Парадигма Big Data]]
