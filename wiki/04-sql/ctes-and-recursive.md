# CTE и рекурсивные запросы

## CTE (Common Table Expression)

CTE — временный именованный результат, существующий только в рамках одного запроса:

```sql
WITH user_stats AS (
    SELECT user_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY user_id
)
SELECT u.name, COALESCE(us.order_count, 0) AS orders
FROM users u
LEFT JOIN user_stats us ON u.id = us.user_id;
```

### Зачем CTE

- **Читаемость**: даёшь имя сложному подзапросу
- **Переиспользование**: один CTE можно использовать несколько раз в запросе
- **Рекурсия**: единственный способ написать рекурсивный запрос в SQL

### CTE vs подзапрос

| | CTE (WITH) | Подзапрос |
|---|---|---|
| Читаемость | ✅ Лучше | ❌ Хуже для сложных |
| Переиспользование | ✅ Можно | ❌ Надо дублировать |
| Производительность | ⚠️ Может материализоваться | ⚠️ Встраивается в план |
| Отладка | ✅ Можно SELECT * FROM cte | ❌ Только весь запрос |

### Материализация CTE

В PostgreSQL CTE по умолчанию материализуется (вычисляется один раз и хранится в памяти). Это оптимизационный барьер — планировщик не может «протолкнуть» WHERE внутрь CTE.

```sql
-- PostgreSQL ≤ 11: CTE всегда материализуется
-- PostgreSQL ≥ 12: можно управлять
WITH cte AS MATERIALIZED (...)  -- принудительно материализовать
WITH cte AS NOT MATERIALIZED (...)  -- встроить в план (как подзапрос)
```

## Цепочки CTE

```sql
WITH
monthly AS (
    SELECT DATE_TRUNC('month', created_at) AS month, SUM(total) AS revenue
    FROM orders GROUP BY 1
),
with_growth AS (
    SELECT *, LAG(revenue) OVER (ORDER BY month) AS prev_revenue
    FROM monthly
)
SELECT month, revenue,
    ROUND((revenue - prev_revenue) * 100.0 / prev_revenue, 1) AS growth_pct
FROM with_growth
ORDER BY month;
```

## Рекурсивные CTE

Структура:

```sql
WITH RECURSIVE cte AS (
    -- Базовый случай (начальные строки)
    SELECT ...
    UNION ALL
    -- Рекурсивный шаг (ссылается на cte)
    SELECT ... FROM cte WHERE условие_останова
)
SELECT * FROM cte;
```

### Генерация последовательности

```sql
WITH RECURSIVE numbers(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 100
)
SELECT n FROM numbers;
```

### Иерархии (org chart)

```sql
WITH RECURSIVE org AS (
    -- Топ-менеджеры (нет начальника)
    SELECT id, name, manager_id, 1 AS level, name::TEXT AS path
    FROM employees WHERE manager_id IS NULL

    UNION ALL

    -- Подчинённые
    SELECT e.id, e.name, e.manager_id, o.level + 1, o.path || ' → ' || e.name
    FROM employees e
    JOIN org o ON e.manager_id = o.id
)
SELECT id, name, level, path FROM org ORDER BY path;
```

### Дерево категорий

```sql
WITH RECURSIVE category_tree AS (
    SELECT id, name, parent_id, 0 AS depth
    FROM categories WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.name, c.parent_id, ct.depth + 1
    FROM categories c
    JOIN category_tree ct ON c.parent_id = ct.id
)
SELECT id, REPEAT('  ', depth) || name AS display
FROM category_tree ORDER BY id;  -- осторожно: порядок не гарантирует иерархию
```

## Ограничения

- Только `UNION ALL` (не UNION) в рекурсивной части
- Рекурсивная часть не может использовать агрегаты, GROUP BY, DISTINCT
- Только одна ссылка на CTE в FROM рекурсивной части
- Нет подзапросов с этим же CTE

## Связанные страницы

- [[../04-sql/window-functions-advanced|Оконные функции]]
- [[../04-sql/set-operations|UNION / INTERSECT / EXCEPT]]
- [[../04-sql/sql-performance|Практическая оптимизация SQL]]
