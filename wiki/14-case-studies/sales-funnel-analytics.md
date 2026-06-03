# Кейс: Воронка продаж

## Бизнес-контекст

E-commerce. Нужно проанализировать воронку продаж: от входа на сайт до покупки. Найти где отваливаются пользователи и как это чинить.

## Данные

```sql
-- events: пользовательские события
-- columns: user_id, event_type, timestamp, session_id
-- event_type: page_view, product_view, add_to_cart, checkout_start, purchase
```

## Этап 1: Воронка конверсий

```sql
WITH funnel AS (
    SELECT
        COUNT(DISTINCT CASE WHEN event_type = 'page_view' THEN user_id END) AS visitors,
        COUNT(DISTINCT CASE WHEN event_type = 'product_view' THEN user_id END) AS viewed_product,
        COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN user_id END) AS added_to_cart,
        COUNT(DISTINCT CASE WHEN event_type = 'checkout_start' THEN user_id END) AS started_checkout,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) AS purchased
    FROM events
    WHERE event_date = CURRENT_DATE - 1
)
SELECT
    visitors,
    viewed_product,
    added_to_cart,
    started_checkout,
    purchased,
    ROUND(viewed_product * 100.0 / visitors, 1) AS view_rate,
    ROUND(added_to_cart * 100.0 / viewed_product, 1) AS cart_rate,
    ROUND(started_checkout * 100.0 / added_to_cart, 1) AS checkout_rate,
    ROUND(purchased * 100.0 / started_checkout, 1) AS purchase_rate
FROM funnel;
```

```
visitors  viewed  cart   checkout  purchased
10000     4500    1200   800       320

view_rate:  45.0%   ← посмотрели товар
cart_rate:  26.7%   ← добавили в корзину
checkout:   66.7%   ← начали оформление
purchase:   40.0%   ← купили (от начавших оформление)

Общая конверсия: 3.2% (320 / 10000)
```

**Главный инсайт**: 66.7% корзины уходят в checkout, но только 40% checkout → purchase. Проблема на этапе оформления!

## Этап 2: Где отваливаются в checkout?

```sql
-- На каком шаге checkout отваливаются?
SELECT checkout_step, COUNT(*) AS reached, COUNT(*) FILTER (WHERE next_step IS NULL) AS dropped
FROM (
    SELECT user_id, session_id, checkout_step,
        LEAD(checkout_step) OVER (PARTITION BY user_id, session_id ORDER BY timestamp) AS next_step
    FROM checkout_events
) t
GROUP BY checkout_step
ORDER BY checkout_step;
```

```
checkout_step          | reached | dropped | drop_rate
────────────────────────────────────────────────────
1. address_form        | 800     | 120     | 15.0%
2. delivery_choice     | 680     | 80      | 11.8%
3. payment             | 600     | 160     | 26.7%  ← ОСНОВНАЯ ТОЧКА ОТВАЛА
4. confirmation        | 440     | 120     | 27.3%
```

Шаг «payment» и «confirmation» — главные точки отвала. Гипотезы:
- Нет удобного способа оплаты (нет Apple Pay / СБП)
- Скрытые комиссии / стоимость доставки показываются поздно

## Этап 3: Когортный анализ конверсии

```sql
-- Конверсия по недельным когортам (cohort = неделя первого визита)
WITH first_visit AS (
    SELECT user_id, DATE_TRUNC('week', MIN(event_date)) AS cohort
    FROM events GROUP BY user_id
),
cohort_metrics AS (
    SELECT fv.cohort, COUNT(*) AS users,
        COUNT(DISTINCT CASE WHEN e.event_type = 'purchase' AND
            e.event_date <= fv.cohort + INTERVAL '7 days' THEN e.user_id END) AS converted
    FROM first_visit fv
    LEFT JOIN events e ON fv.user_id = e.user_id
    GROUP BY fv.cohort
)
SELECT cohort, users, converted, ROUND(converted * 100.0 / users, 1) AS conv_rate
FROM cohort_metrics ORDER BY cohort;
```

## Этап 4: A/B-тест

Гипотеза: добавление Apple Pay на этапе payment увеличит конверсию checkout → purchase на 10 п.п.

**MDE**: +10 п.п. (от 40% до 50%)
**Размер выборки**: ~400/группу (расчёт через statsmodels)

Результат через 2 недели:
- Контроль (без Apple Pay): 41%
- Вариант (с Apple Pay): 48%
- p-value: 0.03 → ✅ Значимо

## Рекомендации

1. **Добавить Apple Pay / Google Pay / СБП** на шаг payment (ожидаемый эффект +7 п.п. конверсии)
2. **Показывать полную стоимость ДО checkout** (скрытые комиссии → отвал)
3. **Упростить форму address** (15% отвала на первом шаге — много)

## Чему учит кейс

1. **Воронка в SQL**: COUNT DISTINCT + CASE — простой и мощный паттерн
2. **Главный вопрос не «сколько», а «где»**: не просто «конверсия 3.2%», а «где именно отваливаются»
3. **Когортный анализ**: смотреть не только абсолютные цифры, но и динамику по когортам
4. **A/B-тест подтверждает гипотезу**: сначала анализ → гипотеза → эксперимент

## Связанные страницы

- [[../04-sql/window-functions-advanced|Оконные функции]]
- [[../04-sql/advanced-sql-patterns|Продвинутые SQL-паттерны]]
- [[../02-statistics/ab-testing|A/B-тестирование]]
