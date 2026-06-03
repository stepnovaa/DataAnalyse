# SQL — Основы

## Структура запроса

```sql
SELECT [DISTINCT] колонки
FROM таблица
[JOIN ... ON ...]
WHERE условие
GROUP BY колонки
HAVING условие_на_агрегаты
ORDER BY колонки [ASC|DESC]
LIMIT число [OFFSET число]
```

### Логический порядок выполнения

В отличие от порядка написания, SQL выполняет запрос в таком порядке:

```
1. FROM + JOIN    — откуда берём данные
2. WHERE          — фильтрация строк
3. GROUP BY       — группировка
4. HAVING         — фильтрация групп
5. SELECT         — выбор колонок + агрегаты
6. ORDER BY       — сортировка
7. LIMIT/OFFSET   — ограничение
```

> Понимание этого порядка критично! Именно поэтому алиасы из SELECT нельзя использовать в WHERE.

## SELECT и FROM

```sql
-- Базовый SELECT
SELECT column1, column2 FROM table_name;

-- Все колонки (НЕ использовать в production-коде!)
SELECT * FROM table_name;

-- Алиасы
SELECT column1 AS alias_name FROM table_name;

-- DISTINCT — уникальные значения
SELECT DISTINCT city FROM users;

-- Выражения
SELECT price * quantity AS total FROM order_items;
```

## WHERE

```sql
-- Сравнение
WHERE age >= 18
WHERE status = 'active'
WHERE created_at > '2024-01-01'

-- Логические операторы
WHERE age >= 18 AND status = 'active'
WHERE country = 'RU' OR country = 'BY'

-- IN
WHERE status IN ('active', 'pending', 'trial')

-- BETWEEN
WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31'

-- LIKE (с _ = 1 символ, % = любое количество)
WHERE email LIKE '%@gmail.com'
WHERE phone LIKE '+7___%'

-- IS NULL / IS NOT NULL
WHERE deleted_at IS NULL

-- NOT
WHERE NOT (status = 'cancelled')
```

## ORDER BY

```sql
ORDER BY created_at DESC          -- новые первыми
ORDER BY country, city DESC       -- по стране, затем по городу
ORDER BY 2, 1                     -- по второй и первой колонке (не рекомендуется)
ORDER BY CASE WHEN city = 'Moscow' THEN 0 ELSE 1 END  -- Moscow первыми
```

## LIMIT и OFFSET

```sql
-- Топ-10
SELECT * FROM orders ORDER BY total DESC LIMIT 10;

-- Пагинация (страница 2, по 20 записей)
SELECT * FROM orders ORDER BY id LIMIT 20 OFFSET 20;
```

> OFFSET на больших таблицах — боль. Для пагинации по большим данным используй keyset pagination (WHERE id > last_seen_id LIMIT 20).

## Работа с NULL

NULL — не значение, а отсутствие значения. Особые правила:
- `NULL = NULL` → NULL (не TRUE!)
- `NULL + 5` → NULL
- Проверка: `IS NULL`, `IS NOT NULL`
- `COALESCE(column, default)` — заменить NULL на значение

## CASE

```sql
SELECT
    name,
    CASE
        WHEN price < 100 THEN 'Дешёвый'
        WHEN price < 1000 THEN 'Средний'
        ELSE 'Дорогой'
    END AS price_category
FROM products;
```

## Связанные страницы

- [[../04-sql/joins-and-subqueries|JOIN'ы и подзапросы]]
- [[../04-sql/aggregations-and-grouping|Агрегации и GROUP BY]]
- [[../04-sql/sql-style-guide|SQL Style Guide]]
