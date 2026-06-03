# ML-таксономия

## Три парадигмы

```
ML
├── Supervised (с учителем)    — есть X и y (ответы)
├── Unsupervised (без учителя)  — есть только X
└── Reinforcement (с подкреплением) — агент, среда, награды
```

| | Supervised | Unsupervised | Reinforcement |
|---|---|---|---|
| **Данные** | (X, y) — пары вход-выход | Только X | Состояния, действия, награды |
| **Цель** | Предсказать y для новых X | Найти структуру в X | Максимизировать награду |
| **Примеры** | Прогноз цены, классификация | Кластеризация, PCA | Игры, роботы, рекомендации |

## Supervised Learning

### Регрессия (y — непрерывная)

- Linear Regression, Ridge, Lasso
- Decision Tree, Random Forest
- Gradient Boosting (XGBoost, LightGBM, CatBoost)
- SVR, KNN

### Классификация (y — категориальная)

- Логистическая регрессия
- Деревья и ансамбли
- SVM
- Наивный Байес

### Метрики

См. [[../09-machine-learning/model-evaluation|Оценка моделей]].

## Unsupervised Learning

### Кластеризация

- K-Means, DBSCAN, HDBSCAN
- Иерархическая кластеризация
- Gaussian Mixture Models

См. [[../09-machine-learning/unsupervised-learning|Обучение без учителя]].

### Снижение размерности

- PCA, t-SNE, UMAP
- Factor Analysis, NMF

## Reinforcement Learning

Вне фокуса этой вики (редко используется в классическом анализе данных). Применяется в робототехнике, играх, управлении.

## Когда какой метод

```
Есть размеченные данные (y)?
├── Да → Supervised
│   ├── y — число → Регрессия
│   └── y — категория → Классификация
└── Нет → Unsupervised
    ├── Ищем группы → Кластеризация
    └── Визуализация/сжатие → PCA, t-SNE
```

## Связанные страницы

- [[../09-machine-learning/supervised-learning|Обучение с учителем]]
- [[../09-machine-learning/unsupervised-learning|Обучение без учителя]]
- [[../09-machine-learning/ml-vs-statistics|ML vs Статистика]]
