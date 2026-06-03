# Проектирование признаков (Feature Engineering)

## Что это

Превращение сырых данных в признаки (features), которые модель может использовать. Часто важнее выбора модели.

> «Applied ML is basically feature engineering.» — Andrew Ng

## Для числовых признаков

### Масштабирование

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# StandardScaler: (x - mean) / std → μ=0, σ=1
# Для: линейной регрессии, SVM, PCA, нейросетей

# MinMaxScaler: (x - min) / (max - min) → [0, 1]
# Для: когда нужен фиксированный диапазон, нейросети

# RobustScaler: (x - median) / IQR → устойчив к выбросам
# Для: данных с выбросами
```

### Трансформации

```python
# Log: для данных с правым скосом (доходы, цены)
np.log1p(df['price'])

# Box-Cox: автоматический подбор нормализующей трансформации
from scipy.stats import boxcox
df['price_boxcox'], lambda_ = boxcox(df['price'] + 1)

# Binning: непрерывное → категориальное
pd.cut(df['age'], bins=[0, 18, 35, 60, 100], labels=['child', 'young', 'adult', 'senior'])
```

### Полиномиальные признаки

```python
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(df[['x1', 'x2']])
# x1, x2 → x1, x2, x1^2, x1*x2, x2^2
```

Добавляет нелинейность в линейные модели. Осторожно: экспоненциальный рост числа признаков.

## Для категориальных признаков

### One-Hot Encoding

```python
pd.get_dummies(df['country'], prefix='country')
# country=RU → country_RU=1, country_US=0, country_CN=0
```

**Минусы**: высокая размерность (N категорий → N колонок). Плохо для высокой кардинальности.

### Label Encoding

```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['country_encoded'] = le.fit_transform(df['country'])
```

**Опасно** для нелинейных моделей: они подумают что RU (0) < US (1) < CN (2). Используй только для tree-based моделей.

### Target Encoding

```python
# Среднее target по категории
means = df.groupby('country')['target'].mean()
df['country_target_enc'] = df['country'].map(means)
```

Мощно, но легко получить overfitting. Всегда со сглаживанием и кросс-валидацией.

### Frequency Encoding

```python
freq = df['country'].value_counts(normalize=True)
df['country_freq'] = df['country'].map(freq)
```

### Count Encoding

```python
df['country_count'] = df['country'].map(df['country'].value_counts())
```

## Для дат и времени

```python
df['hour'] = df['timestamp'].dt.hour
df['day_of_week'] = df['timestamp'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
df['quarter'] = df['timestamp'].dt.quarter
df['days_since_start'] = (df['timestamp'] - df['timestamp'].min()).dt.days

# Циклическое кодирование (чтобы 23:00 и 00:00 были рядом)
df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
```

## Для текста

```python
# Длина текста
df['text_len'] = df['text'].str.len()
df['word_count'] = df['text'].str.split().str.len()

# Ключевые слова (бинарные флаги)
df['has_discount'] = df['text'].str.contains('скидка|акция', case=False).astype(int)

# TF-IDF (для ML)
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features=1000)
X_text = tfidf.fit_transform(df['text'])
```

## Автоматический Feature Engineering

- **Featuretools**: Deep Feature Synthesis — автоматически генерирует признаки из реляционных данных
- **AutoFeat**: автоматический отбор и генерация признаков
- **tsfresh**: 1200+ признаков для временных рядов

## Лучшие практики

1. **Делай до train/test split** только fit на train, transform на test
2. **Проверяй утечку данных**: target encoding из всей выборки — утечка!
3. **Не бойся удалять признаки**: шумный признак хуже, чем его отсутствие
4. **Итеративно**: добавил признак → проверил метрику → оставил/удалил

## Связанные страницы

- [[../07-exploratory-analysis/univariate-analysis|Одномерный анализ]]
- [[../07-exploratory-analysis/missing-data-strategies|Стратегии работы с пропусками]]
- [[../09-machine-learning/supervised-learning|Обучение с учителем]]
