# Кейс: Атрибуция маркетинга

## Бизнес-контекст

Пользователь видит баннер в Instagram → гуглит бренд → кликает по поисковой рекламе → заходит на сайт → через 3 дня получает email → покупает.

**Вопрос**: какому каналу «приписать» продажу?

## Модели атрибуции

### Last Click (последнее касание)

100% ценности → последнему каналу перед покупкой.

```sql
SELECT marketing_channel, SUM(revenue) AS attributed_revenue
FROM purchases
GROUP BY marketing_channel;
```

**Проблема**: игнорирует весь путь пользователя. Email получает всю атрибуцию — хотя он просто напомнил о бренде, который пользователь узнал из Instagram.

### First Click (первое касание)

100% ценности → первому каналу.

**Проблема**: игнорирует конвертирующие касания. Instagram получает всё — но без search ad пользователь бы не купил.

### Linear (равномерная)

Ценность делится поровну между всеми касаниями.

### Time Decay

Чем ближе касание к покупке — тем больше его вклад.

### Position-Based (U-Shaped)

40% первому, 40% последнему, 20% — остальным поровну.

### Data-Driven (алгоритмическая)

Shapley values или ML-модель оценивает вклад каждого канала на основе контрфактического анализа.

## Реализация (SQL)

```sql
-- Путь пользователя к покупке
SELECT
    user_id,
    purchase_id,
    ARRAY_AGG(marketing_channel ORDER BY touch_timestamp) AS touchpoints
FROM marketing_touches
WHERE user_id IN (SELECT user_id FROM purchases)
GROUP BY user_id, purchase_id;

-- Пример пути: ['instagram', 'google_search', 'email']
```

### Last Click в SQL

```sql
WITH last_touch AS (
    SELECT DISTINCT ON (user_id, purchase_id)
        user_id, purchase_id, marketing_channel
    FROM marketing_touches
    WHERE touch_type = 'conversion_assist'
    ORDER BY user_id, purchase_id, touch_timestamp DESC
)
SELECT marketing_channel, SUM(p.revenue) AS revenue
FROM last_touch lt
JOIN purchases p ON lt.purchase_id = p.id
GROUP BY marketing_channel;
```

### Linear в Python

```python
def linear_attribution(touchpoints, revenue):
    value_per_touch = revenue / len(touchpoints)
    return {channel: value_per_touch for channel in touchpoints}

# Пример: ['instagram', 'google_search', 'email'], revenue=1000
# → instagram: 333, google_search: 333, email: 333
```

## Сравнение моделей

| Канал | Last Click | First Click | Linear | Position-Based |
|-------|------------|-------------|--------|----------------|
| Instagram | 300 | 1800 | 600 | 800 |
| Google Search | 500 | 600 | 600 | 200 |
| Email | 1200 | 300 | 600 | 800 |

**Выводы зависят от модели!** Last Click переоценивает Email. First Click переоценивает Instagram. Position-Based — компромисс.

## Чему учит кейс

1. **Нет одной «правильной» модели** — выбор зависит от бизнес-вопроса
2. **Last Click — самый распространённый и самый плохой** (игнорирует верхние этапы воронки)
3. **Data-driven атрибуция** — золотой стандарт, но требует данных и ML
4. **Сравнивай модели**: если канал резко меняет эффективность при смене модели — атрибуция нестабильна

## Связанные страницы

- [[../04-sql/window-functions-advanced|Оконные функции]]
- [[../09-machine-learning/supervised-learning|Обучение с учителем]]
- [[../09-machine-learning/ml-vs-statistics|ML vs Статистика]]
