# CLI-инструменты для данных

## Зачем CLI

GUI — для исследования. CLI — для автоматизации и скорости. Ты можешь встроить CLI в пайплайны и скрипты.

## Универсальные

### csvkit — швейцарский нож для CSV

```bash
pip install csvkit

csvlook data.csv | head           # красивая таблица в терминале
csvcut -c name,price data.csv     # выбрать колонки
csvgrep -c status -m active data.csv  # фильтрация
csvstat data.csv                  # статистика (min, max, unique, null)
csvsql --query "SELECT ..." data.csv  # SQL к CSV!
csvjoin -c id users.csv orders.csv    # JOIN двух CSV
```

### xsv (Rust, быстрее csvkit)

```bash
cargo install xsv

xsv select name,price data.csv
xsv search -s status active data.csv
xsv frequency data.csv --limit 10    # топ значений
xsv sample 1000 data.csv             # сэмпл
xsv stats data.csv                   # статистика
```

### Miller (mlr)

```bash
apt install miller

# Обработка CSV/JSON как awk для структурированных данных
mlr --csv filter '$price > 100' data.csv
mlr --csv put '$tax = $price * 0.2' data.csv
mlr --csv stats1 -a mean,min,max -f price data.csv
mlr --csv group-by category then count data.csv
```

## JSON

### jq — awk для JSON

```bash
# Извлечь поле
curl -s https://api.example.com/data | jq '.results'

# Фильтрация
jq '.items[] | select(.price > 100)'

# Трансформация в CSV
jq -r '.items[] | [.name, .price] | @csv'
```

## DuckDB CLI

```bash
duckdb

# Прямой запрос к файлам!
SELECT category, COUNT(*) FROM 'data/*.parquet' GROUP BY 1;

# Импорт CSV в таблицу
CREATE TABLE orders AS SELECT * FROM 'orders.csv';
```

## VisiData — интерактивный терминал

```bash
pip install visidata
vd data.csv  # интерактивный просмотр, сортировка, фильтрация, графики
```

Как Excel, но в терминале. Для быстрого просмотра данных без GUI.

## Дата-пайплайн в одну строку

```bash
# Скачать, отфильтровать, посчитать, сохранить
curl -s https://api.example.com/data   | jq '.items[] | select(.price > 100) | [.name, .price] | @csv'   | duckdb -c "
      CREATE TABLE items AS SELECT * FROM read_csv_auto('/dev/stdin');
      COPY (SELECT name, AVG(price) FROM items GROUP BY name) TO 'result.csv';
    "
```

## Минимальный набор

```bash
pip install csvkit duckdb visidata
cargo install xsv         # или apt install xsv (если есть в репах)
apt install jq miller
```

## Связанные страницы

- [[../13-toolbox/sql-ides-and-clients|SQL IDE]]
- [[../06-data-processing/data-wrangling-python|Data Wrangling — Python]]
- [[../10-big-data/duckdb-local-analytics|DuckDB]]
