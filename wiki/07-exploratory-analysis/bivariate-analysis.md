# Двумерный анализ

## Что это

Анализ связи между **двумя** переменными. Отвечает на вопрос: «Как X и Y связаны?»

## Числовая vs Числовая

### Корреляция

```python
# Пирсон (линейная)
df[['price', 'quantity']].corr()

# Спирмен (монотонная)
df[['price', 'quantity']].corr(method='spearman')
```

См. [[../02-statistics/correlation-and-regression|Корреляция и регрессия]].

### Scatter plot

```python
import seaborn as sns
sns.scatterplot(data=df, x='price', y='sales', alpha=0.5)
```

Ищи:
- Линейную зависимость
- Нелинейные паттерны (U-образная, экспонента)
- Гетероскедастичность (разброс меняется с X)
- Кластеры

### Hexbin (для больших данных)

```python
df.plot.hexbin(x='x', y='y', gridsize=30)
```

Когда scatter plot превращается в чёрное пятно — hexbin показывает плотность.

## Числовая vs Категориальная

### Boxplot / Violin plot

```python
sns.boxplot(data=df, x='category', y='price')
sns.violinplot(data=df, x='category', y='price')
```

Что искать: разница медиан, разброс, выбросы в категориях.

### Агрегация

```python
df.groupby('category')['price'].agg(['mean', 'median', 'std', 'count'])
```

### Статистический тест

```python
from scipy.stats import f_oneway
# ANOVA: различаются ли средние по категориям?
groups = [g['price'].dropna() for _, g in df.groupby('category')]
f_stat, p_value = f_oneway(*groups)
```

## Категориальная vs Категориальная

### Кросстаб (таблица сопряжённости)

```python
pd.crosstab(df['country'], df['status'], normalize='index')
```

### Heatmap

```python
sns.heatmap(pd.crosstab(df['country'], df['status']), annot=True, fmt='d')
```

### Хи-квадрат тест

```python
from scipy.stats import chi2_contingency
ct = pd.crosstab(df['cat1'], df['cat2'])
chi2, p, dof, expected = chi2_contingency(ct)
```

## EDA-матрица (сводка)

```
Типы пар         →  Метод              →  Визуализация
─────────────────────────────────────────────────────
Число × Число    →  Корреляция         →  Scatter / Hexbin
Число × Катег.   →  Агрегация, ANOVA   →  Boxplot / Violin
Катег. × Катег.  →  Кросстаб, χ²       →  Heatmap / Stacked bar
```

## Pairplot — всё сразу

```python
sns.pairplot(df[['price', 'quantity', 'age', 'category']], hue='category')
```

Для быстрого обзора связей между 3-5 ключевыми переменными. На больших датасетах — на сэмпле.

## Связанные страницы

- [[../07-exploratory-analysis/univariate-analysis|Одномерный анализ]]
- [[../07-exploratory-analysis/multivariate-analysis|Многомерный анализ]]
- [[../02-statistics/correlation-and-regression|Корреляция и регрессия]]
