# Операции над множествами

## Три операции

| Операция | SQL | Описание |
|----------|-----|----------|
| Объединение | `UNION [ALL]` | Строки из A ИЛИ B |
| Пересечение | `INTERSECT [ALL]` | Строки из A И B одновременно |
| Разность | `EXCEPT [ALL]` | Строки из A, которых нет в B |

## UNION

```sql
SELECT city FROM customers
UNION
SELECT city FROM suppliers
ORDER BY city;
```

### UNION vs UNION ALL

| | UNION | UNION ALL |
|---|---|---|
| Дубликаты | Удаляет | Сохраняет |
| Производительность | Медленнее (сортировка) | Быстрее |
| Когда | Нужны уникальные строки | Нужны все строки |

> **Default = UNION DISTINCT** (без ALL). Всегда думай, нужен ли тебе DISTINCT — если нет, используй ALL.

## INTERSECT

```sql
-- Города, где есть и клиенты, и поставщики
SELECT city FROM customers
INTERSECT
SELECT city FROM suppliers;
```

## EXCEPT (MINUS в Oracle)

```sql
-- Клиенты, которые ещё не сделали заказ
SELECT id FROM customers
EXCEPT
SELECT customer_id FROM orders;
```

## Правила операций над множествами

1. Одинаковое **количество колонок** в обоих SELECT'ах
2. Совместимые **типы данных**
3. ORDER BY только в конце всего выражения
4. Имена колонок берутся из первого SELECT

## Практические паттерны

### Сравнение двух таблиц

```sql
-- Строки в A, которых нет в B
SELECT * FROM table_a EXCEPT SELECT * FROM table_b;
-- Строки в B, которых нет в A
SELECT * FROM table_b EXCEPT SELECT * FROM table_a;
```

### Full diff (PostgreSQL)

```sql
SELECT 'only_a' AS source, * FROM table_a EXCEPT SELECT * FROM table_b
UNION ALL
SELECT 'only_b' AS source, * FROM table_b EXCEPT SELECT * FROM table_a;
```

### UNION для вертикальной конкатенации

```sql
SELECT 'Q1' AS quarter, * FROM q1_sales
UNION ALL
SELECT 'Q2', * FROM q2_sales
UNION ALL
SELECT 'Q3', * FROM q3_sales
UNION ALL
SELECT 'Q4', * FROM q4_sales;
```

## UNION vs JOIN

| | UNION | JOIN |
|---|---|---|
| Направление | Вертикальное | Горизонтальное |
| Структура | Добавляет строки | Добавляет колонки |
| Итого строк | A + B (при ALL) | ≤ A × B |

## Связанные страницы

- [[../04-sql/joins-and-subqueries|JOIN'ы и подзапросы]]
- [[../04-sql/ctes-and-recursive|CTE и рекурсивные запросы]]
