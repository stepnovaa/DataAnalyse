# R для статистики

## Python или R?

| | Python | R |
|---|---|---|
| **Статистика** | Хорошо (scipy, statsmodels) | Превосходно (из коробки) |
| **Визуализация** | Хорошо (matplotlib, plotly) | Превосходно (ggplot2) |
| **ML** | Превосходно (sklearn, xgboost) | Хорошо (caret, tidymodels) |
| **ETL / Data Engineering** | Превосходно | Слабо |
| **Продакшн** | Превосходно | Сложно |
| **Сообщество** | Огромное, general-purpose | Статистика, academia, биоинформатика |

> В 2026: Python для всего. R — если ты в академии/биостатистике/глубокой статистике.

## Когда R лучше Python

- **Чистая статистика**: линейные модели со сложной структурой ошибок, mixed models
- **ggplot2**: лучшая грамматика графики (но plotnine портирует её в Python)
- **Биоинформатика**: Bioconductor — экосистема которой нет аналога в Python
- **Готовые статистические пакеты**: в CRAN есть реализация любого статистического теста

## Основы R

```r
library(tidyverse)

# Загрузка
df <- read_csv('data.csv')

# Фильтрация
df %>% filter(age > 30, country == 'RU')

# Трансформация
df %>% mutate(tax = price * 0.2)

# Агрегация
df %>%
  group_by(category) %>%
  summarise(
    mean_price = mean(price),
    count = n()
  )

# Визуализация
ggplot(df, aes(x = price, y = sales, color = category)) +
  geom_point() +
  geom_smooth(method = 'lm') +
  theme_minimal()
```

## Tidyverse

Экосистема пакетов для работы с данными:
- **dplyr** — манипуляция данными (filter, mutate, group_by)
- **ggplot2** — визуализация (грамматика графики)
- **tidyr** — преобразование форматов (pivot_longer, pivot_wider)
- **readr** — чтение данных
- **purrr** — функциональное программирование
- **stringr** — работа со строками

## Стоит ли учить R

- **Да**, если: академия, биостатистика, экономика, сложные статистические модели
- **Нет**, если: стартап, data engineering, ML production, общая аналитика

R — нишевый, но мощный инструмент. Python покрывает 90%+ задач аналитика.

## Связанные страницы

- [[../02-statistics/moc-statistics|Статистика]]
- [[../08-visualization/viz-grammar-and-theory|Грамматика графики]] — ggplot2 как эталон
- [[../13-toolbox/python-data-stack|Python Data Stack]]
