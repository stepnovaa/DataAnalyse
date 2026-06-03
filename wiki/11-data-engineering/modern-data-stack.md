# Современный стек данных (Modern Data Stack)

## Что это

Набор инструментов для построения аналитической инфраструктуры. Облачный, SQL-центричный, с разделением compute и storage.

## Эталонный стек

```
Ingestion:      Fivetran / Airbyte / Stitch
Storage:        Snowflake / BigQuery / Redshift / S3+Iceberg
Transformation: dbt
Orchestration:  Airflow / Prefect / Dagster
BI:             Looker / Superset / Metabase
Governance:     DataHub / Atlan
Observability:  Monte Carlo / Great Expectations
Reverse ETL:    Hightouch / Census
```

## Почему «современный»

| Старый стек | Современный стек |
|-------------|-----------------|
| On-premise (Hadoop) | Облачный (Snowflake) |
| ETL (Informatica) | ELT (Fivetran + dbt) |
| Монолитная команда | Self-serve аналитика |
| Ручное тестирование | Автоматические тесты (dbt) |
| Без версионирования | Git + CI/CD |

## Выбор стека под размер компании

### Стартап / SMB (до 50 человек)

```
Stitch/Airbyte → BigQuery → dbt → Metabase
```

Быстро, дёшево, без dedicated data engineer.

### Scale-up (50-500)

```
Fivetran → Snowflake → dbt → Airflow → Looker/Superset
```

Добавляется оркестрация, observability, governance.

### Enterprise (500+)

```
Fivetran/Kafka → Snowflake/Iceberg → dbt → Airflow → Looker
    + DataHub/Atlan + Monte Carlo + RBAC
```

Полный стек с governance, lineage, CI/CD.

## Тренды Modern Data Stack (2024-2026)

- **Lakehouse**: Iceberg/Delta Lake заменяют проприетарные форматы
- **Headless BI**: метрики в коде (MetricFlow), BI — только визуализация
- **AI в data stack**: LLM пишут dbt-модели, находят аномалии
- **Consolidation**: Fivetran купил Hightouch, dbt Labs строит платформу

## Связанные страницы

- [[../11-data-engineering/dbt-transformations|dbt]]
- [[../11-data-engineering/data-warehouse-architecture|Архитектура хранилищ]]
- [[../08-visualization/bi-tools-landscape|BI-инструменты]]
