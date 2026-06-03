# Оконные функции — продвинутый уровень

## Что такое оконная функция

Оконная функция вычисляет значение для строки, **учитывая другие строки в окне**, но не схлопывая их (в отличие от GROUP BY).

```sql
SELECT
    dept_id, name, salary,
    AVG(salary) OVER (PARTITION BY dept_id) AS dept_avg
FROM employees;
```

Каждая строка остаётся, плюс колонка со средним по отделу.

## Синтаксис

```sql
функция(...) OVER (
    PARTITION BY колонки    -- как GROUP BY для окна
    ORDER BY колонки         -- порядок внутри окна
    ROWS/RANGE/GROUPS ...    -- границы окна
)
```

## Функции ранжирования

| Функция | Поведение |
|---------|-----------|
| **ROW_NUMBER()** | Уникальный номер, даже при одинаковых значениях |
| **RANK()** | Одинаковые значения → одинаковый ранг, с пропусками |
| **DENSE_RANK()** | Одинаковые значения → одинаковый ранг, без пропусков |
| **NTILE(n)** | Делит на n примерно равных групп |
| **PERCENT_RANK()** | (rank - 1) / (total_rows - 1) |
| **CUME_DIST()** | Доля строк ≤ текущей |

```
Значения:    10, 20, 20, 30
ROW_NUMBER:   1,  2,  3,  4
RANK:         1,  2,  2,  4
DENSE_RANK:   1,  2,  2,  3
```

## Функции смещения

| Функция | Возвращает |
|---------|------------|
| **LAG(col, n, default)** | Значение n строк назад |
| **LEAD(col, n, default)** | Значение n строк вперёд |
| **FIRST_VALUE(col)** | Первое значение в окне |
| **LAST_VALUE(col)** | Последнее значение в окне |
| **NTH_VALUE(col, n)** | n-е значение в окне |

### LAG/LEAD — практика

```sql
SELECT
    date,
    revenue,
    LAG(revenue) OVER (ORDER BY date) AS prev_day,
    revenue - LAG(revenue) OVER (ORDER BY date) AS change,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY date)) * 100.0
        / LAG(revenue) OVER (ORDER BY date), 1
    ) AS change_pct
FROM daily_stats;
```

## Границы окна (ROWS / RANGE / GROUPS)

```sql
ROWS BETWEEN start AND end
```

| Режим | start | end |
|-------|-------|-----|
| Скользящее среднее | 2 PRECEDING | CURRENT ROW |
| Накопительная сумма | UNBOUNDED PRECEDING | CURRENT ROW |
| Всё окно | UNBOUNDED PRECEDING | UNBOUNDED FOLLOWING |
| Текущая + следующая | CURRENT ROW | 1 FOLLOWING |

### ROWS vs RANGE vs GROUPS

- **ROWS**: физические строки. `ROWS 2 PRECEDING` = буквально 2 предыдущие строки
- **RANGE**: логический диапазон. `RANGE 2 PRECEDING` = строки со значением в пределах [value-2, value]
- **GROUPS**: группы по значению ORDER BY

> Для 99% задач используй ROWS. RANGE — когда нужна семантика «строки с одинаковым значением».

## Практические паттерны

### Скользящее среднее

```sql
SELECT
    date, revenue,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma_7d
FROM daily_stats;
```

### Накопительная сумма

```sql
SELECT
    date, revenue,
    SUM(revenue) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) AS cumulative
FROM daily_stats;
```

### Разница с предыдущим

```sql
SELECT
    event_time, user_id, action,
    event_time - LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) AS time_since_last
FROM events;
```

### Top-N по группе

```sql
SELECT * FROM (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rn
    FROM employees
) ranked WHERE rn <= 3;
```

### Доля от группы

```sql
SELECT
    product_id, category, revenue,
    revenue * 100.0 / SUM(revenue) OVER (PARTITION BY category) AS pct_of_category
FROM product_sales;
```

## Связанные страницы

- [[../04-sql/aggregations-and-grouping|Агрегации и GROUP BY]]
- [[../04-sql/ctes-and-recursive|CTE и рекурсивные запросы]]
- [[../04-sql/advanced-sql-patterns|Продвинутые SQL-паттерны]]
