# CAP-теорема и PACELC

## CAP (Брюер, 2000)

В распределённой системе можно гарантировать только **два из трёх** свойств одновременно:

```
       C (Consistency)
      / \
     /   \
    /     \
   /  CA   \  CP
  /         \
P ----------- A
(Partition)   (Availability)
     AP
```

| Свойство | Значение |
|----------|----------|
| **C**onsistency | Все узлы видят одни и те же данные в любой момент |
| **A**vailability | Каждый запрос получает ответ (не ошибку) |
| **P**artition tolerance | Система работает даже при разрыве связи между узлами |

## Что CAP значит на практике

**Partition (разрыв сети) неизбежен** в распределённых системах. Значит, при partition ты выбираешь: **консистентность** или **доступность**.

### CP (Consistency + Partition)

При разрыве сети: часть узлов отказывается отвечать, чтобы не отдать устаревшие данные.

- MongoDB (по умолчанию)
- HBase
- Redis (cluster mode с majority writes)

### AP (Availability + Partition)

При разрыве сети: все узлы отвечают, но данные могут быть устаревшими.

- Cassandra
- DynamoDB (по умолчанию)
- Couchbase

### CA (без Partition)

В реальном мире недостижимо — partition'ы всегда возможны. Обычно это значит «одноузловая система»:
- Традиционные реляционные БД (не распределённые)
- SQLite

## PACELC — расширение CAP

**P**artition → tradeoff **A** vs **C**
**E**lse (нет partition) → tradeoff **L**atency vs **C**onsistency

То есть: система выбирает не только поведение при partition, но и при нормальной работе.

- **PA/EL**: Cassandra — доступность при partition, низкая latency без partition
- **PC/EC**: BigTable/HBase — консистентность всегда
- **PA/EC**: DynamoDB — доступность при partition, консистентность без

## Практические выводы

1. **Не выбирай БД только по CAP** — это упрощение. Смотри на реальные гарантии и поведение.
2. **Большинство систем позволяют настраивать консистентность** на уровне запроса (DynamoDB, Cassandra).
3. **ACID vs BASE**: ACID — сильная консистентность, BASE (Basically Available, Soft state, Eventually consistent) — слабая.

## Связанные страницы

- [[../05-databases-nosql/nosql-taxonomy|NoSQL-таксономия]]
- [[../05-databases-nosql/nosql-vs-sql-decision|NoSQL vs SQL]]
- [[../03-databases-relational/transactions-and-acid|Транзакции и ACID]]
