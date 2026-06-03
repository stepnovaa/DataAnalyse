# Векторные базы данных

## Зачем

LLM, поиск по изображениям, рекомендации — всё это требует поиска **похожих** объектов. Векторные БД хранят embeddings (числовые векторы) и ищут ближайших соседей.

## Как работает

```
Текст/изображение → Embedding Model → Вектор [0.1, -0.3, 0.7, ...] → Vector DB
                                                                          ↓
                                                              Поиск: cosine similarity
```

### Меры близости

| Метрика | Формула | Когда |
|---------|---------|-------|
| **Cosine Similarity** | cos(θ) = A·B / (|A|·|B|) | Текст, embeddings (стандарт) |
| **Euclidean Distance** | √Σ(Aᵢ - Bᵢ)² | Когда важна магнитуда |
| **Dot Product** | A·B | Когда векторы нормализованы |

## Инструменты

### Специализированные

| | Pinecone | Qdrant | Weaviate | Milvus |
|---|---|---|---|---|
| **Тип** | Managed Cloud | Open-source + Cloud | Open-source + Cloud | Open-source |
| **Язык** | REST/gRPC | REST/gRPC | GraphQL/REST | REST/gRPC |
| **Фильтрация** | Метаданные | Метаданные | Метаданные + гибридный поиск | Метаданные |
| **Когда** | Самый простой managed | Self-hosted, гибкий | Гибридный поиск (BM25 + вектор) | Большие объёмы (>1B векторов) |

### pgvector (PostgreSQL extension)

```sql
CREATE EXTENSION vector;
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(1536)  -- OpenAI ada-002
);

-- Поиск по сходству
SELECT content, 1 - (embedding <=> query_embedding) AS similarity
FROM documents
ORDER BY embedding <=> query_embedding
LIMIT 10;

-- Индекс
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);
```

**Когда pgvector достаточно**:
- < 10M векторов
- Уже используешь PostgreSQL
- Нужна простая интеграция (JOIN с реляционными данными)

**Когда переходить на специализированную**:
- > 10M векторов (pgvector медленнее)
- Нужна низкая latency (< 10ms)
- Нужны продвинутые фичи (гибридный поиск, мультитенантность)

## Embedding-модели

```python
# OpenAI
from openai import OpenAI
client = OpenAI()
embedding = client.embeddings.create(input='текст', model='text-embedding-3-small')

# Open-source (локально)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('intfloat/multilingual-e5-large')
embedding = model.encode('текст')
```

## RAG (Retrieval-Augmented Generation)

Архитектура, где LLM использует векторную БД для поиска релевантного контекста:

```
Вопрос → Embedding → Поиск в Vector DB → Релевантные документы → LLM + контекст → Ответ
```

## Связанные страницы

- [[../12-modern-trends/llm-for-data-analysis|LLM в аналитике]]
- [[../05-databases-nosql/nosql-taxonomy|NoSQL-таксономия]]
- [[../03-databases-relational/postgresql-deep-dive|PostgreSQL Deep Dive]]
