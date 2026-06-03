# ML-пайплайны и MLflow

## Проблема

Модели размножаются. Версии, параметры, метрики, данные — хаос. MLflow решает проблему воспроизводимости и управления жизненным циклом моделей.

## MLflow — 4 компонента

```
MLflow
├── Tracking     — логирование экспериментов (параметры, метрики, артефакты)
├── Projects     — упаковка кода в воспроизводимый формат
├── Models       — упаковка и деплой моделей в разных форматах
└── Registry     — централизованный реестр моделей (staging, production, archived)
```

## Tracking — логирование экспериментов

```python
import mlflow

mlflow.set_experiment('customer_churn')

with mlflow.start_run():
    # Параметры
    mlflow.log_param('model', 'xgboost')
    mlflow.log_param('max_depth', 6)
    mlflow.log_param('learning_rate', 0.1)

    # Обучение
    model = XGBClassifier(max_depth=6, learning_rate=0.1)
    model.fit(X_train, y_train)

    # Метрики
    y_pred = model.predict(X_test)
    mlflow.log_metric('accuracy', accuracy_score(y_test, y_pred))
    mlflow.log_metric('f1', f1_score(y_test, y_pred))
    mlflow.log_metric('roc_auc', roc_auc_score(y_test, y_pred))

    # Модель и артефакты
    mlflow.sklearn.log_model(model, 'model')
    mlflow.log_artifact('feature_importance.png')
```

### Запуск UI

```bash
mlflow ui --port 5000
# Открыть http://localhost:5000
```

Сравнивай эксперименты в веб-интерфейсе — видно какой набор параметров дал лучшую метрику.

## Auto-logging

```python
mlflow.autolog()  # автоматически логирует sklearn, xgboost, pytorch, ...
```

Ловит модель, параметры и метрики автоматически. Для быстрых экспериментов.

## Model Registry

```python
# Зарегистрировать модель
mlflow.register_model('runs:/<run_id>/model', 'churn_predictor')

# В UI: перевести в Staging → Production
```

Стадии:
- **None** — зарегистрирована
- **Staging** — тестируется
- **Production** — в продакшене
- **Archived** — на пенсии

## Полный ML-пайплайн

```python
# 1. Загрузка данных
# 2. Предобработка (sklearn Pipeline)
# 3. Обучение + MLflow tracking
# 4. Регистрация модели
# 5. Деплой (через MLflow serving)
```

### Деплой через MLflow

```bash
mlflow models serve -m models:/churn_predictor/Production -p 1234
# Теперь модель доступна по REST API
```

```python
import requests
resp = requests.post('http://localhost:1234/invocations',
                     json={'dataframe_split': X_test.to_dict('split')})
predictions = resp.json()
```

## Лучшие практики

1. **Именуй эксперименты осмысленно**: `customer_churn_v2`
2. **Логируй data version**: хеш датасета или git commit
3. **Сравнивай перед выбором**: обучи несколько моделей, сравни в MLflow UI
4. **Promote осознанно**: не всё что имеет хороший AUC должно идти в Production
5. **Мониторь после деплоя**: метрики на живых данных (data drift!)

## Альтернативы MLflow

- **Weights & Biases** (wandb) — для deep learning, лучшая визуализация
- **Neptune.ai** — похож на wandb
- **DVC** — версионирование данных + пайплайны

## Связанные страницы

- [[../09-machine-learning/supervised-learning|Обучение с учителем]]
- [[../09-machine-learning/model-evaluation|Оценка моделей]]
- [[../11-data-engineering/ci-cd-for-data|CI/CD для данных]]
