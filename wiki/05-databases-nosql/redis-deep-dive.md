# Redis Deep Dive

## Что такое Redis

**In-memory** data structure store. Не просто key-value — а сервер структур данных. Используется как кэш, брокер сообщений, очередь, счётчик, база данных.

## Модель данных

Redis — не «ключ → строка», а «ключ → структура данных»:

| Тип | Структура | Пример использования |
|-----|-----------|---------------------|
| **String** | Строка / число | Кэш, счётчики, сессии |
| **List** | Связный список | Очередь, лента новостей |
| **Set** | Множество уникальных | Теги, друзья, online-пользователи |
| **Sorted Set** | Множество + score | Рейтинг, лидерборды |
| **Hash** | Ассоциативный массив | Профиль пользователя, объект |
| **Stream** | Append-only лог | Event sourcing, Kafka-light |
| **Geospatial** | Координаты | «Найти аптеки в радиусе 5 км» |
| **Bitmap / HyperLogLog** | Битовые операции | Уникальные посетители, флаги |

## Основные операции

```redis
# Strings
SET user:1:name "Alice"
GET user:1:name
INCR page:views
SETEX session:token 3600 "data"   # с TTL

# Lists
LPUSH queue:tasks "task1"
RPOP queue:tasks

# Sets
SADD user:1:tags "python" "sql" "analytics"
SINTER user:1:tags user:2:tags   # общие теги

# Sorted Sets
ZADD leaderboard 1000 "player1" 950 "player2"
ZREVRANGE leaderboard 0 9        # топ-10

# Hashes
HSET user:1 name "Alice" email "alice@mail.com"
HGET user:1 name
HGETALL user:1
```

## Persistence (сохранение на диск)

| Метод | Как работает | Плюсы | Минусы |
|-------|-------------|-------|--------|
| **RDB** | Снапшот через N секунд | Компактно, быстрое восстановление | Можно потерять данные между снапшотами |
| **AOF** | Лог всех операций | Минимальные потери | Большой файл, медленное восстановление |
| **RDB + AOF** | Комбинация | Лучшее из двух | Сложнее |

## Когда Redis — правильный выбор

- **Кэширование**: горячие данные, результаты запросов, HTML-фрагменты
- **Сессии**: быстрый доступ + TTL = автоочистка
- **Счётчики и rate limiting**: атомарный INCR
- **Очереди задач**: Lists + BRPOP/BRPOPLPUSH
- **Pub/Sub**: мгновенная доставка сообщений
- **Leaderboards**: Sorted Sets
- **Real-time аналитика**: HyperLogLog для уникальных посетителей

## Когда Redis НЕ подходит

- Основное хранилище больших данных (дорого — память)
- Сложные запросы (нет SQL, JOIN'ов, агрегаций)
- Данные, которые должны пережить перезагрузку без потерь (можно, но не основное назначение)
- Большие бинарные объекты (Redis не для BLOB'ов)

## Паттерны использования

### Cache-Aside

```
Приложение → Redis (есть?) → нет → БД → Redis (сохранить) → Приложение
```

### Счётчик с окном (rate limit)

```redis
MULTI
INCR user:123:requests
EXPIRE user:123:requests 60
EXEC
```

### Distributed Lock (Redlock)

```redis
SET lock:resource_name unique_value NX PX 30000
-- ...
-- освобождение через Lua-скрипт (проверка unique_value)
```

## Кластеризация

- **Redis Sentinel**: мониторинг, failover, без шардирования
- **Redis Cluster**: шардирование по hash slots (16384 слота)

## Связанные страницы

- [[../05-databases-nosql/nosql-vs-sql-decision|NoSQL vs SQL]]
- [[../05-databases-nosql/mongodb-deep-dive|MongoDB]]
- [[../10-big-data/kafka-data-streaming|Kafka]] — для серьёзного стриминга
