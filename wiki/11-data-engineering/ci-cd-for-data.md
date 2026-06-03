# CI/CD для данных

## Зачем

Данные — код. Трансформации (dbt), пайплайны (Airflow), инфраструктура (Terraform) — всё должно быть в git и проходить через CI/CD.

## Что такое CI/CD для данных

| | CI | CD |
|---|---|---|
| **Что** | Автоматическая проверка при PR | Автоматический деплой |
| **Как** | `dbt test`, `sqlfluff lint`, `dbt compile` | `dbt run` в production |
| **Цель** | Не сломать production | Быстрая доставка изменений |

## CI для dbt

```yaml
# .github/workflows/dbt-ci.yml
name: dbt CI
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pip install dbt-snowflake
      - run: dbt deps
      - run: dbt compile          # проверить что компилируется
      - run: sqlfluff lint models/  # стиль
      - run: dbt test --select state:modified+  # тесты на изменённые модели
```

## CD для dbt

```yaml
# deploy.yml
on:
  push:
    branches: [main]
jobs:
  deploy:
    steps:
      - run: dbt deps
      - run: dbt run --target prod
      - run: dbt test --target prod
```

## Data Contracts

**Контракт данных** — соглашение между producer и consumer о схеме и качестве данных:

```yaml
# data_contract.yaml для таблицы orders
schema:
  - field: order_id
    type: integer
    constraints: [unique, not_null]
  - field: amount
    type: decimal
    constraints: {min: 0}
sla:
  freshness: 1 hour
  completeness: 99.9%
```

Инструменты: **Soda**, **Great Expectations**, кастомные проверки в dbt.

## Версионирование данных

- **dbt**: трансформации в git
- **Schema changes**: миграции (как в коде)
- **Data snapshots**: dbt snapshots (SCD Type 2)
- **Data versioning**: DVC, LakeFS, Delta Lake time travel

## Лучшие практики

1. **PR обязателен** для изменений в production-моделях
2. **CI запускает тесты** на изменённые модели (+ downstream)
3. **Slim CI**: тестируем только затронутые модели (dbt `state:modified+`)
4. **Data diff**: сравниваем prod vs dev на сэмпле (Datafold)
5. **Rollback plan**: знаем как откатить, если деплой сломает данные

## Связанные страницы

- [[../11-data-engineering/dbt-transformations|dbt]]
- [[../06-data-processing/data-quality-and-testing|Качество данных]]
- [[../06-data-processing/data-pipelines-orchestration|Оркестрация]]
