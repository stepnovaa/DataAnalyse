# Паттерны моделирования данных

## OLTP vs OLAP моделирование

| | OLTP (транзакции) | OLAP (аналитика) |
|---|---|---|
| **Цель** | Быстрая запись/чтение отдельных записей | Быстрые агрегации и отчёты |
| **Нормализация** | 3НФ | Денормализация |
| **Схема** | Нормализованная | Звезда / Снежинка |
| **Обновления** | Частые, мелкие | Редкие, batch |
| **Пример** | Заказы в интернет-магазине | Анализ продаж за год |

## Паттерны для OLTP

### Звезда (Star Schema)

```
       dim_date        dim_product
           \            //
            fact_sales
           //            \
    dim_customer      dim_store
```

- **Факты** (fact): числовые измерения, которые агрегируем (сумма продаж, количество)
- **Измерения** (dimension): контекст, по которому режем (дата, товар, покупатель, магазин)
- **Плюсы**: простые JOIN'ы, быстрые запросы, понятная структура
- **Минусы**: денормализация — избыточность в измерениях

### Снежинка (Snowflake Schema)

```
       dim_date        dim_category
           \              /
            dim_product
                 \
              fact_sales
               //        \
    dim_customer      dim_store
         |                |
    dim_city         dim_region
```

Нормализованные измерения. Меньше избыточности — больше JOIN'ов.

### Data Vault

Для enterprise хранилищ со сложной историей изменений:
- **Hub**: уникальные бизнес-ключи (Customer, Product)
- **Link**: связи между хабами (Transaction)
- **Satellite**: атрибуты и их история во времени

## Паттерны для OLTP

### EAV (Entity-Attribute-Value)

```sql
-- Вместо:
CREATE TABLE products (id, name, price, color, weight);
-- Делают:
CREATE TABLE product_attrs (product_id, attr_name, attr_value);
```

**Плюсы**: гибкость, не надо ALTER TABLE под новые атрибуты.
**Минусы**: сложные запросы, нет типизации, плохая производительность.

> Почти всегда антипаттерн. Используй JSONB в Postgres, если нужна гибкая схема.

### Наследование (Table Inheritance)

**Single Table Inheritance:**
```sql
CREATE TABLE vehicles (id, type, wheels, wing_span, cargo_capacity);
-- type = 'car' → wing_span = NULL
-- type = 'plane' → cargo_capacity = NULL
```

**Class Table Inheritance:**
```sql
CREATE TABLE vehicles (id, type);
CREATE TABLE cars (vehicle_id, wheels);
CREATE TABLE planes (vehicle_id, wing_span);
```

**Concrete Table Inheritance:**
```sql
CREATE TABLE cars (id, wheels);
CREATE TABLE planes (id, wing_span);
```

### Связи многие-ко-многим

```sql
CREATE TABLE student_courses (
    student_id INT REFERENCES students(id),
    course_id  INT REFERENCES courses(id),
    enrolled_at TIMESTAMP,
    PRIMARY KEY (student_id, course_id)
);
```

Всегда добавляй временную метку и другие атрибуты связи в junction-таблицу.

### Медленно меняющиеся измерения (SCD)

| Тип | Стратегия |
|-----|-----------|
| **SCD Type 1** | Перезаписываем. Истории нет. |
| **SCD Type 2** | Новая строка + effective_date/expiry_date. Полная история. |
| **SCD Type 3** | Добавляем колонку previous_value. Ограниченная история. |

Для аналитики обычно нужен SCD Type 2.

## Связанные страницы

- [[../03-databases-relational/normalization|Нормализация]]
- [[../03-databases-relational/relational-model|Реляционная модель]]
- [[../11-data-engineering/data-warehouse-architecture|Архитектура хранилищ]]
