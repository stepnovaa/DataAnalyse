# Обучение с учителем (Supervised Learning)

## Постановка задачи

Дано: пары (X, y) — признаки и правильные ответы.
Найти: функцию f(X) → ŷ, которая хорошо предсказывает y на новых данных.

## Регрессия vs Классификация

| | Регрессия | Классификация |
|---|---|---|
| **y** | Непрерывное число | Категория |
| **Пример** | Цена, доход, температура | Отток (да/нет), класс товара |
| **Метрика** | RMSE, MAE, R² | Accuracy, F1, ROC-AUC |
| **Модели** | Linear, Ridge, XGBoost | Logistic, Random Forest, XGBoost |

## Базовые модели

### Линейная регрессия

```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

**Плюсы**: интерпретируема, быстрая, baseline.
**Минусы**: только линейные зависимости, чувствительна к выбросам.

### Логистическая регрессия (классификация)

```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, y_train)
y_proba = model.predict_proba(X_test)  # вероятности
y_pred = model.predict(X_test)          # классы
```

Несмотря на название — для классификации. Даёт вероятности.

## Ансамбли

См. [[../09-machine-learning/tree-based-models|Деревья и ансамбли]].

## Pipeline в sklearn

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
pipeline.fit(X_train, y_train)
```

Pipeline объединяет preprocessing и модель — не надо отдельно fit_transform и transform.

## Train / Validation / Test Split

```python
from sklearn.model_selection import train_test_split

# 60 / 20 / 20
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25)
```

- **Train** (60%) — обучаем модель
- **Validation** (20%) — подбираем гиперпараметры, выбираем модель
- **Test** (20%) — финальная оценка. Трогаем ОДИН раз

> Никогда не оптимизируй гиперпараметры на test! Только на validation.

## Кросс-валидация

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f'{scores.mean():.3f} ± {scores.std():.3f}')
```

Устойчивая оценка на всём датасете. Не заменяет test set, а дополняет.

## Overfitting и Underfitting

| | Underfitting | Хорошо | Overfitting |
|---|---|---|---|
| **Train score** | Низкий | Высокий | Очень высокий |
| **Test score** | Низкий | Высокий | Низкий |
| **Разница** | Маленькая | Маленькая | Большая |
| **Рецепт** | Сложнее модель | — | Регуляризация, больше данных |

## Связанные страницы

- [[../09-machine-learning/tree-based-models|Деревья и ансамбли]]
- [[../09-machine-learning/model-evaluation|Оценка моделей]]
- [[../09-machine-learning/ml-pipeline-mlflow|ML-пайплайны и MLflow]]
