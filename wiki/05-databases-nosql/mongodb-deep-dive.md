# MongoDB Deep Dive

## Модель данных

MongoDB — документная БД. Данные хранятся в **BSON** (Binary JSON) — документах.

```json
{
  "_id": ObjectId("..."),
  "name": "iPhone 15",
  "price": 999.99,
  "category": "phones",
  "specs": {
    "screen": 6.1,
    "storage": 128
  },
  "variants": [
    {"color": "black", "stock": 100},
    {"color": "white", "stock": 50}
  ]
}
```

- **Коллекция** ≈ таблица (но без фиксированной схемы)
- **Документ** ≈ строка (JSON-объект)
- **Вложенные документы** и массивы — нативные

## Когда MongoDB — правильный выбор

- Схема данных часто меняется
- Документы — естественная модель (каталог товаров, контент, профили)
- Данные читаются и пишутся вместе (документ — единица доступа)
- Много неструктурированных/полуструктурированных данных

## Когда MongoDB НЕ подходит

- Сложные JOIN'ы и связи между сущностями (в MongoDB JOIN — через `$lookup`, неудобно)
- Строгая консистентность и ACID в масштабе (до 4.0 не было multi-document транзакций; сейчас есть, но дорого)
- Аналитика и отчёты (OLAP) — реляционка/DWH лучше
- Данные, которые должны быть строго нормализованы

## CRUD — базовые операции

```javascript
// Insert
db.products.insertOne({name: "iPhone", price: 999})

// Find
db.products.find({price: {$gt: 500}}).sort({price: -1}).limit(10)

// Update
db.products.updateOne(
  {_id: id},
  {$set: {price: 899}, $inc: {views: 1}}
)

// Delete
db.products.deleteMany({status: "discontinued"})
```

## Aggregation Pipeline

Главный аналитический инструмент MongoDB. Документы проходят через стадии (stages) пайплайна:

```javascript
db.orders.aggregate([
  {$match: {status: "completed"}},           // фильтр
  {$group: {_id: "$customer_id", total: {$sum: "$amount"}}},  // группировка
  {$sort: {total: -1}},                       // сортировка
  {$limit: 10}                                // топ-10
])
```

**Стадии**: `$match`, `$group`, `$sort`, `$project`, `$lookup` (JOIN), `$unwind` (развернуть массив), `$bucket` (гистограмма).

## Индексы

```javascript
// Обычный индекс
db.products.createIndex({category: 1})

// Составной
db.products.createIndex({category: 1, price: -1})

// Текстовый
db.products.createIndex({description: "text"})

// Геопространственный
db.stores.createIndex({location: "2dsphere"})

// TTL (автоудаление через N секунд)
db.sessions.createIndex({createdAt: 1}, {expireAfterSeconds: 3600})
```

## Шардирование

MongoDB изначально проектировался для горизонтального масштабирования:

```
Shard 1 ─┐
Shard 2 ─┼── Mongos (Router) ── Приложение
Shard 3 ─┘
```

**Shard key** — поле, по которому данные распределяются по шардам. Критично выбрать правильно:
- Хороший shard key: равномерное распределение, используется в большинстве запросов
- Плохой: монотонно возрастающий (все новые документы на один шард — hotspot)

## Практические советы

1. **Embed vs Reference**: если данные читаются вместе — embed. Если обновляются независимо — reference.
2. **Следи за размером документа**: 16 МБ лимит. Большие массивы ↔ отдельная коллекция.
3. **Транзакции дороги**: не злоупотребляй multi-document транзакциями. Проектируй документы так, чтобы обновлять один документ.
4. **Aggregation pipeline** часто эффективнее MapReduce (который deprecated).

## Связанные страницы

- [[../05-databases-nosql/nosql-vs-sql-decision|NoSQL vs SQL]]
- [[../05-databases-nosql/redis-deep-dive|Redis Deep Dive]]
- [[../03-databases-relational/mysql-deep-dive|MySQL]] — сравнение
