# Apache Spark Deep Dive

## Что такое Spark

Распределённый вычислительный движок. Умеет batch, streaming, SQL и ML на кластере из десятков/сотен машин.

## Архитектура

```
Driver (твоя программа)
    ↓
Cluster Manager (YARN / Kubernetes / Standalone)
    ↓
Executors (рабочие процессы на узлах кластера)
```

- **Driver** — твой код, координирует работу
- **Executors** — выполняют задачи, хранят данные в памяти
- **Cluster Manager** — управляет ресурсами

## RDD, DataFrame, Dataset

| API | Уровень | Оптимизация | Когда |
|-----|---------|-------------|-------|
| **RDD** | Низкий | Нет | Legacy / сложная логика |
| **DataFrame** | Высокий | Catalyst оптимизатор | 95% задач |
| **Dataset** | Высокий + типы | Catalyst | Scala/Java, строгая типизация |

В Python используй **DataFrame** — это основной API.

## PySpark — базовые операции

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('analysis').getOrCreate()

# Чтение
df = spark.read.parquet('s3://bucket/data/')
df = spark.read.csv('data.csv', header=True, inferSchema=True)

# Фильтрация
df.filter(df.age > 30)
df.filter('age > 30')

# Агрегация
df.groupBy('category').agg(
    F.avg('price').alias('avg_price'),
    F.count('*').alias('count')
)

# JOIN
df1.join(df2, on='key', how='left')

# Оконные функции
from pyspark.sql.window import Window
window = Window.partitionBy('category').orderBy('price')
df.withColumn('rank', F.row_number().over(window))

# Сохранение
df.write.parquet('output.parquet', mode='overwrite')
```

## Ленивые вычисления (Lazy Evaluation)

Spark **ничего не делает**, пока не вызван action:

- **Transformations** (ленивые): `filter`, `select`, `groupBy`, `join`
- **Actions** (запускают вычисления): `show`, `count`, `collect`, `write`

Это позволяет Catalyst-оптимизатору построить эффективный план.

## Catalyst Optimizer

План запроса проходит 4 стадии:
1. **Analysis** — разрешение имён колонок и типов
2. **Logical Optimization** — predicate pushdown, projection pruning
3. **Physical Planning** — выбор join-алгоритма (broadcast vs shuffle)
4. **Code Generation** — генерация Java-кода (Tungsten)

## Shuffle — узкое место

Shuffle — перемещение данных между партициями (join, groupBy, window). Это самая дорогая операция в Spark.

### Минимизация shuffle

- **Broadcast Join**: маленькую таблицу (<10 МБ) копируем на каждый executor
- **`reduceByKey` вместо `groupByKey`**: агрегирует локально перед shuffle
- **Правильное партиционирование**: если данные уже сгруппированы по ключу

## Конфигурация

```python
spark.conf.set('spark.sql.shuffle.partitions', 200)  # дефолт
spark.conf.set('spark.sql.adaptive.enabled', True)  # AQE
```

- `shuffle.partitions`: слишком мало → большие партиции (OOM), слишком много → overhead
- **AQE (Adaptive Query Execution)**: Spark сам адаптирует план на лету

## Когда Spark

- Данные > 1 ТБ (не влезают в DuckDB/Polars)
- Распределённая обработка
- Batch + Streaming в одном фреймворке
- ML на больших данных (Spark MLlib)

## Когда НЕ Spark

- < 100 ГБ данных (Polars/DuckDB быстрее)
- Интерактивная аналитика (Trino лучше)
- Низкая latency (< 100ms) (Flink)

## Связанные страницы

- [[../10-big-data/big-data-paradigm|Парадигма Big Data]]
- [[../10-big-data/spark-streaming|Spark Streaming]]
- [[../10-big-data/duckdb-local-analytics|DuckDB]]
