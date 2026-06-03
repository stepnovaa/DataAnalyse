# Jupyter Workflow

## Jupyter — инструмент, а не религия

Jupyter отличен для **исследования и прототипирования**. Но в продакшене код в ноутбуках — источник боли.

## Best Practices

### Структура ноутбука

```markdown
# Заголовок: что делаем
## 1. Setup (импорты, конфиг)
## 2. Загрузка данных
## 3. EDA / Анализ
## 4. Моделирование (если нужно)
## 5. Выводы
```

### Первая ячейка — конфигурация

```python
%load_ext autoreload
%autoreload 2           # автоматически перезагружать модули

%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style='whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

import pandas as pd
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 100)

import warnings
warnings.filterwarnings('ignore')
```

### Сквозная ячейка конфигурации БД

```python
from sqlalchemy import create_engine
import os

engine = create_engine(os.environ['DATABASE_URL'])
# engine = create_engine('duckdb:///analytics.db')  # или DuckDB локально
```

## Магия Jupyter

```python
%time df.groupby('cat').mean()      # время выполнения ячейки
%timeit df.groupby('cat').mean()    # многократный замер

%%sql                               # SQL напрямую (с ipython-sql)
SELECT * FROM orders LIMIT 10

%debug                              # дебаггер после исключения

!pip install package                # быстрая установка (осторожно)
```

## От ноутбука к скрипту

### Плохо: всё в ноутбуке (notebook-driven development)

```
analysis.ipynb → запускаешь ячейки вручную → каждый раз разный результат
```

### Хорошо: код в .py, ноутбук как интерфейс

```
config.py      ← конфигурация
queries.sql    ← SQL-запросы
etl.py         ← функции загрузки и очистки
analysis.py    ← основные функции
eda.ipynb      ← только визуализация и выводы
```

Ноутбук импортирует функции из .py файлов и вызывает их:

```python
from etl import load_data, clean_data
from analysis import analyze_churn

df = load_data()
df_clean = clean_data(df)
results = analyze_churn(df_clean)
results.plot()
```

## Инструменты

### nbformat + Jupytext

```bash
pip install jupytext
# Сохраняет ноутбуки как .py файлы автоматически
```

Позволяет версионировать ноутбуки в git (смотри diff в Python, а не JSON).

### Papermill — параметризованные ноутбуки

```bash
papermill template.ipynb output.ipynb -p country RU -p date 2024-01-01
```

Запускает ноутбук с параметрами — для автоматизации отчётов.

### Quarto

Next-gen система для технических публикаций: ноутбуки + markdown → HTML/PDF/презентация. Замена RMarkdown.

## Связанные страницы

- [[../13-toolbox/python-data-stack|Python Data Stack]]
- [[../07-exploratory-analysis/eda-framework|EDA-фреймворк]]
