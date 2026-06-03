# MySQL / InnoDB Deep Dive

## Место MySQL в экосистеме

MySQL — самая популярная open-source БД для веб-приложений. InnoDB — стандартный движок (с 5.5).

## MySQL vs PostgreSQL — ключевые отличия

| | MySQL | PostgreSQL |
|---|---|---|
| **Модель процессов** | Потоки (threads) | Процессы (processes) |
| **MVCC** | Через undo log в tablespace | Через хранение версий в куче |
| **Транзакции** | Read-Uncommitted до 5.5 | Read-Committed всегда |
| **JSON** | JSON (свой формат) | JSONB (бинарный, с индексами) |
| **Полнотекстовый поиск** | Встроенный (InnoDB) | Через расширения |
| **Гео-данные** | Базовая поддержка | PostGIS (мощный стандарт) |
| **Репликация** | Statement/Row/Mixed | Streaming WAL |
| **Расширения** | Plugins (сложнее) | Extensions (проще) |
| **SQL-стандарт** | Расслабленный режим по умолчанию | Строгий |

## InnoDB — архитектура

```
InnoDB Buffer Pool
├── Data Pages (строки, индексы)
├── Adaptive Hash Index
├── Change Buffer (для вторичных индексов)
├── Undo Log
└── Redo Log (аналог WAL в Postgres)
```

### Buffer Pool

- **Главный кэш**. Хранит страницы данных и индексов.
- Размер: до 80% RAM на выделенном сервере.
- LRU с защитой от вымывания (midpoint insertion).

### Doublewrite Buffer

Защита от «torn pages» (частичная запись страницы после краха). Сначала пишет в doublewrite buffer, потом в основную таблицу. Дорого, но надёжно.

### Redo Log

Аналог WAL. Групповой сброс (group commit) для производительности. Размер фиксированный (`innodb_log_file_size`).

## Движки хранения

| Движок | Для чего |
|--------|----------|
| **InnoDB** | Основной: ACID, MVCC, FK, row-level locking |
| **MyISAM** | Устарел. Без транзакций. Только table-level locking |
| **Memory** | В памяти, hash-индексы. Для временных данных и кэшей |
| **Archive** | Сжатие, только INSERT/SELECT. Для логов |

## Особенности, о которых надо знать

### SQL Mode

По умолчанию MySQL прощает многое:
```sql
SELECT 'hello' / 2;  -- вернёт 0, а не ошибку!
```

Всегда включай строгий режим:
```sql
SET sql_mode = 'STRICT_TRANS_TABLES,ONLY_FULL_GROUP_BY,NO_ZERO_DATE';
```

### ONLY_FULL_GROUP_BY

Без этого флага MySQL позволяет:
```sql
SELECT user_id, COUNT(*) FROM orders GROUP BY user_id;
-- вернёт случайный user_id из группы!
```

### Кодировки

По умолчанию `latin1` в старых версиях. Всегда явно указывай `utf8mb4`.

## Репликация

| Тип | Принцип | Плюсы | Минусы |
|-----|---------|-------|--------|
| **Statement-based** | Пишет SQL-запросы | Компактно | Недетерминированные функции |
| **Row-based** | Пишет изменения строк | Детерминировано | Больше данных |
| **Mixed** | Комбинация | Компромисс | Сложность |

### GTID (Global Transaction ID)

Упрощает failover: каждая транзакция имеет глобальный ID, реплика знает какие транзакции уже применены.

## Индексы в InnoDB

### Clustered Index

**Главное отличие от Postgres**: первичный ключ — это clustered index. Строки хранятся в B-Tree, упорядоченные по PK.

- PK = данные. Вторичные индексы хранят PK как указатель на строку.
- PK должен быть коротким и монотонно возрастающим (AUTO_INCREMENT или UUID v7)
- Случайный UUID как PK = fragmented B-Tree = боль

## Когда выбирать MySQL

- LAMP/LEMP-стек
- Простые веб-приложения
- Read-heavy workload с репликацией
- Совместимость с существующей инфраструктурой (WordPress, Magento)

## Когда выбирать PostgreSQL

См. [[../03-databases-relational/postgresql-deep-dive|PostgreSQL Deep Dive]].

## Связанные страницы

- [[../03-databases-relational/postgresql-deep-dive|PostgreSQL Deep Dive]]
- [[../03-databases-relational/transactions-and-acid|Транзакции и ACID]]
- [[../03-databases-relational/indexing-internals|Индексы]]
