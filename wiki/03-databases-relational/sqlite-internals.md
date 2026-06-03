# SQLite — архитектура

## Что такое SQLite

**Встроенная (embedded) реляционная БД.** Не клиент-сервер — библиотека, которая читает и пишет в один файл. Самая распространённая БД в мире (в каждом телефоне, браузере, приложении).

## Когда SQLite — правильный выбор

- Локальное хранение (мобильные приложения, десктоп)
- Embedded-устройства, IoT
- Анализ данных на локальной машине (один пользователь)
- Прототипирование и тестирование
- Замена файлового хранения (конфиги, кэш)
- Небольшие веб-приложения (one-writer, many-readers)

## Когда SQLite НЕ подходит

- Высокая конкурентность записи (один writer в моменте)
- Много пользователей пишут одновременно (клиент-сервер БД лучше)
- Очень большие данные (терабайты — хотя SQLite справляется с десятками ГБ)
- Нужна сетевая репликация

## Архитектура

```
SQL команда
    ↓
Tokenizer → Parser → Code Generator → Virtual Machine
                                            ↓
                                       B-Tree (VDBE)
                                            ↓
                                   Pager (кеш страниц)
                                            ↓
                                      OS Interface
                                            ↓
                                   Файл .sqlite
```

### VDBE (Virtual Database Engine)

SQL компилируется в байткод, исполняемый виртуальной машиной. Быстро, портабельно, детерминировано.

### Pager

Управляет чтением/записью страниц, кэшированием, блокировками и транзакциями. B-Tree работает поверх Pager.

## Типы данных (манифестная типизация)

SQLite динамически типизирован — тип хранится со значением, а не с колонкой:

```sql
CREATE TABLE t (x INTEGER);
INSERT INTO t VALUES (42), ('hello'), (3.14);  -- всё работает!
```

**Storage classes** (не типы колонок!): NULL, INTEGER, REAL, TEXT, BLOB.

**Type affinity**: колонка имеет «предпочтение», но не ограничение.

> Это мощно для прототипирования, но боль в production. Используй STRICT tables (SQLite 3.37+):
> ```sql
> CREATE TABLE t (x INTEGER) STRICT;
> ```

## WAL Mode (Write-Ahead Log)

По умолчанию SQLite использует rollback journal. Включи WAL:

```sql
PRAGMA journal_mode = WAL;
```

- Читатели не блокируют писателя
- Писатель не блокирует читателей
- Быстрее для конкурентных read/write

## Производительность

### Прагмы, которые стоит включить

```sql
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;     -- безопасно в WAL mode
PRAGMA cache_size = -8000;       -- 8MB кэш (отрицательное = KB)
PRAGMA busy_timeout = 5000;      -- ждать 5с вместо мгновенной ошибки
PRAGMA foreign_keys = ON;        -- FK отключены по умолчанию!
```

### Одновременная запись

SQLite блокирует всю БД на запись. Много concurrent writers = плохо. Но для single-writer/many-readers — отлично.

## SQLite для аналитики

Современный SQLite — неплохой движок для локальной аналитики:
- Импорт CSV: `.import --csv file.csv table`
- Оконные функции (с 3.25)
- CTE (с 3.8.3)
- JSON-функции
- Полнотекстовый поиск (FTS5)
- До ~281 ТБ максимальный размер БД

Но для серьёзной OLAP-аналитики лучше [[../10-big-data/duckdb-local-analytics|DuckDB]].

## Связанные страницы

- [[../03-databases-relational/postgresql-deep-dive|PostgreSQL]] — сравнение
- [[../10-big-data/duckdb-local-analytics|DuckDB]] — OLAP-альтернатива
- [[../04-sql/sql-basics|SQL — Основы]]
