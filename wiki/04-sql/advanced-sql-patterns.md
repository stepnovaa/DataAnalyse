# Продвинутые SQL-паттерны

## Pivot (поворот таблицы)

Превратить строки в колонки:

### Через CASE (универсально)

```sql
SELECT
    year,
    SUM(CASE WHEN quarter = 'Q1' THEN revenue ELSE 0 END) AS q1,
    SUM(CASE WHEN quarter = 'Q2' THEN revenue ELSE 0 END) AS q2,
    SUM(CASE WHEN quarter = 'Q3' THEN revenue ELSE 0 END) AS q3,
    SUM(CASE WHEN quarter = 'Q4' THEN revenue ELSE 0 END) AS q4
FROM sales
GROUP BY year;
```

### Через CROSSTAB (PostgreSQL)

```sql
CREATE EXTENSION tablefunc;
SELECT * FROM crosstab(
    'SELECT year, quarter, revenue FROM sales ORDER BY 1,2',
    'SELECT DISTINCT quarter FROM sales ORDER BY 1'
) AS ct(year INT, q1 NUMERIC, q2 NUMERIC, q3 NUMERIC, q4 NUMERIC);
```

### Unpivot (колонки → строки)

```sql
SELECT year, 'Q1' AS quarter, q1 AS revenue FROM pivoted
UNION ALL
SELECT year, 'Q2', q2 FROM pivoted
UNION ALL
SELECT year, 'Q3', q3 FROM pivoted
UNION ALL
SELECT year, 'Q4', q4 FROM pivoted;
```

## Gaps and Islands

### Gaps (пропуски)

Найти пропуски в последовательности ID:

```sql
SELECT (id + 1) AS gap_start, (next_id - 1) AS gap_end
FROM (
    SELECT id, LEAD(id) OVER (ORDER BY id) AS next_id
    FROM items
) t
WHERE next_id > id + 1;
```

### Islands (острова непрерывности)

Сгруппировать последовательные ID:

```sql
WITH numbered AS (
    SELECT id, id - ROW_NUMBER() OVER (ORDER BY id) AS grp
    FROM items
)
SELECT MIN(id) AS island_start, MAX(id) AS island_end, COUNT(*) AS size
FROM numbered
GROUP BY grp
ORDER BY island_start;
```

## Running Total (накопительная сумма)

```sql
SELECT date, amount,
    SUM(amount) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) AS balance
FROM transactions;
```

## Percentile (перцентили)

```sql
-- PostgreSQL
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median,
       PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY salary) AS p95
FROM employees;

-- Общий подход (для любой БД)
SELECT AVG(salary) AS median
FROM (
    SELECT salary,
        ROW_NUMBER() OVER (ORDER BY salary) AS rn,
        COUNT(*) OVER () AS total
    FROM employees
) t WHERE rn IN ((total + 1) / 2, (total + 2) / 2);
```

## Условный COUNT DISTINCT

```sql
SELECT
    COUNT(DISTINCT user_id) FILTER (WHERE action = 'purchase') AS buyers,
    COUNT(DISTINCT user_id) FILTER (WHERE action = 'view') AS viewers
FROM events;
```

## Date Spine (генерация ряда дат)

```sql
-- PostgreSQL
SELECT generate_series('2024-01-01'::date, '2024-12-31'::date, '1 day') AS date;

-- Общий подход (рекурсивный CTE)
WITH RECURSIVE dates(date) AS (
    SELECT '2024-01-01'::date
    UNION ALL
    SELECT date + 1 FROM dates WHERE date < '2024-12-31'
)
SELECT date FROM dates;
```

**Применение**: заполнить даты без данных, чтобы график не прерывался:

```sql
WITH dates AS (
    SELECT generate_series('2024-01-01', '2024-01-31', '1 day'::interval)::date AS date
)
SELECT d.date, COALESCE(s.revenue, 0) AS revenue
FROM dates d
LEFT JOIN daily_sales s ON d.date = s.date;
```

## Deduplication (дедупликация)

```sql
-- Оставить последнюю запись для каждого user_id
SELECT DISTINCT ON (user_id) *
FROM events
ORDER BY user_id, created_at DESC;

-- Через ROW_NUMBER (портабельно)
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
    FROM events
) t WHERE rn = 1;
```

## Ratio to Parent

```sql
SELECT category, product, revenue,
    revenue * 100.0 / SUM(revenue) OVER (PARTITION BY category) AS pct_of_category,
    revenue * 100.0 / SUM(revenue) OVER () AS pct_of_total
FROM product_sales;
```

## Связанные страницы

- [[../04-sql/window-functions-advanced|Оконные функции]]
- [[../04-sql/ctes-and-recursive|CTE и рекурсивные запросы]]
- [[../04-sql/sql-performance|Практическая оптимизация SQL]]
