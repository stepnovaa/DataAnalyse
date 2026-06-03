# Реляционные базы данных

> **Map of Content.** Реляционные БД — основа хранения данных в индустрии уже 50 лет. Понимание их устройства критично для аналитика и инженера.

## Страницы раздела

- [[03-databases-relational/relational-model|Реляционная модель]] — отношения, кортежи, ключи, целостность
- [[03-databases-relational/normalization|Нормализация]] — 1НФ → 5НФ, денормализация: когда и зачем
- [[03-databases-relational/indexing-internals|Индексы — внутреннее устройство]] — B-Tree, Hash, GiST, GIN, EXPLAIN
- [[03-databases-relational/transactions-and-acid|Транзакции и ACID]] — уровни изоляции, MVCC, блокировки, deadlock
- [[03-databases-relational/query-optimization|Оптимизация запросов]] — план выполнения, узкие места, профайлинг
- [[03-databases-relational/postgresql-deep-dive|PostgreSQL Deep Dive]] — архитектура, расширения, лучшие практики
- [[03-databases-relational/mysql-deep-dive|MySQL/InnoDB Deep Dive]] — отличия от Postgres, особенности
- [[03-databases-relational/sqlite-internals|SQLite — архитектура]] — когда применять, ограничения, file-based модель
- [[03-databases-relational/data-modeling-patterns|Паттерны моделирования данных]] — звезда, снежинка, EAV, наследование

## Ключевые вопросы

- Почему реляционная модель до сих пор доминирует?
- Как индекс ускоряет запрос — и когда он бесполезен?
- Чем жертвуем ради ACID — и всегда ли оно нужно?
