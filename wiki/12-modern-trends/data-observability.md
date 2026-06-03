# Наблюдаемость данных (Data Observability)

## Data Quality vs Data Observability

| | Data Quality | Data Observability |
|---|---|---|
| **Что** | Проверка данных на соответствие правилам | Непрерывный мониторинг здоровья данных |
| **Вопрос** | «Эти данные правильные?» | «Я доверяю этой таблице сегодня?» |
| **Подход** | Тесты (статичные ожидания) | Мониторинг (динамическое обнаружение) |
| **Инструменты** | dbt tests, Great Expectations | Monte Carlo, Sifflet, Datafold |

## 5 столпов observability (Barr Moses)

| Столп | Вопрос | Пример |
|-------|--------|--------|
| **Freshness** | Данные актуальны? | Таблица orders не обновлялась 3 часа (должна — каждый час) |
| **Volume** | Данных столько сколько ожидаем? | Сегодня пришло 100 строк, обычно 10000 |
| **Schema** | Схема не изменилась? | Колонку deleted, таблица больше не принимает NULL |
| **Quality** | Данные в порядке? | NULL в колонке вырос с 1% до 20% |
| **Lineage** | Откуда данные и куда идут? | Поломка в upstream: какой дашборд пострадает? |

## Инструменты

| Инструмент | Тип | Когда |
|------------|-----|-------|
| **Monte Carlo** | Enterprise SaaS | Полный observability |
| **Sifflet** | Enterprise SaaS | Data pipeline observability |
| **Datafold** | Data diff | Сравнение окружений при деплое |
| **Elementary** | Open-source (на dbt) | Для небольшой dbt-команды |
| **Great Expectations** | Open-source | Data quality testing |

## Обнаружение аномалий

Вместо ручных порогов («NULL < 5%») — автоматическое обнаружение:

```python
# Monte Carlo / аналоги делают это автоматически
# Принцип: сравнение распределения метрики сегодня vs исторический baseline
today_volume = count_rows_today()
historical_volumes = [count_rows(day) for day in last_30_days]
if today_volume < np.percentile(historical_volumes, 1):
    alert('Аномальное падение объёма!')
```

## Как начать

1. **Мониторь свежесть** (самое простое): когда таблица обновлялась последний раз
2. **Мониторь объём**: число строк сегодня vs вчера
3. **Мониторь схему**: обнаружение изменений колонок (dbt)
4. **Мониторь ключевые метрики**: NULL% в критичных колонках

## Связанные страницы

- [[../06-data-processing/data-quality-and-testing|Качество данных]]
- [[../11-data-engineering/data-governance|Data Governance]]
- [[../11-data-engineering/ci-cd-for-data|CI/CD для данных]]
