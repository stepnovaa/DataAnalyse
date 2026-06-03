# Одномерный анализ

## Что это

Анализ каждой переменной по отдельности. Ответ на вопрос: «Что из себя представляет эта колонка?»

## Для числовых переменных

### Центральные метрики

```python
df['price'].mean()     # среднее
df['price'].median()   # медиана
df['price'].mode()     # мода
```

### Разброс

```python
df['price'].std()      # стандартное отклонение
df['price'].var()      # дисперсия
df['price'].quantile([0.25, 0.75])  # квартили
df['price'].skew()     # скос
df['price'].kurtosis() # эксцесс
```

### Обнаружение выбросов

```python
# IQR
Q1, Q3 = df['price'].quantile([0.25, 0.75])
IQR = Q3 - Q1
lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
outliers = df[(df['price'] < lower) | (df['price'] > upper)]

# Z-score
from scipy import stats
z = stats.zscore(df['price'].dropna())
outliers = df[np.abs(z) > 3]
```

### Визуализация

- **Гистограмма**: форма распределения, скос, модальность
- **Boxplot**: медиана, IQR, выбросы
- **KDE (Kernel Density Estimate)**: сглаженная оценка плотности
- **QQ-plot**: сравнение с теоретическим распределением

### Нужна ли трансформация?

Признаки того, что нужна нормализация:
- Сильный скос (skew > 1)
- Модель предполагает нормальность (линейная регрессия)
- Разные масштабы (для distance-based моделей)

```python
# Log-трансформация (для положительных значений с правым скосом)
df['price_log'] = np.log1p(df['price'])

# Box-Cox (λ подбирается автоматически)
from scipy.stats import boxcox
df['price_boxcox'], lambda_ = boxcox(df['price'] + 1)
```

## Для категориальных переменных

### Частоты

```python
df['category'].value_counts()             # абсолютные
df['category'].value_counts(normalize=True)  # доли
df['category'].value_counts().plot.bar()  # bar chart
```

### Кардинальность

```python
df['category'].nunique()  # сколько уникальных значений
```

Высокая кардинальность (>50 категорий): думай об объединении редких категорий в «Other».

### Проблемы

- **Дисбаланс**: одна категория 95%, остальные 5% — может быть проблемой для ML
- **Редкие категории**: <1% выборки — объединить
- **Опечатки**: `'Male'` vs `'male'` vs `'M'` — нормализовать

## Для дат и времени

```python
df['date'].min(), df['date'].max()  # диапазон
df['date'].value_counts().resample('M').sum()  # по месяцам
df['date'].dt.dayofweek.value_counts()  # по дням недели
```

Ищи:
- **Пропуски дат**: нет данных за выходные? праздники?
- **Сезонность**: дневная, недельная, годовая
- **Аномалии**: даты в будущем, 1900-01-01 (значение по умолчанию)

## Экспресс-профиль

```python
def univariate_profile(df, col):
    if df[col].dtype in ('int64', 'float64'):
        return {
            'dtype': df[col].dtype,
            'missing': df[col].isnull().sum(),
            'missing_pct': df[col].isnull().mean(),
            'mean': df[col].mean(),
            'median': df[col].median(),
            'std': df[col].std(),
            'skew': df[col].skew(),
            'min': df[col].min(),
            'max': df[col].max(),
            'nunique': df[col].nunique(),
        }
    else:
        return {
            'dtype': df[col].dtype,
            'missing': df[col].isnull().sum(),
            'nunique': df[col].nunique(),
            'top': df[col].value_counts().head(5).to_dict()
        }
```

## Связанные страницы

- [[../02-statistics/descriptive-statistics|Описательная статистика]]
- [[../07-exploratory-analysis/bivariate-analysis|Двумерный анализ]]
- [[../07-exploratory-analysis/feature-engineering|Проектирование признаков]]
