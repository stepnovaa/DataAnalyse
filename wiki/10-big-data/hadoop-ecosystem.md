# Hadoop — экосистема

## Нужен ли Hadoop в 2026?

Кратко: **нет, если ты не поддерживаешь legacy или не в on-premise enterprise.** Облачные Data Lake (S3 + Spark/Trino) заменили Hadoop. Но понимать его полезно — идеи живут в современных системах.

## Компоненты

```
Hadoop
├── HDFS       — распределённая файловая система
├── YARN       — менеджер ресурсов кластера
└── MapReduce  — вычислительная модель (устарела)
```

### HDFS (Hadoop Distributed File System)

- Данные разбиваются на блоки (обычно 128 МБ)
- Каждый блок реплицируется (обычно 3 копии)
- NameNode хранит метаданные (какой файл → какие блоки → на каких узлах)
- DataNode'ы хранят сами блоки

**Минусы HDFS**:
- NameNode — single point of failure (в HA — два, но сложно)
- Small files problem: много мелких файлов → перегрузка NameNode
- Не для real-time (batch-ориентирован)

### Современная замена: Object Storage

- S3 (AWS), GCS (Google Cloud), Blob Storage (Azure)
- Дешевле, масштабируется автоматически, нет NameNode bottleneck
- Spark/Trino могут читать напрямую из S3

## Когда Hadoop ещё жив

- On-premise enterprise с огромными данными
- Легаси-инфраструктура
- Строгие требования к хранению данных (регуляторы)

## Что выучить вместо Hadoop

1. **Облачный Data Lake**: S3 + IAM + Lifecycle Policies
2. **Spark**: работает поверх S3, не нужен HDFS
3. **Форматы**: Parquet, Iceberg, Delta Lake
4. **Оркестрация**: Airflow

## Связанные страницы

- [[../10-big-data/big-data-paradigm|Парадигма Big Data]]
- [[../10-big-data/spark-deep-dive|Spark]]
- [[../10-big-data/data-lake-architecture|Data Lake]]
