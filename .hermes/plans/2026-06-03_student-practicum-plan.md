# DataAnalyse Practicum — План проекта для студента

> **Цель:** Пройти полный цикл анализа данных на практике — от сырых данных до бизнес-выводов. Каждый этап закрепляет один из разделов вики и даёт рабочий артефакт.

**Стек:** Python (pandas, numpy, matplotlib, seaborn, scikit-learn, plotly)  
**Формат:** Jupyter Notebooks (.ipynb) + вспомогательные .py-скрипты  
**Данные:** Открытые датасеты (Kaggle / UCI / встроенные в seaborn)  
**Время:** ~2–4 недели при 2–3 часа в день

---

## 📁 Структура проекта

```
DataAnalyse/
├── wiki/                    # ← вики (уже есть, 109 страниц)
├── data/                    # ← датасеты (создаём)
│   ├── raw/                 #   исходные данные
│   ├── processed/           #   очищенные данные
│   └── external/            #   внешние справочники
├── notebooks/               # ← Jupyter ноутбуки
│   ├── 01-data-wrangling/   #   этап 1
│   ├── 02-eda/              #   этап 2
│   ├── 03-statistics/       #   этап 3
│   ├── 04-visualization/    #   этап 4
│   ├── 05-ml-basics/        #   этап 5
│   └── 06-case-study/       #   этап 6 — финальный кейс
├── src/                     # ← переиспользуемые модули
│   ├── __init__.py
│   ├── config.py            #   пути, константы
│   └── utils.py             #   вспомогательные функции
├── reports/                 # ← отчёты и презентации
│   └── images/              #   экспортированные графики
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Этап 0: Настройка окружения

**Что делаем:** Разворачиваем рабочее окружение.

**Файлы:**
- Создать: `requirements.txt`, `.gitignore`, `src/config.py`, `src/utils.py`

**Шаги:**

1. Создать `requirements.txt`:
   ```
   pandas>=2.0
   numpy>=1.24
   matplotlib>=3.7
   seaborn>=0.12
   scikit-learn>=1.3
   plotly>=5.15
   scipy>=1.11
   jupyter>=1.0
   statsmodels>=0.14
   ```

2. Создать `.gitignore`:
   ```
   __pycache__/
   .venv/
   .env
   data/raw/*
   data/processed/*
   !data/raw/.gitkeep
   !data/processed/.gitkeep
   *.ipynb_checkpoints/
   .DS_Store
   ```

3. Создать структуру папок (`data/raw/`, `data/processed/`, `data/external/`, `notebooks/`, `src/`, `reports/images/`)

4. Установить зависимости: `pip install -r requirements.txt`

**Чему научитесь:** работа с виртуальным окружением, управление зависимостями, git + .gitignore.

**Связь с вики:** [[13-toolbox/python-data-stack|Python Data Stack]]

---

## Этап 1: Data Wrangling — очистка и подготовка данных

**Что делаем:** Берём реальный «грязный» датасет и приводим его в порядок.

**Датасет:** Titanic (встроенный в seaborn: `sns.load_dataset('titanic')`)

**Ноутбук:** `notebooks/01-data-wrangling/titanic-wrangling.ipynb`

**Задачи:**

1. **Загрузка и первичный осмотр**
   - `df.info()`, `df.describe()`, `df.head(10)`
   - Определить типы колонок, количество пропусков

2. **Обработка пропусков**
   - `age` → заполнить медианой по классу (`Pclass` + `Sex`)
   - `embarked` → заполнить модой
   - `deck` → создать бинарный признак `has_deck`
   - Создать колонку-индикатор `age_missing`

3. **Выбросы и дубликаты**
   - Проверить дубликаты по `df.duplicated()`
   - Проверить выбросы в `fare` (IQR-метод + визуализация)
   - Решить: удалить, заменить или оставить

4. **Создание новых признаков (feature engineering)**
   - `family_size = sibsp + parch + 1`
   - `is_alone = family_size == 1`
   - `title` (Mr, Mrs, Miss, Master...) — извлечь из имени
   - `age_group` (binning: Child, Teen, Adult, Senior)

5. **Сохранение очищенного датасета**
   - `data/processed/titanic_clean.csv`

**Чему научитесь:** pandas (filter, transform, fillna, groupby), обработка пропусков и выбросов, создание признаков.

**Связь с вики:** [[06-data-processing/data-cleaning|Очистка данных]], [[06-data-processing/data-wrangling-python|Data Wrangling — Python]], [[07-exploratory-analysis/feature-engineering|Feature Engineering]]

---

## Этап 2: EDA — разведочный анализ данных

**Что делаем:** Применяем EDA-фреймворк из вики на двух датасетах.

**Датасеты:**
- Titanic (очищенный с этапа 1)
- Tips (`sns.load_dataset('tips')`) — проще, для отработки техник

**Ноутбуки:**
- `notebooks/02-eda/titanic-eda.ipynb`
- `notebooks/02-eda/tips-eda.ipynb`

**Задачи (для каждого датасета — одинаковый фреймворк):**

1. **Структура** (`df.shape`, типы, уникальные значения)
2. **Одномерный анализ** (гистограммы, boxplot, value_counts)
3. **Двумерный анализ** (cross-tab, correlation heatmap, scatter)
4. **Многомерный анализ** (pairplot, facet grid)
5. **Выводы и гипотезы** — 3–5 ключевых инсайтов по каждому датасету
6. **EDA-отчёт в markdown** (шаблон из вики)

**Чему научитесь:** системный EDA, различие uni/bi/multivariate, формулировка гипотез, автоматические EDA-отчёты (ydata-profiling).

**Связь с вики:** [[07-exploratory-analysis/eda-framework|EDA-фреймворк]], [[07-exploratory-analysis/univariate-analysis|Одномерный анализ]], [[07-exploratory-analysis/bivariate-analysis|Двумерный анализ]], [[07-exploratory-analysis/multivariate-analysis|Многомерный анализ]]

---

## Этап 3: Статистика — проверка гипотез и A/B-тест

**Что делаем:** Проверяем гипотезы, которые появились на этапе EDA.

**Датасет:** Tips (из seaborn)

**Ноутбук:** `notebooks/03-statistics/hypothesis-testing.ipynb`

**Задачи:**

1. **Описательная статистика** для сегментов
   - Средние, медианы, std, квартили по группам (smoker/no-smoker, sex, day)
   
2. **Визуализация распределений**
   - Гистограммы с KDE
   - Boxplot по группам
   - Q-Q plot для проверки нормальности

3. **Проверка гипотез**
   - **t-test:** отличаются ли средние чаевые у курящих и некурящих?
   - **Mann-Whitney:** то же для ненормальных распределений
   - **Chi-square:** есть ли связь пола и курения?
   - **ANOVA:** отличаются ли чаевые по дням недели?

4. **Корреляционный анализ**
   - Pearson vs Spearman
   - Матрица корреляций с аннотациями

5. **Простой A/B-тест (имитация)**
   - Сгенерировать две выборки (контроль vs тест)
   - Проверить на нормальность
   - Применить t-test
   - Рассчитать size effect (Cohen's d)
   - Интерпретировать p-value и доверительный интервал

**Чему научитесь:** t-test, Mann-Whitney, Chi-square, ANOVA, p-value, корреляции, A/B-тестирование.

**Связь с вики:** [[02-statistics/descriptive-statistics|Описательная статистика]], [[02-statistics/hypothesis-testing|Проверка гипотез]], [[02-statistics/ab-testing|A/B-тестирование]], [[02-statistics/correlation-and-regression|Корреляция и регрессия]]

---

## Этап 4: Визуализация и сторителлинг

**Что делаем:** Учимся делать графики, которые рассказывают историю.

**Датасет:** Titanic (очищенный)

**Ноутбук:** `notebooks/04-visualization/data-storytelling.ipynb`

**Задачи:**

1. **Повторение грамматики графики**
   - Matplotlib: фигура → оси → слои
   - Seaborn: `relplot`, `catplot`, `displot` с параметрами

2. **Библиотека графиков (chart chooser)**
   - Распределение: hist, box, violin, kde
   - Сравнение: bar, grouped bar, heatmap
   - Связи: scatter, jointplot, pairplot
   - Состав: stacked bar, pie (осторожно!)
   - Временные ряды: line, area (на вымышленных данных)

3. **Один датасет — три истории**
   - История 1: «Класс выживания» (Pclass vs Survival)
   - История 2: «Женщины и дети» (Sex + Age vs Survival)
   - История 3: «Цена билета и шансы» (Fare vs Survival)
   - Для каждой: продумать визуализацию, подписать оси, добавить аннотацию-вывод

4. **Интерактивная визуализация (Plotly)**
   - Те же графики в Plotly (интерактивные)
   - Сохранить как HTML

5. **Dashboard-макет**
   - 3–4 графика в одной фигуре (plt.subplots)
   - Единая цветовая схема, подписи, легенда

6. **Правила цвета и доступности**
   - Цветовая палитра для дальтоников (ColorBrewer / viridis)
   - Размер шрифта, контраст, метки

**Чему научитесь:** осознанный выбор графика, сторителлинг данными, Plotly, дизайн дашбордов, доступность.

**Связь с вики:** [[08-visualization/viz-grammar-and-theory|Грамматика графики]], [[08-visualization/chart-chooser|Выбор графика]], [[08-visualization/matplotlib-seaborn|Matplotlib + Seaborn]], [[08-visualization/plotly-interactive|Plotly]], [[08-visualization/data-storytelling|Сторителлинг]], [[08-visualization/color-and-accessibility|Цвет и доступность]]

---

## Этап 5: ML — первые модели

**Что делаем:** Строим модели классификации и регрессии, учимся оценивать их качество.

**Датасеты:**
- Titanic (классификация — выживание)
- Tips (регрессия — предсказание чаевых)

**Ноутбук:** `notebooks/05-ml-basics/first-models.ipynb`

**Задачи:**

1. **Подготовка данных для ML**
   - One-hot encoding категориальных признаков
   - Разделение на train/test (80/20, stratify для классификации)
   - Масштабирование (StandardScaler)

2. **Классификация (Titanic)**
   - Logistic Regression
   - Decision Tree
   - Random Forest
   - Сравнение метрик: accuracy, precision, recall, F1, ROC-AUC
   - Confusion matrix
   - ROC-кривая

3. **Регрессия (Tips)**
   - Linear Regression
   - Ridge / Lasso
   - Decision Tree Regressor
   - Метрики: MSE, RMSE, MAE, R²
   - График residuals (остатки vs предсказания)

4. **Feature importance**
   - Коэффициенты логистической регрессии
   - Importance из Random Forest
   - SHAP summary plot (если осилите)
   - Вывод: какие признаки самые важные? Совпадает ли это с EDA?

5. **Борьба с переобучением**
   - Cross-validation (KFold, 5-fold)
   - Learning curves
   - Noise в feature importance при малом датасете

**Чему научитесь:** разметка train/test, логистическая регрессия, деревья, Random Forest, метрики, feature importance, cross-validation.

**Связь с вики:** [[09-machine-learning/supervised-learning|Обучение с учителем]], [[09-machine-learning/tree-based-models|Деревья и ансамбли]], [[09-machine-learning/model-evaluation|Оценка моделей]], [[09-machine-learning/ml-vs-statistics|ML vs Статистика]]

---

## Этап 6: Финальный кейс — от данных до презентации

**Что делаем:** End-to-end проект, объединяющий все навыки.

**Датасет:** Telecom Customer Churn (Kaggle: Telco Customer Churn)
- ~7000 строк, 21 колонка
- Реальная бизнес-задача

**Ноутбуки:** `notebooks/06-case-study/churn-analysis/` — серия:
- `01-data-loading.ipynb`
- `02-eda.ipynb`
- `03-sql-analysis.ipynb` (DuckDB + SQL)
- `04-modeling.ipynb`
- `05-conclusions.ipynb`

**Задачи:**

1. **Загрузка и первичный осмотр** (как в этапе 1, но на новом датасете)
2. **Очистка:** пропуски в TotalCharges, типы данных
3. **EDA:** churn rate по сегментам, корреляции, распределения
4. **SQL-анализ через DuckDB** (новый навык!)
   - Подключиться к тому же CSV через DuckDB
   - Написать SQL-запросы: churn rate по контрактам, по платёжным методам
   - Сравнить подходы: pandas vs SQL

5. **ML-модель:** предсказание churn
   - Random Forest / XGBoost
   - ROC-AUC, confusion matrix
   - Feature importance → главные причины оттока

6. **Бизнес-выводы**
   - Таблица «Инсайт → Рекомендация → Ожидаемый эффект»
   - Топ-3 сегмента для удержания
   - Какие метрики отслеживать дальше

7. **Презентация** (в виде README.md или markdown-отчёта)
   - Структура: Проблема → Данные → Анализ → Модель → Выводы
   - 3–5 ключевых графиков
   - Язык: для бизнес-аудитории, без кода

**Чему научитесь:** полный цикл анализа данных, SQL через DuckDB, бизнес-интерпретация ML, презентация результатов.

**Связь с вики:** [[14-case-studies/customer-churn-analysis|Кейс: Анализ оттока]], [[10-big-data/duckdb-local-analytics|DuckDB]], [[04-sql/moc-sql|SQL]], [[13-toolbox/python-data-stack|Python Data Stack]]

---

## ⏱ График прохождения

| Этап | Тема | Дней | Объём (ноутбуков) |
|------|------|------|-------------------|
| 0 | Настройка окружения | 1 | — |
| 1 | Data Wrangling | 2–3 | 1 |
| 2 | EDA | 3–4 | 2 |
| 3 | Статистика | 3–4 | 1 |
| 4 | Визуализация | 3–4 | 1 |
| 5 | ML-модели | 4–5 | 1 |
| 6 | Финальный кейс | 4–5 | 5 |
| **Итого** | | **~18–26 дней** | **11 ноутбуков** |

---

## 📚 Связь каждого этапа с вики

| Этап | Раздел вики | Что прочитать перед этапом |
|------|-------------|---------------------------|
| 0 | `13-toolbox/python-data-stack.md` | Python Data Stack |
| 1 | `06-data-processing/data-cleaning.md`, `06-data-processing/data-wrangling-python.md` | Очистка + Data Wrangling |
| 2 | `07-exploratory-analysis/eda-framework.md`, `07-exploratory-analysis/univariate.md`, `07-exploratory-analysis/bivariate.md` | EDA Framework |
| 3 | `02-statistics/descriptive-statistics.md`, `02-statistics/hypothesis-testing.md`, `02-statistics/ab-testing.md` | Статистика |
| 4 | `08-visualization/chart-chooser.md`, `08-visualization/data-storytelling.md`, `08-visualization/matplotlib-seaborn.md` | Визуализация |
| 5 | `09-machine-learning/supervised-learning.md`, `09-machine-learning/tree-based-models.md`, `09-machine-learning/model-evaluation.md` | ML |
| 6 | `14-case-studies/customer-churn-analysis.md`, `10-big-data/duckdb-local-analytics.md` | Кейс + DuckDB |

---

## 🧰 Инструменты, которые освоите

- **pandas** — вся мощь датафреймов (группировки, pivot, melt, join)
- **matplotlib + seaborn** — статическая визуализация для публикаций
- **plotly** — интерактивные графики, дашборды
- **scikit-learn** — классический ML (логистическая регрессия, деревья, Random Forest)
- **scipy + statsmodels** — статистические тесты (t-test, Chi-square, ANOVA)
- **DuckDB** — SQL-анализ локально без установки БД
- **Jupyter** — интерактивная разработка и отчёты
- **Git** — версионирование кода

---

## ✅ Критерии успеха

После прохождения плана вы сможете:

- [ ] Самостоятельно загрузить любой CSV-датасет и сделать первичный осмотр
- [ ] Найти и обработать пропуски, дубликаты, выбросы
- [ ] Провести полный EDA с формулировкой гипотез
- [ ] Выбрать правильный тип графика для задачи
- [ ] Проверить гипотезу статистическим тестом (t-test, Chi-square)
- [ ] Построить и оценить модель классификации (accuracy, F1, ROC-AUC)
- [ ] Интерпретировать важность признаков
- [ ] Сформулировать бизнес-выводы и представить их без кода
- [ ] Написать SQL-запросы через DuckDB
- [ ] Работать в Jupyter + Git + виртуальное окружение

---

## 🚀 Старт

Готовы начать? Я помогу на каждом этапе:
- Напишу код — вы разбираете
- Объясню, что делает каждая строка
- Отвечу на вопросы
- Поправлю, если что-то пошло не так

Просто скажите: **«Поехали с этапа 0»** или **«Начинаем этап 1»**.
