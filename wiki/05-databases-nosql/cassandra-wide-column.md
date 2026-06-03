# Cassandra и Wide-Column БД

## Что такое Wide-Column

Не «колоночная БД» (как ClickHouse), а **модель данных с разреженными строками**, где разные строки могут иметь разный набор колонок. Данные организованы вокруг запросов, а не сущностей.

## Cassandra — архитектура

```
                         Данные
                    ┌──────┼──────┐
                 Node1  Node2  Node3
             (токен 0) (т. 80) (т. 160)
                    │       │       │
              ┌─────┼───────┼───────┼─────┐
         Репликация: RF=2 (каждая запись на 2 узлах)
```

- **Кольцевая архитектура**: узлы образуют кольцо
- **Каждый узел равноправен**: нет master/slave
- **Шардирование**: через partition key (хеш-функция распределяет по токенам кольца)
- **Репликация**: данные реплицируются на N следующих узлов по кольцу

## Модель данных

```cql
CREATE TABLE sensor_data (
    sensor_id UUID,
    date DATE,
    time TIMESTAMP,
    temperature DOUBLE,
    humidity DOUBLE,
    PRIMARY KEY ((sensor_id, date), time)
);
```

- **Partition Key** `(sensor_id, date)`: определяет на каком узле данные
- **Clustering Key** `time`: определяет сортировку внутри партиции

Данные внутри партиции отсортированы по clustering key — можно эффективно делать range queries по `time`.

## CQL (Cassandra Query Language)

Похож на SQL, но с ограничениями:

```sql
-- Работает (partition + clustering key)
SELECT * FROM sensor_data
WHERE sensor_id = ? AND date = ? AND time > ?;

-- НЕ работает (нет partition key)
SELECT * FROM sensor_data WHERE temperature > 30;

-- НЕ работает (нет ALLOW FILTERING)
SELECT * FROM sensor_data WHERE sensor_id = ? AND humidity > 50;
```

**Золотое правило Cassandra**: моделируй данные под запросы. Если нужен запрос по `temperature` — создай другую таблицу или материализованное представление.

## Consistency Levels

Настраивается **на каждый запрос**:

```cql
CONSISTENCY QUORUM;  -- большинство реплик подтверждают
```

| Уровень | Чтение | Запись |
|---------|--------|--------|
| ONE | Ответ от 1 реплики | Запись на 1 реплику |
| QUORUM | Большинство реплик | Большинство реплик |
| ALL | Все реплики | Все реплики |
| LOCAL_QUORUM | Большинство в локальном ДЦ | Большинство в локальном ДЦ |

### Формула консистентности

Если `R + W > RF` (Replication Factor), получаем **сильную консистентность**.
- RF=3, R=2, W=2 → 2+2 > 3 ✓ (strong consistency)
- RF=3, R=1, W=1 → 1+1 < 3 (eventual consistency)

## Когда Cassandra — правильный выбор

- Огромные объёмы записей (миллионы в секунду)
- Известные паттерны запросов (знаем partition key)
- Геораспределённость (несколько дата-центров)
- Высокая доступность (нет single point of failure)
- Временные ряды, IoT, логи, метрики

## Когда Cassandra НЕ подходит

- Ad-hoc запросы и аналитика (нет гибких WHERE/JOIN/агрегаций)
- Сложные транзакции (нет ACID в масштабе партиций)
- Часто меняющиеся запросы (модель заточена под конкретные запросы)
- Небольшие данные (переусложнение)

## ScyllaDB

Современная C++ переработка Cassandra. Совместима по API, в 5-10× быстрее. Если выбираешь Cassandra сегодня — смотри на ScyllaDB.

## Связанные страницы

- [[../05-databases-nosql/nosql-taxonomy|NoSQL-таксономия]]
- [[../05-databases-nosql/cap-theorem|CAP-теорема]]
- [[../10-big-data/data-lake-architecture|Data Lake]]
