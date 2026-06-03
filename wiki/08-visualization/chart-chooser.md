# Выбор графика под задачу

## Дерево решений

```
Что нужно показать?
│
├── Сравнение величин
│   ├── Много категорий (≥ 5) → Горизонтальный bar chart
│   ├── Мало категорий → Вертикальный bar chart
│   └── Ранжирование → Dot plot
│
├── Изменение во времени
│   ├── Непрерывный тренд → Line chart
│   ├── Дискретные периоды → Bar chart
│   └── Циклический паттерн → Спиральный график / Seasonal plot
│
├── Распределение
│   ├── Одна переменная → Histogram / KDE
│   ├── Сравнение групп → Boxplot / Violin / Ridgeline
│   └── Сравнение с теоретическим → Q-Q plot
│
├── Связь между переменными
│   ├── Две числовые → Scatter plot (+ trend line)
│   ├── Три числовые → Bubble chart / 3D scatter (осторожно)
│   ├── Много числовых → Correlation heatmap / PCA plot
│   └── Числовая vs Категориальная → Boxplot / Violin / Bar
│
├── Часть от целого
│   ├── Простые доли → Stacked bar (100%)
│   ├── Иерархия → Treemap / Sunburst
│   └── НЕ ИСПОЛЬЗУЙ → Pie chart (кроме 2-3 категорий с сильным контрастом)
│
├── Геопространственные данные
│   ├── Регионы → Choropleth map
│   ├── Точки → Scatter map
│   └── Плотность → Heatmap map
│
└── Потоки и связи
    ├── Направленные → Sankey diagram
    ├── Сеть → Node-link diagram
    └── Матрица → Heatmap
```

## Графики-антипаттерны

### Pie Chart

- Человек плохо сравнивает углы и площади
- > 3 секторов = нечитаемо
- Всегда можно заменить на bar chart

**Единственный случай**: 2-3 категории с очевидным контрастом (75% / 25%). И то — горизонтальный bar лучше.

### 3D-графики

- Искажают восприятие (перспектива обманывает)
- Передние объекты загораживают задние
- Угол обзора меняет восприятие величин

> Никаких 3D pie charts. Никогда.

### Двойная ось Y

- Можно подогнать масштаб под любой «нужный» вывод
- Разные единицы на одной шкале
- Если очень надо — используй faceting

## Quick Reference (шпаргалка)

```
Данные               →  График            →  Python
─────────────────────────────────────────────────────
Одна числовая        →  Histogram         →  plt.hist() / sns.histplot()
Одна категориальная  →  Countplot         →  sns.countplot()
Число × Время        →  Line              →  sns.lineplot()
Число × Категория    →  Boxplot           →  sns.boxplot()
Число × Число        →  Scatter           →  sns.scatterplot()
Катег. × Катег.      →  Heatmap           →  sns.heatmap()
Катег. × Катег.      →  Stacked bar       →  df.plot.bar(stacked=True)
Много числовых       →  Pairplot          →  sns.pairplot()
Гео                  →  Choropleth        →  px.choropleth()
```

## Связанные страницы

- [[../08-visualization/viz-grammar-and-theory|Грамматика графики]]
- [[../08-visualization/matplotlib-seaborn|Matplotlib + Seaborn]]
- [[../08-visualization/plotly-interactive|Plotly]]
