# Обучение без учителя (Unsupervised Learning)

## Зачем

Нет правильных ответов (y). Ищем скрытую структуру в данных.

## Кластеризация

### K-Means

```python
from sklearn.cluster import KMeans

# Подбор k через elbow method
inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X_scaled)
```

**Плюсы**: быстрый, масштабируется.
**Минусы**: надо знать k, предполагает сферические кластеры одинакового размера, чувствителен к выбросам.

### DBSCAN

```python
from sklearn.cluster import DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
clusters = dbscan.fit_predict(X_scaled)
# cluster = -1 → шум (не попал ни в один кластер)
```

**Плюсы**: не надо знать k, находит кластеры любой формы, находит шум.
**Минусы**: чувствителен к параметрам eps/min_samples, плохо с разной плотностью.

### HDBSCAN (улучшенный DBSCAN)

```python
import hdbscan
clusterer = hdbscan.HDBSCAN(min_cluster_size=10)
clusters = clusterer.fit_predict(X_scaled)
```

Устойчивее к параметрам, находит кластеры разной плотности.

### Оценка качества кластеризации

```python
from sklearn.metrics import silhouette_score
silhouette_score(X_scaled, clusters)
```

- Близко к +1: хорошая кластеризация
- Около 0: кластеры перекрываются
- Отрицательно: объекты в неправильных кластерах

## Снижение размерности

### PCA

```python
from sklearn.decomposition import PCA
pca = PCA(n_components=0.95)  # объяснить 95% дисперсии
X_pca = pca.fit_transform(X_scaled)

# Визуализация explained variance
plt.plot(np.cumsum(pca.explained_variance_ratio_))
```

**Когда использовать**:
- Уменьшить размерность перед ML
- Визуализировать в 2D/3D
- Убрать мультиколлинеарность

### t-SNE

```python
from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, perplexity=30)
X_tsne = tsne.fit_transform(X_scaled)
```

**Для визуализации**, не для уменьшения размерности перед ML. perplexity=5-50.

### UMAP

```python
import umap
reducer = umap.UMAP()
X_umap = reducer.fit_transform(X_scaled)
```

Быстрее t-SNE, лучше сохраняет глобальную структуру, можно для уменьшения размерности.

## Практический workflow

```python
# 1. Масштабировать
from sklearn.preprocessing import StandardScaler
X_scaled = StandardScaler().fit_transform(X)

# 2. PCA для визуализации
X_pca = PCA(n_components=2).fit_transform(X_scaled)

# 3. Кластеризация
clusters = HDBSCAN(min_cluster_size=10).fit_predict(X_scaled)

# 4. Профили кластеров
df['cluster'] = clusters
df.groupby('cluster').mean()
```

## Связанные страницы

- [[../07-exploratory-analysis/multivariate-analysis|Многомерный анализ]]
- [[../09-machine-learning/ml-taxonomy|ML-таксономия]]
- [[../09-machine-learning/supervised-learning|Обучение с учителем]]
