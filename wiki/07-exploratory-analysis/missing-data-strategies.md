# Стратегии работы с пропусками

## Диагностика

```python
# Сколько пропущено?
df.isnull().sum()
df.isnull().mean() * 100  # в процентах

# Паттерн пропусков
import missingno as msno
msno.matrix(df)     # матрица пропусков
msno.heatmap(df)    # корреляции пропусков между колонками
msno.dendrogram(df) # иерархическая кластеризация пропусков
```

## Три механизма пропусков (Rubin, 1976)

| Механизм | Описание | Пример |
|----------|----------|--------|
| **MCAR** (Completely At Random) | Пропуск не зависит ни от чего | Датчик случайно не сработал |
| **MAR** (At Random) | Пропуск зависит от других переменных | Женщины реже указывают возраст |
| **MNAR** (Not At Random) | Пропуск зависит от самого значения | Люди с высоким доходом скрывают доход |

> MNAR — самый опасный. Нельзя просто заполнить средним — получишь смещённую оценку.

## Стратегии

### 1. Удаление

```python
# Удалить строки с любыми пропусками
df.dropna()

# Удалить строки, где пропущен target
df.dropna(subset=['target'])

# Удалить колонки с >50% пропусков
threshold = len(df) * 0.5
df.dropna(axis=1, thresh=threshold)
```

**Когда**: MCAR, мало пропусков (<5%), колонка не критичная.

### 2. Заполнение константой

```python
# Для чисел
df['age'].fillna(-1)
df['age'].fillna(df['age'].median())

# Для категорий
df['country'].fillna('Unknown')
df['country'].fillna(df['country'].mode()[0])
```

**Плюсы**: просто.
**Минусы**: искажает распределение, занижает дисперсию.

### 3. Заполнение средним/медианой/модой

```python
df['age'].fillna(df['age'].mean())    # среднее
df['age'].fillna(df['age'].median())  # медиана (лучше при выбросах)
```

### 4. Forward/Backward fill (для временных рядов)

```python
df['sensor'].fillna(method='ffill')  # предыдущее значение
df['sensor'].fillna(method='bfill')  # следующее значение
```

### 5. Интерполяция

```python
df['sensor'].interpolate(method='linear')     # линейная
df['sensor'].interpolate(method='spline', order=3)  # сплайн
```

Для временных рядов с плавным изменением.

### 6. KNN Imputation

```python
from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=5)
df_filled = imputer.fit_transform(df)
```

Заполняет на основе похожих строк. Медленно на больших данных.

### 7. MICE (Multiple Imputation)

```python
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
imputer = IterativeImputer(max_iter=10, random_state=42)
df_filled = imputer.fit_transform(df)
```

Итеративно предсказывает пропуски, используя другие колонки как предикторы.

### 8. Индикатор пропуска

```python
df['age_missing'] = df['age'].isnull().astype(int)
df['age'].fillna(df['age'].median(), inplace=True)
```

Иногда сам факт пропуска — информативный признак (люди, не указавшие доход, ведут себя иначе).

## Выбор стратегии

| Ситуация | Стратегия |
|----------|-----------|
| <5% пропусков, MCAR | Удаление строк |
| 5-20%, колонка важная | Медиана / MICE |
| >50% в колонке | Удалить колонку (или индикатор) |
| Временной ряд | Forward fill / Интерполяция |
| MNAR | Индикатор пропуска + обсудить с domain expert |

## Золотое правило

**Не заполняй пропуски до train/test split!** Иначе test данные «подсмотрят» статистики train → data leakage.

```python
# Правильно
X_train, X_test = train_test_split(df)
median = X_train['age'].median()
X_train['age'].fillna(median, inplace=True)
X_test['age'].fillna(median, inplace=True)
```

## Связанные страницы

- [[../06-data-processing/data-cleaning|Очистка данных]]
- [[../07-exploratory-analysis/univariate-analysis|Одномерный анализ]]
- [[../07-exploratory-analysis/feature-engineering|Проектирование признаков]]
