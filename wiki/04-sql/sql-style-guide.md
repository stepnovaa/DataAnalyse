# SQL Style Guide

## Зачем стайлгайд

Код читают чаще, чем пишут. SQL в аналитике живёт годами в dbt-моделях, отчётах, дашбордах. Единый стиль — это уважение к будущему себе и коллегам.

## Ключевые слова — ВЕРХНИЙ РЕГИСТР

```sql
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
  AND o.created_at >= '2024-01-01'
GROUP BY u.id, u.name
HAVING COUNT(*) > 1
ORDER BY u.name
LIMIT 100;
```

- SELECT, FROM, WHERE, JOIN, ON, AND, OR, GROUP BY, HAVING, ORDER BY, LIMIT — UPPERCASE
- Названия таблиц, колонок, алиасов — lowercase (snake_case)

## Форматирование

### Вертикальная структура

Каждая основная клаузула с новой строки:

```sql
SELECT ...
FROM ...
WHERE ...
GROUP BY ...
HAVING ...
ORDER BY ...
LIMIT ...
```

### AND/OR на отдельных строках

```sql
WHERE country = 'RU'
  AND status = 'active'
  AND created_at >= '2024-01-01'
```

AND/OR — **в начале** строки (легче комментировать и добавлять условия).

### JOIN'ы

```sql
INNER JOIN orders o
    ON u.id = o.user_id
    AND o.deleted_at IS NULL
LEFT JOIN payments p
    ON o.id = p.order_id
```

- Каждый JOIN с новой строки
- ON с отступом
- Явно указывай тип (INNER, LEFT) — не оставляй просто JOIN

### Подзапросы и CTE

```sql
WITH active_users AS (
    SELECT user_id
    FROM users
    WHERE status = 'active'
),

recent_orders AS (
    SELECT user_id, COUNT(*) AS order_count
    FROM orders
    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY user_id
)

SELECT u.user_id, COALESCE(ro.order_count, 0) AS order_count
FROM active_users u
LEFT JOIN recent_orders ro ON u.user_id = ro.user_id;
```

- CTE с осмысленными именами, разделены запятыми
- Скобки на отдельных строках
- Вложенные подзапросы → перепиши в CTE

## Именование

| Вещь | Стиль | Пример |
|------|-------|--------|
| Таблицы | snake_case, plural | `users`, `order_items` |
| Колонки | snake_case, singular | `created_at`, `user_id` |
| Первичный ключ | `id` или `table_name_id` | `id`, `product_id` |
| Внешний ключ | `referenced_table_id` | `user_id`, `category_id` |
| Булевы колонки | `is_` / `has_` префикс | `is_active`, `has_discount` |
| Даты | `_at` суффикс | `created_at`, `deleted_at` |
| Агрегаты (CTE) | смысл + `_agg` | `user_stats`, `monthly_revenue` |

### Алиасы

- Осмысленные, не однобуквенные (не `a`, `b`, `c`)
- Для таблиц: краткий смысл (`cust` для customers, `ord` для orders)
- Вместо `x` напиши `stats` — сэкономишь время будущему читателю

## Явность

### Явно указывай JOIN-тип

```sql
-- ❌ Плохо
FROM users JOIN orders ON ...

-- ✅ Хорошо
FROM users INNER JOIN orders ON ...
```

### Явные имена колонок

```sql
-- ❌ Плохо
SELECT * FROM users;

-- ✅ Хорошо
SELECT id, name, email, created_at FROM users;
```

### Квалифицируй колонки в JOIN'ах

```sql
-- ❌ Непонятно откуда id
SELECT id, name, total FROM users u JOIN orders o ON u.id = o.user_id;

-- ✅ Явно
SELECT u.id, u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id;
```

## Комментарии

```sql
-- Разовые ad-hoc запросы: комментарий с вопросом и датой
-- Q: Сколько активных пользователей в RU за последнюю неделю?
-- 2024-06-01, Вадим

-- Для продакшн-кода (dbt): описание модели в YAML
```

## Антипаттерны

- `SELECT *` в продакшене
- Неявные JOIN'ы (`FROM a, b WHERE a.id = b.id`)
- `RIGHT JOIN` → перепиши на `LEFT JOIN`
- NATURAL JOIN — сломается при изменении схемы
- `ORDER BY ordinal` (`ORDER BY 2, 1`)
- Бессмысленные алиасы (`t1`, `t2`, `x`)

## Инструменты

- **SQLFluff** — линтер с кастомизируемыми правилами
- **dbt** — встроенные проверки стиля
- **DataGrip** — встроенный форматтер

## Связанные страницы

- [[../04-sql/sql-basics|SQL — Основы]]
- [[../04-sql/sql-performance|Практическая оптимизация SQL]]
