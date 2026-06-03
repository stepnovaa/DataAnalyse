# Агрегации и GROUP BY

## Агрегатные функции

| Функция | Возвращает |
|---------|------------|
| **COUNT(*)** | Количество строк |
| **COUNT(column)** | Количество не-NULL значений |
| **COUNT(DISTINCT column)** | Количество уникальных значений |
| **SUM(column)** | Сумма |
| **AVG(column)** | Среднее |
| **MIN(column)** | Минимум |
| **MAX(column)** | Максимум |
| **STRING_AGG(col, sep)** | Конкатенация строк |
| **ARRAY_AGG(col)** | Массив значений (PostgreSQL) |
| **BOOL_AND/BOOL_OR** | Логические агрегаты |

## GROUP BY

```sql
SELECT
    dept_id,
    COUNT(*) AS employee_count,
    AVG(salary) AS avg_salary,
    MAX(salary) AS max_salary
FROM employees
GROUP BY dept_id;
```

**Правило**: всё что в SELECT без агрегации — должно быть в GROUP BY.

## HAVING

Фильтрация **после** агрегации (WHERE фильтрует **до**):

```sql
SELECT dept_id, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id
HAVING AVG(salary) > 50000;
```

### WHERE vs HAVING

| | WHERE | HAVING |
|---|---|---|
| Когда применяется | До группировки | После группировки |
| Что фильтрует | Строки | Группы |
| Агрегаты | ❌ Нельзя | ✅ Можно |

## DISTINCT vs GROUP BY

```sql
-- Эти запросы идентичны
SELECT DISTINCT city FROM users;
SELECT city FROM users GROUP BY city;
```

DISTINCT — частный случай GROUP BY без агрегатов. Для подсчёта уникальных всегда используй GROUP BY + COUNT.

## ROLLUP, CUBE, GROUPING SETS

### ROLLUP — иерархические итоги

```sql
SELECT
    COALESCE(country, 'Всего') AS country,
    COALESCE(city, 'Всего') AS city,
    SUM(sales) AS total
FROM sales
GROUP BY ROLLUP (country, city);
```

Результат: итоги по странам-городам → по странам → общий итог.

### CUBE — все комбинации

```sql
GROUP BY CUBE (country, city)
```

Результат: по country+city, только country, только city, общий итог. Все 2^n комбинаций.

### GROUPING SETS — конкретные комбинации

```sql
GROUP BY GROUPING SETS ((country, city), (country), ())
```

### Функция GROUPING

```sql
SELECT
    CASE WHEN GROUPING(country) = 1 THEN 'Все страны' ELSE country END
```

Определяет, является ли NULL результатом агрегации или реальным значением.

## FILTER (агрегаты с условием)

```sql
SELECT
    dept_id,
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE salary > 50000) AS high_paid,
    AVG(salary) FILTER (WHERE age < 30) AS young_avg
FROM employees
GROUP BY dept_id;
```

Элегантнее, чем подзапросы или CASE внутри агрегатов.

## DISTINCT внутри агрегатов

```sql
SELECT COUNT(DISTINCT user_id) FROM orders;          -- сколько уникальных пользователей
SELECT COUNT(DISTINCT (user_id, product_id)) FROM o;  -- уникальных пар (PostgreSQL)
```

## Связанные страницы

- [[../04-sql/window-functions-advanced|Оконные функции]]
- [[../04-sql/sql-basics|SQL — Основы]]
- [[../02-statistics/descriptive-statistics|Описательная статистика]]
