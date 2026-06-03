# Облачные платформы — сравнение

## Три кита

| | AWS | GCP | Azure |
|---|---|---|---|
| **DWH** | Redshift | BigQuery | Synapse |
| **Data Lake** | S3 + Lake Formation | GCS + BigLake | ADLS + Purview |
| **ETL** | Glue | Dataflow / Data Fusion | Data Factory |
| **Orchestration** | MWAA (Airflow) / Step Functions | Cloud Composer (Airflow) | Data Factory |
| **Real-time** | Kinesis + MSK (Kafka) | Pub/Sub + Dataflow | Event Hubs + Stream Analytics |
| **BI** | QuickSight | Looker / Looker Studio | Power BI |
| **ML** | SageMaker | Vertex AI | Azure ML |
| **Serverless SQL** | Athena | BigQuery (serverless) | Synapse Serverless |

## Как выбирать

### AWS — когда

- Самая богатая экосистема (200+ сервисов)
- Ты уже в AWS (EC2, RDS, etc.)
- Нужен максимальный контроль и гибкость
- Готов платить complexity tax

**Data stack**: S3 → Glue → Redshift → QuickSight

### GCP — когда

- BigQuery — лучший serverless DWH
- Data-centric компания (Looker, Google Analytics)
- Хочешь меньше complexity, больше managed
- Меньше legacy, современный стек

**Data stack**: BigQuery → dbt → Looker

### Azure — когда

- Ты в Microsoft-стеке (Office 365, Power BI, Dynamics)
- Enterprise, compliance, hybrid cloud
- Power BI — основной BI-инструмент
- Хочешь единого вендора (Microsoft)

**Data stack**: ADLS → Synapse → Power BI

## Сравнение стоимости

| Сервис | Модель | ~Цена |
|--------|--------|-------|
| **BigQuery** | Per query (data scanned) | $5/TB scanned |
| **Redshift** | Per node-hour | $1/час (RA3) |
| **Snowflake** | Per credit | $2-3/credit |
| **S3** | Per GB stored | $0.023/GB/мес |
| **Athena** | Per query | $5/TB scanned |

## Практический совет

Если начинаешь с нуля и не привязан к экосистеме:

**GCP + BigQuery + dbt** — самый простой старт. BigQuery serverless (не думаешь о кластере), dbt для трансформаций.

## Multi-cloud

Некоторые компании используют:
- **AWS** для инфраструктуры
- **GCP** для BigQuery (аналитика)
- **Snowflake** на AWS/GCP/Azure

Multi-cloud сложнее, но даёт leverage в переговорах с вендорами.

## Связанные страницы

- [[../11-data-engineering/data-warehouse-architecture|Архитектура хранилищ]]
- [[../11-data-engineering/modern-data-stack|Современный стек]]
- [[../10-big-data/data-lake-architecture|Data Lake]]
