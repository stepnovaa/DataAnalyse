# Многомерный анализ

## Что это

Анализ взаимодействия **трёх и более** переменных. Когда двумерных связей недостаточно.

## Матрица корреляций

```python
# Heatmap
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)

# Или через mask для треугольной матрицы
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True)
```

Ищи:
- Сильные корреляции (>0.7) между предикторами → мультиколлинеарность
- Сильные корреляции с target → потенциально важные фичи

## Многомерная визуализация

### Цвет как третье измерение

```python
sns.scatterplot(data=df, x='price', y='sales', hue='category', size='quantity')
```

### FacetGrid (матрица графиков)

```python
g = sns.FacetGrid(df, col='country', row='year', hue='category')
g.map(sns.scatterplot, 'price', 'sales')
```

### Параллельные координаты

```python
from pandas.plotting import parallel_coordinates
parallel_coordinates(df[['category', 'price', 'sales', 'rating']], 'category')
```

Хорошо для сравнения профилей категорий по нескольким осям.

## Снижение размерности

### PCA (Principal Component Analysis)

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

X_scaled = StandardScaler().fit_transform(df[numeric_cols])
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Визуализация
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['target'])
print(f'Explained variance: {pca.explained_variance_ratio_}')
```

Используй PCA для:
- Визуализации высокоразмерных данных в 2D/3D
- Обнаружения кластеров (глазами)
- Уменьшения размерности перед ML

### t-SNE (для визуализации)

```python
from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_tsne = tsne.fit_transform(X_scaled)
```

t-SNE лучше PCA для визуализации кластеров, но:
- Медленный на больших данных (>5000 точек)
- Не сохраняет расстояния глобально (только локальную структуру)
- Не для уменьшения размерности перед ML!

## Кластеризация как инструмент EDA

```python
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4)
df['cluster'] = kmeans.fit_predict(X_scaled)

# Профили кластеров
df.groupby('cluster')[numeric_cols].mean()
```

Используй кластеризацию в EDA чтобы:
- Найти естественные группы в данных
- Понять, есть ли сегменты пользователей/товаров

## Продвинутые техники

### Взаимодействия признаков

```python
# Явное создание взаимодействий
df['price_x_quantity'] = df['price'] * df['quantity']

# Проверка значимости через регрессию
import statsmodels.api as sm
X = sm.add_constant(df[['price', 'quantity', 'price_x_quantity']])
model = sm.OLS(df['sales'], X).fit()
```

### VIF (Variance Inflation Factor) — мультиколлинеарность

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame({
    'feature': X.columns,
    'VIF': [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
})
# VIF > 5-10 → проблема
```

## Связанные страницы

- [[../07-exploratory-analysis/bivariate-analysis|Двумерный анализ]]
- [[../07-exploratory-analysis/feature-engineering|Проектирование признаков]]
- [[../09-machine-learning/unsupervised-learning|Обучение без учителя]]
