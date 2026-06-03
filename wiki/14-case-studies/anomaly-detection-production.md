# Кейс: Поиск аномалий в продакшне

## Бизнес-контекст

Интернет-магазин. Нужно автоматически обнаруживать аномалии в метриках и присылать алерты. Метрика: количество заказов в час.

## Этап 1: Понимание нормального поведения

```sql
-- Распределение заказов по часам за последние 30 дней
SELECT
    EXTRACT(HOUR FROM created_at) AS hour,
    AVG(order_count) AS avg_orders,
    STDDEV(order_count) AS std_orders
FROM (
    SELECT DATE_TRUNC('hour', created_at) AS hour_bucket, COUNT(*) AS order_count
    FROM orders
    WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY 1
) hourly
GROUP BY hour
ORDER BY hour;
```

## Этап 2: Простой метод — Z-score

```python
# Z-score: на сколько стандартных отклонений текущее значение отличается от среднего?
def detect_anomaly_zscore(current_value, historical_values):
    mean = np.mean(historical_values)
    std = np.std(historical_values)
    z = (current_value - mean) / std

    if abs(z) > 3:
        return 'anomaly', z
    elif abs(z) > 2:
        return 'warning', z
    else:
        return 'normal', z

# historical_values = значения за этот день недели + час за последние 8 недель
```

**Плюсы**: просто, быстро, объяснимо.
**Минусы**: предполагает нормальное распределение, чувствителен к выбросам в истории.

## Этап 3: Устойчивый метод — IQR + сезонность

```python
def detect_anomaly_iqr(current_value, historical_values):
    q1, q3 = np.percentile(historical_values, [25, 75])
    iqr = q3 - q1
    lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr

    if current_value < lower or current_value > upper:
        severity = 'high' if (current_value - upper) / iqr > 2 else 'medium'
        return 'anomaly', severity, current_value
    return 'normal', None, current_value
```

Устойчив к выбросам, но может не заметить постепенный дрейф.

## Этап 4: Скользящее среднее + контрольные границы

```python
# Экспоненциальное скользящее среднее
df['ewma'] = df['orders'].ewm(span=24).mean()     # 24 часа
df['ewm_std'] = df['orders'].ewm(span=24).std()

# Контрольные границы: EWMA ± 3 * EWM_STD
df['upper'] = df['ewma'] + 3 * df['ewm_std']
df['lower'] = df['ewma'] - 3 * df['ewm_std']
df['anomaly'] = (df['orders'] > df['upper']) | (df['orders'] < df['lower'])
```

Адаптируется к тренду и сезонности. Хорошо для плавно меняющихся метрик.

## Этап 5: Production-ready система

```python
import schedule
import requests

def check_and_alert():
    current = get_current_order_count()
    history = get_historical_values(hour=now.hour, weekday=now.weekday())

    status, detail = detect_anomaly_iqr(current, history)

    if status == 'anomaly':
        message = f'ALERT: Orders {detail}xIQR from normal'
        if detail.startswith('high') and current < history.mean():
            message += ' (drop!)'  # падение заказов — критично
        send_telegram_alert(message)

schedule.every(5).minutes.do(check_and_alert)
```

## Чему учит кейс

1. **Контекст важнее алгоритма**: падение заказов в 3 часа ночи на 50% — норма. Днём — аномалия.
2. **Несколько методов**: Z-score для быстрой проверки, IQR для устойчивости, EWMA для трендов
3. **Сезонность — ключ**: день недели, час, праздники — без них любой метод будет орать по выходным
4. **Алерт должен быть actionable**: «аномалия» без контекста бесполезна. Добавь: величина, направление, возможная причина

## Связанные страницы

- [[../02-statistics/descriptive-statistics|Описательная статистика]]
- [[../09-machine-learning/time-series-analysis|Временные ряды]]
- [[../04-sql/window-functions-advanced|Оконные функции]]
