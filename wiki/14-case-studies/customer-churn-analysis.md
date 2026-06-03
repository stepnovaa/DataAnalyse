# Кейс: Анализ оттока клиентов

## Бизнес-контекст

Телеком-компания. 7000+ клиентов. Нужно понять, кто уходит и почему, и построить модель предсказания оттока.

## Данные

```python
# columns: customer_id, tenure, monthly_charges, total_charges,
#          contract_type, payment_method, tech_support, churn (target)
```

## Этап 1: SQL-анализ

```sql
-- Общий churn rate
SELECT
    COUNT(*) FILTER (WHERE churn = 'Yes') * 100.0 / COUNT(*) AS churn_rate
FROM customers;
-- ≈ 26.5%

-- Churn по типу контракта
SELECT contract_type,
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE churn = 'Yes') AS churned,
    ROUND(COUNT(*) FILTER (WHERE churn = 'Yes') * 100.0 / COUNT(*), 1) AS rate
FROM customers
GROUP BY contract_type
ORDER BY rate DESC;
```

```
contract_type    | total | churned | rate
─────────────────────────────────────────
Month-to-month   | 3875  | 1655    | 42.7%  ← главная зона риска
One year         | 1473  | 166     | 11.3%
Two year         | 1695  | 48      | 2.8%
```

**Инсайт**: помесячный контракт → 42.7% churn. Двухлетний → 2.8%. Контракт — главный предиктор.

## Этап 2: EDA

```python
# Распределение tenure (как долго клиент с нами)
sns.histplot(data=df, x='tenure', hue='churn', bins=50)
# Клиенты, которые уходят — в основном новички (tenure < 12 месяцев)

# Monthly charges vs tenure
sns.scatterplot(data=df, x='tenure', y='monthly_charges', hue='churn', alpha=0.5)
# Высокие monthly charges + низкий tenure = зона риска
```

## Этап 3: Модель

```python
import xgboost as xgb
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

X = pd.get_dummies(df.drop(['customer_id', 'churn'], axis=1))
y = df['churn'].map({'Yes': 1, 'No': 0})

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)

model = xgb.XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print(f'ROC-AUC: {roc_auc_score(y_test, y_proba):.3f}')
print(classification_report(y_test, y_pred))
```

### Важность признаков

```python
feat_imp = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

# Top-3: tenure, contract_type_Month-to-month, monthly_charges
```

## Этап 4: Выводы и рекомендации

| Инсайт | Рекомендация |
|--------|-------------|
| Помесячный контракт = 42.7% churn | Стимулировать переход на годовой/двухлетний контракт (скидки) |
| Новички (tenure < 12m) — зона риска | Onboarding программа, персональный менеджер первые 3 месяца |
| Высокие charges + низкий tenure | Проактивное предложение: снизить тариф при угрозе оттока |

## Чему учит кейс

1. **Простые SQL-запросы** могут дать главный инсайт (contract_type)
2. **Дисбаланс классов**: 26.5% churn — accuracy не лучшая метрика. Смотри ROC-AUC, F1.
3. **Интерпретация > точность**: важнее понять почему уходят, чем предсказать с AUC 0.99
4. **Бизнес-рекомендация**: модель бесполезна без действия (что делать с предсказанным churn?)

## Связанные страницы

- [[../04-sql/aggregations-and-grouping|Агрегации и GROUP BY]]
- [[../07-exploratory-analysis/eda-framework|EDA-фреймворк]]
- [[../09-machine-learning/tree-based-models|Деревья и ансамбли]]
