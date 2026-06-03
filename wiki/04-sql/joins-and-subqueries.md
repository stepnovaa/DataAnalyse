# JOIN'ы и подзапросы

## Типы JOIN

SQL определяет 7 типов JOIN:

```
   A         B        A INNER JOIN B        A LEFT JOIN B        A RIGHT JOIN B     A FULL OUTER JOIN B
 ┌───┐    ┌───┐       ┌───┬───┐            ┌───┬───┐            ┌───┬───┐           ┌───┬───┐
 │ 1 │    │ 1 │       │ 1 │ 1 │            │ 1 │ 1 │            │ 1 │ 1 │           │ 1 │ 1 │
 │ 2 │    │ 3 │       └───┴───┘            │ 2 │   │            │   │ 3 │           │ 2 │   │
 │ 3 │    │ 4 │                            │ 3 │ 4 │            │ 3 │ 4 │           │ 3 │ 4 │
 └───┘    └───┘                            └───┴───┘            └───┴───┘           └───┴───┘
```

| JOIN | Результат |
|------|-----------|
| **INNER JOIN** | Только совпадающие строки из обеих таблиц |
| **LEFT JOIN** | Все строки из A + совпадения из B |
| **RIGHT JOIN** | Все строки из B + совпадения из A |
| **FULL OUTER JOIN** | Все строки из обеих таблиц |
| **CROSS JOIN** | Декартово произведение (каждая × каждая) |
| **SELF JOIN** | JOIN таблицы с самой собой |
| **NATURAL JOIN** | JOIN по всем одноимённым колонкам (избегай) |

## Синтаксис JOIN

```sql
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

### Явный vs неявный JOIN

```sql
-- Явный (рекомендуется)
FROM users u JOIN orders o ON u.id = o.user_id

-- Неявный (старого стиля, НЕ ИСПОЛЬЗУЙ)
FROM users u, orders o WHERE u.id = o.user_id
```

## LEFT JOIN — особенности

```sql
-- Пользователи и их заказы
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name;
```

- Все пользователи будут в результате, даже без заказов (order_count = 0)
- **Где ставить фильтр — критично**:
  - `WHERE o.status = 'paid'` — отфильтрует NULL → превратит LEFT JOIN в INNER
  - `AND o.status = 'paid'` в ON — оставит всех пользователей

## Подзапросы

### Скалярный подзапрос (одно значение)

```sql
SELECT name, price,
    price - (SELECT AVG(price) FROM products) AS diff_from_avg
FROM products;
```

### Табличный подзапрос в FROM

```sql
SELECT *
FROM (SELECT user_id, COUNT(*) AS cnt FROM orders GROUP BY user_id) AS user_stats
WHERE cnt > 5;
```

### Подзапрос в WHERE

```sql
-- IN — проверка множества
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 1000);

-- EXISTS — проверка существования (часто эффективнее IN)
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.total > 1000);
```

### Коррелированный подзапрос

Подзапрос ссылается на внешний запрос (выполняется для каждой строки):

```sql
SELECT name, salary
FROM employees e
WHERE salary > (SELECT AVG(salary) FROM employees WHERE dept_id = e.dept_id);
```

## IN vs EXISTS vs JOIN

Для проверки наличия записей в другой таблице:

- **IN**: для маленького фиксированного списка
- **EXISTS**: для проверки существования — обычно быстрее IN с большим подзапросом (может остановиться на первом совпадении)
- **JOIN**: когда нужны данные из второй таблицы. Для EXISTS/JOIN на больших таблицах часто JOIN с GROUP BY + HAVING

## Антипаттерны

- **Неявный JOIN**: трудно читать, легко получить CROSS JOIN
- **RIGHT JOIN**: используй LEFT — читается естественнее
- **NATURAL JOIN**: если схема изменится — JOIN сломается молча
- **Коррелированные подзапросы на миллионах строк**: замени на JOIN или оконные функции

## Связанные страницы

- [[../04-sql/sql-basics|SQL — Основы]]
- [[../04-sql/set-operations|Операции над множествами]]
- [[../04-sql/sql-performance|Практическая оптимизация SQL]]
