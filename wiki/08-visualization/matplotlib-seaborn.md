# Matplotlib + Seaborn

## Matplotlib — фундамент

Библиотека для статической визуализации в Python. Низкоуровневая, гибкая, многословная.

### Два подхода

```python
import matplotlib.pyplot as plt

# 1. Pyplot (stateful) — быстро, но меньше контроля
plt.plot(x, y)
plt.title('Title')
plt.show()

# 2. Object-oriented — для сложных графиков
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y)
ax.set_title('Title')
plt.show()
```

### Базовые типы

```python
ax.plot(x, y)           # линия
ax.scatter(x, y)        # точки
ax.bar(x, height)       # столбцы
ax.barh(y, width)       # горизонтальные столбцы
ax.hist(data, bins=30)  # гистограмма
ax.boxplot(data)        # boxplot
```

### Настройка

```python
fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
ax.plot(x, y, color='#2196f3', linewidth=2, linestyle='--', marker='o')
ax.set_xlabel('X Label', fontsize=12)
ax.set_ylabel('Y Label')
ax.set_title('Title', fontweight='bold', fontsize=14)
ax.legend(['Series 1'], loc='upper left')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('chart.png', dpi=150, bbox_inches='tight')
```

## Seaborn — статистическая визуализация

Seaborn надстройка над matplotlib: красивые дефолты, высокоуровневые статистические графики.

### Почему Seaborn

- **Стиль из коробки**: `sns.set_theme()` — и уже красиво
- **Интеграция с Pandas**: колонки передаются по именам
- **Статистика «из коробки»**: доверительные интервалы, регрессии

### Основные графики

```python
import seaborn as sns

# Распределения
sns.histplot(df['price'], bins=50, kde=True)
sns.kdeplot(df['price'], fill=True)

# Связи
sns.scatterplot(data=df, x='price', y='sales', hue='category')
sns.lineplot(data=df, x='date', y='revenue', hue='product')
sns.regplot(data=df, x='price', y='sales')  # + линия регрессии

# Категориальные
sns.boxplot(data=df, x='category', y='price')
sns.violinplot(data=df, x='category', y='price')
sns.barplot(data=df, x='category', y='price')  # + доверительный интервал
sns.countplot(data=df, x='category')

# Матрицы
sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
sns.clustermap(df.corr())  # + дендрограмма

# Множественные
sns.pairplot(df, hue='category')
sns.jointplot(data=df, x='price', y='sales', kind='hex')
```

### Стилизация

```python
sns.set_theme(style='whitegrid', palette='muted', font_scale=1.2)
# Стили: darkgrid, whitegrid, dark, white, ticks
# Палитры: deep, muted, pastel, bright, dark, colorblind
```

## Рецепты

### Вертикальная линия (аннотация)

```python
ax.axvline(x=threshold, color='red', linestyle='--', alpha=0.7, label='Target')
```

### Две шкалы Y (осторожно!)

```python
ax2 = ax.twinx()
ax2.plot(x, y2, color='red')
```

### Сохранение с прозрачностью

```python
plt.savefig('chart.png', transparent=True, dpi=200, bbox_inches='tight')
```

## Связанные страницы

- [[../08-visualization/plotly-interactive|Plotly — интерактивная визуализация]]
- [[../08-visualization/chart-chooser|Выбор графика]]
- [[../08-visualization/color-and-accessibility|Цвет и доступность]]
