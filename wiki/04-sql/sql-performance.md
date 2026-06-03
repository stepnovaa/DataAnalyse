# Практическая оптимизация SQL

## Методология

1. **Измерь** → EXPLAIN ANALYZE
2. **Найди bottleneck** → где больше всего времени/строк?
3. **Исправь ОДНУ вещь**
4. **Перемерь** → стало лучше?
5. Повтори

Никогда не оптимизируй «на глаз». Базы данных полны сюрпризов.

## Чтение EXPLAIN ANALYZE

```sql
EXPLAIN (ANALYZE, BUFFERS, TIMING, FORMAT TEXT)
SELECT ...
```

### На что смотреть

```
Sort (cost=100..120 rows=1000 width=64) (actual time=15.2..15.8 rows=1000 loops=1)
    Sort Key: created_at DESC
    Sort Method: quicksort  Memory: 128kB
    -> Seq Scan on orders (cost=0..50 rows=1000 width=64)
       (actual time=0.015..5.2 rows=1000 loops=1)
       Buffers: shared hit=45
```

- **cost=** — оценка планировщика. Чем меньше, тем лучше. Разница с actual → плохая статистика
- **actual time** — реальное время. Первое число = время до первой строки, второе = общее
- **rows** — если оценка сильно расходится с actual → `ANALYZE table`
- **Buffers** — hit (из кэша) vs read (с диска). Много read → добавить памяти или улучшить индексы

## Частые проблемы и решения

### 1. Seq Scan на большой таблице

**Диагноз**: `Seq Scan on large_table (rows=5000000)`

**Решения** (по приоритету):
1. Создать индекс под WHERE/JOIN
2. Проверить что индекс используется: `EXPLAIN` не показывает Index Scan
3. `ANALYZE table` — обновить статистику
4. Возможно, возвращается >20% таблицы → Seq Scan оправдан

### 2. Nested Loop вместо Hash Join

```
Nested Loop (rows=10000 loops=5000)
```

Для каждой строки внешней таблицы — сканирование внутренней. Кошмар.

**Решения**:
- Добавить индекс на JOIN-колонку внутренней таблицы
- `ANALYZE` для корректных оценок
- `SET enable_nestloop = off` (на сессию, осторожно)

### 3. Сортировка на диске

```
Sort Method: external merge  Disk: 204800kB
```

`work_mem` недостаточно.

**Решения**:
- Увеличить `work_mem` для сессии: `SET work_mem = '512MB'`
- Убрать ORDER BY если не нужен
- Добавить индекс, который уже даёт нужный порядок

### 4. Медленный OFFSET

```sql
-- Плохо: сканирует и выбрасывает 100000 строк
SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 100000;
```

**Решение — keyset pagination:**
```sql
SELECT * FROM orders
WHERE id > 123456  -- последний id предыдущей страницы
ORDER BY id
LIMIT 20;
```

### 5. Функции на индексируемых колонках

```sql
-- Индекс по email бесполезен! Планировщик не знает что LOWER(email) = email
WHERE LOWER(email) = 'user@mail.com'

-- Решение: функциональный индекс
CREATE INDEX idx_email_lower ON users (LOWER(email));
```

### 6. OR в WHERE

```sql
-- Часто превращается в Seq Scan
WHERE status = 'active' OR created_at > '2024-01-01'

-- Решение: UNION ALL
SELECT * FROM t WHERE status = 'active'
UNION ALL
SELECT * FROM t WHERE created_at > '2024-01-01' AND status != 'active'
```

### 7. COUNT(*) на больших таблицах

PostgreSQL сканирует ВСЮ таблицу для COUNT(*). Для приблизительного значения:

```sql
SELECT reltuples::bigint AS estimate
FROM pg_class WHERE relname = 'table_name';
```

## Инструменты профилирования

### PostgreSQL

```sql
-- Включить профилирование
LOAD 'auto_explain';
SET auto_explain.log_min_duration = 1000;  -- логировать запросы дольше 1с
SET auto_explain.log_analyze = true;

-- Самые медленные запросы (pg_stat_statements)
CREATE EXTENSION pg_stat_statements;
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;
```

### MySQL

```sql
-- Slow query log
SET GLOBAL slow_query_log = ON;
SET GLOBAL long_query_time = 1;

-- Текущие запросы
SHOW PROCESSLIST;
SHOW ENGINE INNODB STATUS;
```

## План действий при медленном запросе

1. `EXPLAIN ANALYZE` → понять где время
2. Проверить индексы → созданы ли? используются ли?
3. Проверить статистику → `ANALYZE`
4. Упростить логику → лишние JOIN'ы? подзапросы?
5. Проверить конфигурацию → work_mem, shared_buffers, effective_cache_size
6. Рассмотреть денормализацию / materialized view
7. Рассмотреть партиционирование

## Связанные страницы

- [[../03-databases-relational/indexing-internals|Индексы]]
- [[../03-databases-relational/query-optimization|Оптимизация запросов]]
- [[../04-sql/sql-style-guide|SQL Style Guide]]
