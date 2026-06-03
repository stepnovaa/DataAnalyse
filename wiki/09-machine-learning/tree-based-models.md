# Деревья и ансамбли

## Почему деревья

Деревья решений и ансамбли на их основе — самые популярные модели для табличных данных. Они выигрывают большинство Kaggle-соревнований и production-задач.

## Decision Tree (база)

```python
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
tree = DecisionTreeClassifier(max_depth=5)
tree.fit(X_train, y_train)
```

**Плюсы**: интерпретируемость, не требует масштабирования, работает с категориальными.
**Минусы**: склонность к overfitting, нестабильность (малое изменение данных → другое дерево).

## Ансамбли

Идея: объединить много слабых моделей в одну сильную.

### Bagging: Random Forest

```python
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, max_depth=10)
rf.fit(X_train, y_train)
```

- Обучаем много деревьев на **бутстрэп-выборках**
- Каждое дерево использует **случайное подмножество признаков**
- Результат: среднее (регрессия) или голосование (классификация)

**Главные гиперпараметры**: `n_estimators`, `max_depth`, `min_samples_leaf`.

### Boosting: XGBoost / LightGBM / CatBoost

В отличие от bagging, деревья обучаются **последовательно**, каждое исправляет ошибки предыдущих.

```python
# XGBoost — классика
from xgboost import XGBClassifier
xgb = XGBClassifier(n_estimators=200, learning_rate=0.1, max_depth=6)

# LightGBM — быстрее, для больших данных
from lightgbm import LGBMClassifier
lgb = LGBMClassifier(n_estimators=200, learning_rate=0.1, num_leaves=31)

# CatBoost — для категориальных признаков (без one-hot!)
from catboost import CatBoostClassifier
cb = CatBoostClassifier(iterations=200, learning_rate=0.1, verbose=0)
```

### Сравнение бустингов

| | XGBoost | LightGBM | CatBoost |
|---|---|---|---|
| **Скорость** | Быстро | Очень быстро | Средне |
| **Категориальные фичи** | Нужен one-hot | Встроенная поддержка | Автоматически |
| **Пропуски** | Обрабатывает | Обрабатывает | Обрабатывает |
| **Overfitting** | Надо следить | Склонен при малых данных | Лучший контроль |
| **Когда** | Default-выбор | Большие данные | Много категорий |

## Feature Importance

```python
# Важность признаков
importances = model.feature_importances_
feat_imp = pd.DataFrame({'feature': X.columns, 'importance': importances})
feat_imp.sort_values('importance', ascending=False).head(10)

# SHAP — более продвинутая интерпретация
import shap
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)
shap.summary_plot(shap_values, X)
```

## Регуляризация

Деревья склонны к overfitting. Основные рычаги:

- `max_depth` — максимальная глубина
- `min_samples_split` / `min_samples_leaf` — минимальное число объектов в узле/листе
- `min_child_weight` (XGBoost) — минимальная сумма весов в листе
- `learning_rate` (бустинг) — уменьшает вклад каждого дерева
- `n_estimators` + early stopping

```python
model.fit(X_train, y_train,
          eval_set=[(X_val, y_val)],
          early_stopping_rounds=10,
          verbose=False)
```

## Когда tree-based

- Табличные данные (строки и колонки)
- Смешанные типы (числа + категории)
- Нелинейные зависимости
- Важна интерпретируемость (feature importance)

## Когда НЕ tree-based

- Изображения, текст (→ нейросети)
- Очень высокая размерность (→ линейные модели с регуляризацией)
- Нужна гладкая функция (деревья кусочно-постоянные)

## Связанные страницы

- [[../09-machine-learning/supervised-learning|Обучение с учителем]]
- [[../09-machine-learning/model-evaluation|Оценка моделей]]
- [[../09-machine-learning/ml-pipeline-mlflow|ML-пайплайны и MLflow]]
