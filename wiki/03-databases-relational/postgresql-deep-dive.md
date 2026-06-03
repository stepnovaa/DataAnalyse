# PostgreSQL Deep Dive

## Почему Postgres

- **MVCC без откатов** (no undo log — VACUUM вместо этого)
- **Расширяемость**: кастомные типы, языки (PL/Python, PL/V8), расширения (PostGIS, pgvector)
- **Стандарты**: самый близкий к SQL-стандарту из популярных СУБД
- **Лицензия**: полностью open-source, нет Enterprise-версии
- **Сообщество**: огромное, активное, tons of extensions

## Архитектура

```
Client → Postmaster → Backend Process (per connection)
                        ↓
                  Shared Buffers
                        ↓
              WAL Writer ← → WAL (Write-Ahead Log)
                        ↓
              Background Writer → Data Files
              Autovacuum → Cleanup
              Checkpointer → Checkpoints
```

### Ключевые процессы

| Процесс | Задача |
|---------|--------|
| **Postmaster** | Принимает соединения, форкает backend'ы |
| **Backend** | Один процесс на соединение (не поток!) |
| **WAL Writer** | Сбрасывает WAL на диск |
| **Background Writer** | Пишет dirty pages из shared buffers на диск |
| **Autovacuum** | Чистит мёртвые кортежи, обновляет статистику |
| **Checkpointer** | Создаёт контрольные точки для восстановления |

### Разделяемая память (Shared Buffers)

- Кэш страниц данных в памяти
- Все backend'ы читают из одного кэша
- Размер: обычно 25% RAM (но не больше ~10GB — дальше diminishing returns)
- Управляется clock-sweep алгоритмом (не LRU!)

## WAL (Write-Ahead Log)

**Правило**: изменение пишется в WAL ДО того, как пишется в data files.

Зачем:
- **Durability**: после краха восстанавливаемся по WAL
- **Репликация**: streaming replication передаёт WAL на реплики
- **Point-in-time recovery (PITR)**

## Расширения, которые стоит знать

| Расширение | Для чего |
|------------|----------|
| **pg_stat_statements** | Профилирование запросов — must-have |
| **PostGIS** | Гео-данные |
| **pgvector** | Векторные embeddings, similarity search |
| **pg_partman** | Автоматическое партиционирование |
| **pg_cron** | Планировщик внутри БД |
| **pg_repack** | Перестройка таблиц без долгих блокировок |

## JSONB vs MongoDB

PostgreSQL имеет зрелую поддержку JSONB:
- Индексация (GIN)
- Частичное обновление (jsonb_set)
- Атомарные операции
- Можно JOIN'ить JSONB с реляционными данными

> Когда нужен и строгий schema, и гибкий JSON — Postgres + JSONB часто лучше, чем MongoDB + ... схема.

## Лучшие практики

### Конфигурация (pgconf)

```ini
shared_buffers = 4GB              # 25% RAM
effective_cache_size = 12GB       # ~75% RAM
work_mem = 256MB                  # на операцию — осторожно, умножается на число соединений!
maintenance_work_mem = 1GB        # для VACUUM, CREATE INDEX
random_page_cost = 1.1            # для SSD
effective_io_concurrency = 200    # для SSD
wal_level = replica               # для репликации
max_wal_size = 4GB
checkpoint_timeout = 15min
```

### Connection Pooling

Postgres форкает **процесс** на каждое соединение. 1000 соединений = 1000 процессов = дорого. **Всегда используй пулер**:
- **PgBouncer**: лёгкий, session/transaction/statement pooling
- **Pgpool-II**: тяжелее, но умеет read/write splitting

### Мониторинг

```sql
-- Активные запросы
SELECT pid, state, query, age(clock_timestamp(), query_start)
FROM pg_stat_activity WHERE state != 'idle';

-- Самые медленные запросы (с pg_stat_statements)
SELECT query, mean_exec_time, calls
FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;

-- Размер таблиц
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_stat_user_tables ORDER BY pg_total_relation_size(relid) DESC;
```

## Связанные страницы

- [[../03-databases-relational/mysql-deep-dive|MySQL Deep Dive]] — сравнение
- [[../03-databases-relational/transactions-and-acid|Транзакции и ACID]]
- [[../03-databases-relational/indexing-internals|Индексы]]
