# BI-инструменты: ландшафт

## Что такое BI

**Business Intelligence** — инструменты для превращения данных в дашборды, отчёты и интерактивные визуализации, доступные бизнес-пользователям без знания кода.

## Ландшафт (2024-2026)

```
Open Source                    Commercial                    Enterprise
─────────────────────────────────────────────────────────────────────
Metabase      Tableau         Power BI
Apache Superset  Looker       Qlik
Grafana          Looker Studio   Sisense
Redash           Holistics        MicroStrategy
```

## Сравнение ключевых игроков

| | Metabase | Superset | Tableau | Power BI | Looker |
|---|---|---|---|---|---|
| **Лицензия** | Open-source | Open-source | Коммерческая | Коммерческая | Коммерческая |
| **SQL** | Да | Да | Частично | Да | LookML |
| **Drag-n-drop** | Да | Ограничено | Да | Да | Нет |
| **Self-serve** | ★★★ | ★★ | ★★★ | ★★★ | ★★ |
| **Embedding** | ★★★ | ★★★ | ★★ | ★★ | ★★★ |
| **Масштабирование** | Среднее | Высокое | Высокое | Высокое | Очень высокое |
| **Кому** | Стартапы, SMB | Tech-компании | Enterprise | Microsoft-стек | Data-first компании |

## Open-source BI

### Metabase

- Самый простой старт: `java -jar metabase.jar`
- SQL + визуальный построитель запросов
- Красивые дашборды из коробки
- Идеален для стартапов и внутренней аналитики

### Apache Superset

- Мощнее Metabase, сложнее в настройке
- SQL Lab — полноценная IDE для запросов
- Кэширование (Redis), много типов визуализаций
- Для компаний с выделенной data-командой

### Grafana

- Не совсем BI — скорее мониторинг
- Идеален для временных рядов, метрик, логов
- Часто используют вместе с BI-инструментом

## Коммерческие BI

### Tableau

- Король визуализации: самые красивые и гибкие графики
- Дорогой (~$70/пользователь/месяц)
- Сложная модель данных (Tableau Data Model)

### Power BI

- Дёшево (Pro ~$10/мес), интеграция с Microsoft-стеком
- DAX — мощный, но сложный язык формул
- Сложно версионировать и CI/CD

### Looker

- LookML — моделирование данных как код (git-friendly!)
- Дорогой. Куплен Google, интегрирован в Google Cloud
- Data-first подход: всё начинается с модели данных

## Как выбирать

| Ситуация | Рекомендация |
|----------|-------------|
| Стартап, <20 человек, нужна быстрая аналитика | Metabase |
| Tech-компания, data-команда, open-source | Superset |
| Enterprise, Microsoft-стек, дёшево | Power BI |
| Enterprise, важен дизайн и визуализация | Tableau |
| Data-first культура, git-подход, Google Cloud | Looker |

## Тренд: Headless BI

Данные моделируются в dbt, метрики определяются в коде (metricflow), визуализация — отдельный слой. Инструменты:
- **Lightdash** — open-source BI на dbt
- **MetricFlow** — семантический слой от dbt Labs

## Связанные страницы

- [[../08-visualization/dashboard-design|Дизайн дашбордов]]
- [[../08-visualization/data-storytelling|Сторителлинг данными]]
- [[../11-data-engineering/dbt-transformations|dbt]]
