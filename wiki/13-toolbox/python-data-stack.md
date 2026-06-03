# Python Data Stack

## Ядро

| Библиотека | Для чего | Когда |
|------------|----------|-------|
| **NumPy** | N-мерные массивы, линейная алгебра | Всегда — фундамент |
| **Pandas** | Табличные данные, ETL | Основной инструмент аналитика |
| **Polars** | Быстрые датафреймы | >1GB данных, production |
| **SciPy** | Научные вычисления, статистика | Статистические тесты, оптимизация |

## Визуализация

| Библиотека | Стиль | Когда |
|------------|-------|-------|
| **Matplotlib** | Статическая, низкоуровневая | Публикации, полный контроль |
| **Seaborn** | Статистическая, красивая | Быстрый EDA |
| **Plotly** | Интерактивная | Дашборды, исследование |

См. [[../08-visualization/moc-visualization|Визуализация]].

## ML и статистика

| Библиотека | Для чего |
|------------|----------|
| **scikit-learn** | Классический ML (регрессия, классификация, кластеризация) |
| **XGBoost / LightGBM / CatBoost** | Градиентный бустинг |
| **statsmodels** | Статистические модели (OLS, ARIMA, тесты) |
| **Prophet** | Прогнозирование временных рядов |
| **SHAP** | Интерпретация ML-моделей |

## NLP

| Библиотека | Для чего |
|------------|----------|
| **NLTK** | Классический NLP (токенизация, стемминг) |
| **spaCy** | Промышленный NLP (NER, POS, parsing) |
| **Transformers** | Современные LLM (BERT, GPT) |
| **sentence-transformers** | Embeddings |

## Инструменты разработки

| Инструмент | Для чего |
|------------|----------|
| **Jupyter** | Интерактивная разработка |
| **VS Code / Cursor** | IDE с автодополнением |
| **pytest** | Тестирование кода |
| **Black / Ruff** | Форматирование |
| **Poetry / uv** | Управление зависимостями |

## Минимальный стек аналитика

```bash
pip install pandas numpy matplotlib seaborn scikit-learn jupyter
```

## Продвинутый стек

```bash
pip install polars plotly xgboost statsmodels scipy spacy transformers
```

## Связанные страницы

- [[../06-data-processing/data-wrangling-python|Data Wrangling — Python]]
- [[../06-data-processing/polars-modern-dataframes|Polars]]
- [[../08-visualization/moc-visualization|Визуализация]]
- [[../09-machine-learning/moc-machine-learning|ML]]
