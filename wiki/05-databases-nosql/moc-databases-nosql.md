# Нереляционные базы данных

> **Map of Content.** NoSQL — не «no SQL», а «not only SQL». Зоопарк моделей данных для задач, где реляционка не оптимальна.

## Страницы раздела

- [[05-databases-nosql/nosql-taxonomy|NoSQL-таксономия]] — ключ-значение, документные, колоночные, графовые
- [[05-databases-nosql/cap-theorem|CAP-теорема и PACELC]] — консистентность vs доступность vs устойчивость к разделению
- [[05-databases-nosql/mongodb-deep-dive|MongoDB Deep Dive]] — документная модель, aggregation pipeline, индексы
- [[05-databases-nosql/redis-deep-dive|Redis Deep Dive]] — структуры данных, persistence, pub/sub, кэширование
- [[05-databases-nosql/cassandra-wide-column|Cassandra и Wide-Column]] — CQL, архитектура кольца, compaction
- [[05-databases-nosql/neo4j-graph-databases|Графовые БД — Neo4j]] — Cypher, когда графы эффективнее SQL
- [[05-databases-nosql/elasticsearch-search-analytics|Elasticsearch]] — инвертированный индекс, полнотекстовый поиск, агрегации
- [[05-databases-nosql/nosql-vs-sql-decision|NoSQL vs SQL — когда что выбирать]] — дерево решений, критерии, антипаттерны

## Ключевые вопросы

- Почему «просто возьмём MongoDB» — плохая стратегия по умолчанию?
- Когда реляционка тормозит, а NoSQL взлетает?
- Как CAP-теорема предсказывает поведение распределённой БД под нагрузкой?
