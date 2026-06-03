# Elasticsearch

## Что такое Elasticsearch

Распределённый **поисковый и аналитический** движок на базе Apache Lucene. Не совсем «база данных» в классическом смысле — это специализированное хранилище для полнотекстового поиска и агрегаций.

## Архитектура

```
   Индекс (Index) — как база данных
        │
   Шарды (Shards) — партиции
   ├── Primary 0    ├── Primary 1
   ├── Replica 0    ├── Replica 1
```

- **Индекс** — логическое пространство документов
- **Шард** — физическая часть индекса (Lucene instance)
- **Реплика** — копия шарда для отказоустойчивости и ускорения чтения
- **Документ** — JSON-объект, базовая единица хранения

## Инвертированный индекс

Секрет скорости Elasticsearch:

```
Сырые документы:
  doc1: "The quick brown fox"
  doc2: "The quick fox"

Инвертированный индекс:
  "the"    → [doc1, doc2]
  "quick"  → [doc1, doc2]
  "brown"  → [doc1]
  "fox"    → [doc1, doc2]
```

Поиск по слову = lookup в инвертированном индексе, а не scan по документам.

## CRUD и поиск

```json
// Index (вставить/обновить документ)
PUT /products/_doc/1
{
  "name": "iPhone 15",
  "brand": "Apple",
  "price": 999,
  "description": "Смартфон с отличной камерой и мощным процессором"
}

// Search
GET /products/_search
{
  "query": {
    "match": {
      "description": "камера процессор"
    }
  }
}

// Фильтрация + сортировка
GET /products/_search
{
  "query": {
    "bool": {
      "filter": [
        {"term": {"brand": "Apple"}},
        {"range": {"price": {"gte": 500, "lte": 1500}}}
      ]
    }
  },
  "sort": [{"price": "asc"}]
}
```

## Агрегации

Elasticsearch — мощный движок агрегаций, сравнимый с GROUP BY в SQL:

```json
GET /orders/_search
{
  "size": 0,
  "aggs": {
    "by_category": {
      "terms": {"field": "category.keyword"},
      "aggs": {
        "avg_price": {"avg": {"field": "price"}},
        "total_revenue": {"sum": {"field": "total"}}
      }
    },
    "sales_over_time": {
      "date_histogram": {
        "field": "created_at",
        "calendar_interval": "month"
      }
    }
  }
}
```

## Когда Elasticsearch — правильный выбор

- **Полнотекстовый поиск**: релевантность, fuzzy matching, автодополнение
- **Логи и мониторинг** (ELK Stack: Elasticsearch + Logstash + Kibana)
- **Поиск по каталогу товаров**: фасеты, фильтры, быстрый поиск
- **Аналитика в реальном времени**: агрегации по миллионам документов за миллисекунды

## Когда Elasticsearch НЕ подходит

- Основное хранилище (нет транзакций, не ACID)
- Частые обновления (каждое обновление = переиндексация документа)
- JOIN-ы (Elasticsearch не реляционная БД)
- Данные, которые не нужно искать (храни в БД, индексируй только нужное в ES)

## ELK Stack

```
Logstash / Beats → Elasticsearch → Kibana
   (сбор логов)     (хранение+поиск)    (визуализация)
```

Классический стек для централизованного логирования и мониторинга.

## Связанные страницы

- [[../05-databases-nosql/nosql-taxonomy|NoSQL-таксономия]]
- [[../05-databases-nosql/nosql-vs-sql-decision|NoSQL vs SQL]]
- [[../08-visualization/bi-tools-landscape|BI-инструменты]] — Kibana как BI для ES
