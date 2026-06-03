# Оценка моделей

## Зачем оценивать

Модель, идеальная на train и бесполезная на test — overfitting. Метрики — единственный способ узнать, хороша ли модель.

## Метрики регрессии

| Метрика | Формула | Интерпретация |
|---------|---------|---------------|
| **MAE** | Среднее |y - ŷ| | Абсолютная ошибка в единицах y |
| **MSE** | Среднее (y - ŷ)² | Квадрат ошибки. Сильно штрафует выбросы |
| **RMSE** | √MSE | Ошибка в единицах y. Популярна |
| **R²** | 1 - SSres/SStot | Доля объяснённой дисперсии. 1 = идеально, 0 = как среднее |
| **MAPE** | Среднее |(y-ŷ)/y| | Ошибка в %. Плох при y≈0 |

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
```

## Метрики классификации

### Confusion Matrix

```
                Предсказано
                Positive  Negative
Факт  Positive     TP        FN
      Negative     FP        TN
```

### Базовые метрики

| Метрика | Формула | Когда важна |
|---------|---------|-------------|
| **Accuracy** | (TP+TN)/All | Сбалансированные классы |
| **Precision** | TP/(TP+FP) | Цена ложной тревоги высока |
| **Recall** | TP/(TP+FN) | Цена пропуска высока |
| **F1** | 2PR/(P+R) | Баланс Precision и Recall |

```python
from sklearn.metrics import (
    accuracy_score, precision_score,
    recall_score, f1_score, classification_report
)
print(classification_report(y_test, y_pred))
```

### Когда что

- **Accuracy**: классы сбалансированы 50/50
- **Precision (точность)**: «Сколько из предсказанных спам-писем — реально спам?» Цена ложной тревоги
- **Recall (полнота)**: «Сколько реальных спам-писем мы нашли?» Цена пропуска
- **F1**: баланс, когда важен компромисс

### ROC-AUC

```python
from sklearn.metrics import roc_auc_score, roc_curve
auc = roc_auc_score(y_test, y_proba[:, 1])
```

- AUC = 1: идеально
- AUC = 0.5: случайное угадывание (модель бесполезна)
- AUC < 0.5: модель предсказывает наоборот

ROC-AUC устойчив к дисбалансу классов — хорошая метрика по умолчанию для бинарной классификации.

### PR-AUC (Precision-Recall AUC)

Для сильного дисбаланса (<5% положительных) PR-AUC информативнее ROC-AUC.

## Кросс-валидация

```python
from sklearn.model_selection import cross_validate
scores = cross_validate(model, X, y, cv=5,
                        scoring=['accuracy', 'f1', 'roc_auc'])
```

Показывает не только среднее, но и разброс метрики. `cv=5` — стандарт.

## Выбор метрики под бизнес-задачу

| Задача | Пример | Метрика |
|--------|--------|---------|
| Спам-фильтр | Пропустить спам ок, потерять письмо — плохо | Precision |
| Поиск мошенников | Пропустить мошенника — плохо, лишняя проверка — ок | Recall |
| Рекомендации | Важен порядок, а не метки | NDCG, MAP@k |
| Прогноз цены | Ошибка в деньгах | MAE / RMSE |

## Связанные страницы

- [[../09-machine-learning/supervised-learning|Обучение с учителем]]
- [[../02-statistics/inferential-statistics|Статистический вывод]]
- [[../09-machine-learning/ml-vs-statistics|ML vs Статистика]]
