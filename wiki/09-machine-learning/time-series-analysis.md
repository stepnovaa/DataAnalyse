# Временные ряды

## Что такое временной ряд

Данные, упорядоченные во времени: цена акции, дневная выручка, температура. Ключевое отличие от обычных данных — **зависимость наблюдений** (автокорреляция).

## Декомпозиция

Любой временной ряд можно представить как:

```
Y(t) = Trend + Seasonality + Residual
```

```python
from statsmodels.tsa.seasonal import seasonal_decompose
decomp = seasonal_decompose(df['value'], model='additive', period=365)
decomp.plot()
```

- **Trend** — долгосрочное направление (рост, падение)
- **Seasonality** — повторяющиеся паттерны (день недели, месяц, квартал)
- **Residual** — то, что осталось (шум)

## Стационарность

Ряд **стационарен**, если его статистические свойства (среднее, дисперсия) не меняются со временем. Многие модели требуют стационарности.

### Проверка (ADF test)

```python
from statsmodels.tsa.stattools import adfuller
p_value = adfuller(df['value'])[1]
# p < 0.05 → ряд стационарен
```

### Как сделать стационарным

- **Дифференцирование**: `df['diff'] = df['value'].diff()`
- **Логарифмирование + diff**: для данных с растущей дисперсией
- **Удаление тренда/сезонности**

## Модели прогнозирования

### Наивные (Baseline)

- **Среднее историческое**: ŷ(t+1) = mean(y)
- **Последнее значение**: ŷ(t+1) = y(t)
- **Сезонный наив**: ŷ(t+1) = y(t - season + 1)

Всегда начинай с baseline. Если твоя сложная модель не бьёт «последнее значение» — что-то не так.

### ARIMA (AutoRegressive Integrated Moving Average)

```python
from statsmodels.tsa.arima.model import ARIMA
model = ARIMA(df['value'], order=(p, d, q))
model_fit = model.fit()
forecast = model_fit.forecast(steps=30)
```

- **p**: порядок авторегрессии (AR) — сколько прошлых значений используем
- **d**: порядок дифференцирования (I) — чтобы сделать ряд стационарным
- **q**: порядок скользящего среднего (MA) — сколько прошлых ошибок используем

### SARIMA (Seasonal ARIMA)

```python
model = ARIMA(df['value'], order=(1,1,1), seasonal_order=(1,1,1,12))
```

Добавляет сезонные компоненты. `seasonal_order=(P,D,Q,s)` где s = длина сезона (12 для месяцев, 7 для дней недели).

### Prophet (Facebook/Meta)

```python
from prophet import Prophet
model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
model.fit(df.rename(columns={'date': 'ds', 'value': 'y'}))
forecast = model.predict(model.make_future_dataframe(periods=30))
```

- Автоматически обрабатывает сезонность, праздники, пропуски
- Для бизнес-прогнозов с человеческой интерпретацией
- Не для высокочастотных или нестабильных рядов

## Метрики для временных рядов

```python
from sklearn.metrics import mean_absolute_percentage_error
mape = mean_absolute_percentage_error(y_true, y_pred)
```

- **MAE / RMSE** — абсолютная ошибка
- **MAPE** — ошибка в процентах
- **SMAPE** — симметричная MAPE (лучше когда y≈0)

## Особенности ML для временных рядов

- **НЕ используй случайный train/test split!** Временной порядок важен.
- Используй **TimeSeriesSplit** (последовательные блоки):

```python
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)
```

- **Лаговые признаки**: добавь значения t-1, t-2, t-7 как фичи
- **Скользящие окна**: среднее за последние 7 дней

## Связанные страницы

- [[../09-machine-learning/supervised-learning|Обучение с учителем]] — лаговые признаки превращают ряд в supervised
- [[../02-statistics/descriptive-statistics|Описательная статистика]]
- [[../09-machine-learning/model-evaluation|Оценка моделей]]
