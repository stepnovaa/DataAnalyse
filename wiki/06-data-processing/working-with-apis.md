# Работа с API для сбора данных

## Модели API

| Тип | Как работает | Пример |
|-----|-------------|--------|
| **REST** | HTTP-методы (GET/POST), JSON | Большинство API |
| **GraphQL** | Один endpoint, клиент запрашивает нужные поля | GitHub API v4 |
| **gRPC** | Бинарный протокол, быстрее REST | Внутренние сервисы |
| **WebSocket** | Двустороннее постоянное соединение | Real-time данные |
| **SOAP** | XML, legacy | Enterprise-системы |

## REST API — базовая работа

```python
import requests

resp = requests.get(
    'https://api.example.com/v1/orders',
    headers={'Authorization': 'Bearer TOKEN'},
    params={'since': '2024-01-01', 'limit': 100}
)
resp.raise_for_status()  # исключение при 4xx/5xx
data = resp.json()
```

## Аутентификация

| Метод | Как | Пример |
|-------|-----|--------|
| **API Key** | В заголовке или параметре | `X-API-Key: abc123` |
| **Bearer Token** | OAuth 2.0 | `Authorization: Bearer <token>` |
| **Basic Auth** | Base64(user:pass) | `Authorization: Basic dXNlcjpwYXNz` |
| **OAuth 2.0** | Трёхсторонний flow | Google, GitHub, etc. |

## Пагинация

### Offset-based

```python
params = {'offset': 0, 'limit': 100}
while True:
    resp = requests.get(url, params=params)
    data = resp.json()
    if not data:
        break
    all_data.extend(data)
    params['offset'] += len(data)
```

### Cursor-based (более надёжная)

```python
params = {'limit': 100}
while True:
    resp = requests.get(url, params=params)
    data = resp.json()
    all_data.extend(data['items'])
    if 'next_cursor' not in data:
        break
    params['cursor'] = data['next_cursor']
```

### Link Header (RFC 5988)

```python
import requests
resp = requests.get(url)
while resp.links.get('next'):
    resp = requests.get(resp.links['next']['url'])
```

## Rate Limiting

```python
import time

def rate_limited_get(url, max_retries=5):
    for attempt in range(max_retries):
        resp = requests.get(url)
        if resp.status_code == 429:
            wait = int(resp.headers.get('Retry-After', 60))
            print(f'Rate limited, waiting {wait}s (attempt {attempt+1})')
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp
    raise Exception('Max retries exceeded')
```

Всегда проверяй `X-RateLimit-Remaining` если API его отдаёт.

## Надёжная интеграция (best practices)

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=5, backoff_factor=1,
              status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retry))

# Используй сессию для connection pooling
resp = session.get(url, timeout=30)  # всегда ставь таймаут
```

### Чек-лист надёжности

1. **Timeout**: всегда. `timeout=30`. Connection timeout + read timeout.
2. **Retry**: 429 (rate limit) и 5xx с экспоненциальной задержкой
3. **Логирование**: что запросил, что получил, сколько заняло
4. **Идемпотентность**: если сбор упал на середине, перезапуск не должен дублировать
5. **Инкрементальная загрузка**: запрашивать только новые данные (`since=last_run`)

## GraphQL

```python
query = """
query {
  repository(owner: "pandas-dev", name: "pandas") {
    stargazers { totalCount }
    issues(states: OPEN, first: 5) {
      nodes {
        title
        createdAt
      }
    }
  }
}
"""
resp = requests.post('https://api.github.com/graphql',
    json={'query': query},
    headers={'Authorization': 'Bearer TOKEN'})
```

**Плюсы**: запрашиваешь только нужные поля, нет over-fetching.
**Минусы**: сложнее кэшировать (всегда POST), нет простого rate limiting по URL.

## Связанные страницы

- [[../06-data-processing/etl-vs-elt|ETL vs ELT]]
- [[../06-data-processing/data-pipelines-orchestration|Оркестрация пайплайнов]]
- [[../10-big-data/kafka-data-streaming|Kafka]] — для стриминга через API
