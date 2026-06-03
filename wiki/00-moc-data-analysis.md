# Data Analysis & Databases — Карта знаний

> **Навигационный хаб.** Отсюда расходятся все разделы вики. Выбери направление или иди по порядку.

---

## Рекомендуемые пути

### Путь 1: С нуля до аналитика
`01 → 04 → 03 → 06 → 07 → 08 → 02 → 09 → 14`
Фундамент → SQL → базы → обработка → EDA → визуализация → статистика → ML → кейсы.

### Путь 2: С нуля до дата-инженера
`01 → 03 → 04 → 06 → 11 → 10 → 05`
Фундамент → реляционные БД → SQL → обработка → инженерия → большие данные → NoSQL.

### Путь 3: Быстрый референс
Прыгай в нужный раздел через MOC — каждая страница содержит cross-links на связанные темы.

---

## Полная карта разделов

### 📐 [01 — Фундамент](01-fundamentals/moc-fundamentals.md)
Что такое анализ данных, типы и структуры, жизненный цикл, роли, аналитическое мышление.

- [[01-fundamentals/what-is-data-analysis|Что такое анализ данных]]
- [[01-fundamentals/data-types-and-structures|Типы и структуры данных]]
- [[01-fundamentals/data-lifecycle|Жизненный цикл данных]]
- [[01-fundamentals/roles-in-data|Роли в данных]]
- [[01-fundamentals/analytical-thinking|Аналитическое мышление]]

### 📊 [02 — Статистика](02-statistics/moc-statistics.md)
Описательная и инференциальная статистика, вероятности, проверка гипотез, A/B-тесты.

- [[02-statistics/descriptive-statistics|Описательная статистика]]
- [[02-statistics/probability-basics|Основы вероятности]]
- [[02-statistics/distributions|Распределения]]
- [[02-statistics/inferential-statistics|Статистический вывод]]
- [[02-statistics/hypothesis-testing|Проверка гипотез]]
- [[02-statistics/correlation-and-regression|Корреляция и регрессия]]
- [[02-statistics/ab-testing|A/B-тестирование]]

### 🗄️ [03 — Реляционные БД](03-databases-relational/moc-databases-relational.md)
Реляционная модель, нормализация, индексы, транзакции, Postgres, MySQL, SQLite, паттерны.

- [[03-databases-relational/relational-model|Реляционная модель]]
- [[03-databases-relational/normalization|Нормализация]]
- [[03-databases-relational/indexing-internals|Индексы — внутреннее устройство]]
- [[03-databases-relational/transactions-and-acid|Транзакции и ACID]]
- [[03-databases-relational/query-optimization|Оптимизация запросов]]
- [[03-databases-relational/postgresql-deep-dive|PostgreSQL Deep Dive]]
- [[03-databases-relational/mysql-deep-dive|MySQL Deep Dive]]
- [[03-databases-relational/sqlite-internals|SQLite — архитектура]]
- [[03-databases-relational/data-modeling-patterns|Паттерны моделирования]]

### 💾 [04 — SQL](04-sql/moc-sql.md)
От SELECT до оконных функций, CTE, продвинутые паттерны, оптимизация, стайлгайд.

- [[04-sql/sql-basics|SQL — Основы]]
- [[04-sql/joins-and-subqueries|JOIN'ы и подзапросы]]
- [[04-sql/aggregations-and-grouping|Агрегации и GROUP BY]]
- [[04-sql/window-functions-advanced|Оконные функции — продвинутый уровень]]
- [[04-sql/ctes-and-recursive|CTE и рекурсивные запросы]]
- [[04-sql/set-operations|Операции над множествами]]
- [[04-sql/advanced-sql-patterns|Продвинутые SQL-паттерны]]
- [[04-sql/sql-performance|Практическая оптимизация SQL]]
- [[04-sql/sql-style-guide|SQL Style Guide]]

### 🧩 [05 — Нереляционные БД](05-databases-nosql/moc-databases-nosql.md)
NoSQL-таксономия, CAP-теорема, MongoDB, Redis, Cassandra, Neo4j, Elasticsearch.

- [[05-databases-nosql/nosql-taxonomy|NoSQL-таксономия]]
- [[05-databases-nosql/cap-theorem|CAP-теорема и PACELC]]
- [[05-databases-nosql/mongodb-deep-dive|MongoDB Deep Dive]]
- [[05-databases-nosql/redis-deep-dive|Redis Deep Dive]]
- [[05-databases-nosql/cassandra-wide-column|Cassandra и Wide-Column]]
- [[05-databases-nosql/neo4j-graph-databases|Графовые БД — Neo4j]]
- [[05-databases-nosql/elasticsearch-search-analytics|Elasticsearch]]
- [[05-databases-nosql/nosql-vs-sql-decision|NoSQL vs SQL — когда что]]

### ⚙️ [06 — Обработка данных](06-data-processing/moc-data-processing.md)
ETL/ELT, очистка данных, pandas/Polars, оркестрация, качество, работа с API.

- [[06-data-processing/etl-vs-elt|ETL vs ELT]]
- [[06-data-processing/data-cleaning|Очистка данных]]
- [[06-data-processing/data-wrangling-python|Data Wrangling — Python]]
- [[06-data-processing/polars-modern-dataframes|Polars — современные датафреймы]]
- [[06-data-processing/data-pipelines-orchestration|Оркестрация пайплайнов]]
- [[06-data-processing/data-quality-and-testing|Качество данных]]
- [[06-data-processing/working-with-apis|Работа с API]]

### 🔍 [07 — Разведочный анализ (EDA)](07-exploratory-analysis/moc-eda.md)
Фреймворк EDA, одно-/дву-/многомерный анализ, пропуски, feature engineering.

- [[07-exploratory-analysis/eda-framework|EDA-фреймворк]]
- [[07-exploratory-analysis/univariate-analysis|Одномерный анализ]]
- [[07-exploratory-analysis/bivariate-analysis|Двумерный анализ]]
- [[07-exploratory-analysis/multivariate-analysis|Многомерный анализ]]
- [[07-exploratory-analysis/missing-data-strategies|Стратегии работы с пропусками]]
- [[07-exploratory-analysis/feature-engineering|Проектирование признаков]]
- [[07-exploratory-analysis/eda-case-studies|EDA — разбор кейсов]]

### 📈 [08 — Визуализация](08-visualization/moc-visualization.md)
Грамматика графики, выбор графика, matplotlib/Plotly, дашборды, сторителлинг.

- [[08-visualization/viz-grammar-and-theory|Грамматика графики]]
- [[08-visualization/chart-chooser|Выбор графика]]
- [[08-visualization/matplotlib-seaborn|Matplotlib + Seaborn]]
- [[08-visualization/plotly-interactive|Plotly — интерактивная визуализация]]
- [[08-visualization/bi-tools-landscape|BI-инструменты: ландшафт]]
- [[08-visualization/dashboard-design|Дизайн дашбордов]]
- [[08-visualization/data-storytelling|Сторителлинг данными]]
- [[08-visualization/color-and-accessibility|Цвет и доступность]]

### 🤖 [09 — Машинное обучение](09-machine-learning/moc-machine-learning.md)
Supervised/unsupervised, деревья, временные ряды, NLP, ML-пайплайны, ML vs статистика.

- [[09-machine-learning/ml-taxonomy|ML-таксономия]]
- [[09-machine-learning/supervised-learning|Обучение с учителем]]
- [[09-machine-learning/unsupervised-learning|Обучение без учителя]]
- [[09-machine-learning/tree-based-models|Деревья и ансамбли]]
- [[09-machine-learning/model-evaluation|Оценка моделей]]
- [[09-machine-learning/time-series-analysis|Временные ряды]]
- [[09-machine-learning/nlp-for-analysis|NLP для аналитики]]
- [[09-machine-learning/ml-pipeline-mlflow|ML-пайплайны и MLflow]]
- [[09-machine-learning/ml-vs-statistics|ML vs Статистика]]

### ⚡ [10 — Большие данные](10-big-data/moc-big-data.md)
Парадигма Big Data, Hadoop, Spark, Kafka, Data Lake, DuckDB.

- [[10-big-data/big-data-paradigm|Парадигма Big Data]]
- [[10-big-data/hadoop-ecosystem|Hadoop — экосистема]]
- [[10-big-data/spark-deep-dive|Apache Spark Deep Dive]]
- [[10-big-data/spark-streaming|Spark Streaming]]
- [[10-big-data/kafka-data-streaming|Kafka — потоковая передача]]
- [[10-big-data/data-lake-architecture|Data Lake — архитектура]]
- [[10-big-data/duckdb-local-analytics|DuckDB — встроенная аналитика]]

### 🏗️ [11 — Инженерия данных](11-data-engineering/moc-data-engineering.md)
Хранилища данных, dbt, Data Mesh, governance, современный стек, CI/CD для данных.

- [[11-data-engineering/data-warehouse-architecture|Архитектура хранилищ]]
- [[11-data-engineering/dbt-transformations|dbt — трансформации как код]]
- [[11-data-engineering/data-mesh-vs-monolith|Data Mesh vs монолит]]
- [[11-data-engineering/data-governance|Data Governance]]
- [[11-data-engineering/modern-data-stack|Современный стек данных]]
- [[11-data-engineering/ci-cd-for-data|CI/CD для данных]]

### 🚀 [12 — Современные тренды](12-modern-trends/moc-modern-trends.md)
Векторные БД, LLM-аналитика, real-time, observability, приватность.

- [[12-modern-trends/vector-databases|Векторные базы данных]]
- [[12-modern-trends/llm-for-data-analysis|LLM в аналитике]]
- [[12-modern-trends/real-time-analytics|Real-Time аналитика]]
- [[12-modern-trends/data-observability|Наблюдаемость данных]]
- [[12-modern-trends/privacy-and-ethics|Приватность и этика]]
- [[12-modern-trends/data-mesh-in-practice|Data Mesh на практике]]

### 🛠️ [13 — Инструментарий](13-toolbox/moc-toolbox.md)
Python/R, Jupyter, SQL IDE, CLI-инструменты, облачные платформы.

- [[13-toolbox/python-data-stack|Python Data Stack]]
- [[13-toolbox/r-for-statistics|R для статистики]]
- [[13-toolbox/jupyter-workflow|Jupyter Workflow]]
- [[13-toolbox/sql-ides-and-clients|SQL IDE и клиенты]]
- [[13-toolbox/cli-tools-for-data|CLI-инструменты для данных]]
- [[13-toolbox/cloud-platforms-compare|Облачные платформы — сравнение]]

### 📋 [14 — Практические кейсы](14-case-studies/moc-case-studies.md)
End-to-end разборы: отток клиентов, воронки продаж, атрибуция, аномалии, пайплайны.

- [[14-case-studies/customer-churn-analysis|Анализ оттока клиентов]]
- [[14-case-studies/sales-funnel-analytics|Воронка продаж]]
- [[14-case-studies/marketing-attribution|Атрибуция маркетинга]]
- [[14-case-studies/anomaly-detection-production|Поиск аномалий]]
- [[14-case-studies/building-a-data-pipeline|Построение дата-пайплайна]]

---

## Быстрые ссылки по темам

- **Только начинаешь?** → [[01-fundamentals/what-is-data-analysis|Что такое анализ данных]]
- **Хочешь SQL?** → [[04-sql/sql-basics|SQL — Основы]]
- **Нужна визуализация?** → [[08-visualization/chart-chooser|Выбор графика]]
- **Выбираешь БД?** → [[05-databases-nosql/nosql-vs-sql-decision|NoSQL vs SQL]]
- **Готовишься к собеседованию?** → [[14-case-studies/moc-case-studies|Практические кейсы]]
