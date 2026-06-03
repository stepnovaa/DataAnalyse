# Архитектура хранилищ данных

## DWH vs БД

Data Warehouse ≠ обычная база данных. DWH оптимизирован для **аналитических запросов** (агрегации, JOIN'ы по большим таблицам), а не для транзакций.

## Kimball vs Inmon

Два классических подхода:

| | Kimball | Inmon |
|---|---|---|
| **Подход** | Снизу-вверх: сначала data marts | Сверху-вниз: единый DWH |
| **Схема** | Звезда / Снежинка | 3НФ |
| **Скорость запуска** | Быстро (недели) | Медленно (месяцы) |
| **Гибкость** | Меньше | Больше |
| **Сложность** | Проще для бизнеса | Сложнее, но целостнее |

**В 2026 Kimball побеждает**: быстрее, дешевле, Agile-friendly. Inmon — для крупных enterprise с тонной legacy.

## Размерное моделирование (Dimensional Modeling)

### Факты и Измерения

```
Fact:    business events, measures    → SUM, COUNT, AVG
Dim:     контекст, описания            → WHERE, GROUP BY
```

```
         Dim_Date         Dim_Product
             \              //
              Fact_Sales
             //              \
      Dim_Customer        Dim_Store
```

### Типы таблиц фактов

| Тип | Описание |
|-----|----------|
| **Transaction** | Одна строка = одно событие (заказ, платёж) |
| **Periodic Snapshot** | Состояние на момент (остатки на конец дня) |
| **Accumulating Snapshot** | Одна строка на процесс, обновляется (жизненный цикл заказа) |

### SCD (Slowly Changing Dimensions)

Измерения меняются. Как хранить историю?

- **Type 0**: Не меняем (редко)
- **Type 1**: Перезаписываем (нет истории)
- **Type 2**: Новая строка (полная история) — **стандарт**
- **Type 3**: Добавляем previous_value (ограниченная история)

## Современный DWH-стек

```
ELT:    Fivetran/Airbyte → Snowflake/BigQuery/Redshift
Model:  dbt (трансформации, тесты, документация)
BI:     Looker/Superset/Metabase
```

## Облачные DWH — сравнение

| | Snowflake | BigQuery | Redshift |
|---|---|---|---|
| **Архитектура** | Раздельные compute/storage | Serverless | Кластеры |
| **Масштабирование** | Авто | Авто | Ручное |
| **SQL** | Стандартный + расширения | Стандартный | PostgreSQL-based |
| **Цена** | $$ (per credit) | $ (per query) | $ (per node-hour) |
| **Когда** | Лучший default | GCP-стек | AWS-стек |

## Связанные страницы

- [[../03-databases-relational/data-modeling-patterns|Паттерны моделирования]]
- [[../11-data-engineering/dbt-transformations|dbt]]
- [[../10-big-data/data-lake-architecture|Data Lake]]
