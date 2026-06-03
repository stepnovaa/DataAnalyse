# Графовые БД — Neo4j

## Зачем графы

Реляционные БД отлично справляются с данными, организованными в таблицы. Но когда связи между сущностями так же важны, как сами сущности — графы эффективнее.

### Реляционный подход: «Друзья друзей на глубину 3»

```sql
WITH RECURSIVE friends AS (
    SELECT friend_id, 1 AS depth FROM friendships WHERE user_id = 1
    UNION ALL
    SELECT f.friend_id, depth + 1
    FROM friendships f JOIN friends ON f.user_id = friends.friend_id
    WHERE depth < 3
)
SELECT DISTINCT friend_id FROM friends;
```

На большом графе — часы выполнения.

### Графовый подход (Cypher):

```cypher
MATCH (u:User {id: 1})-[:FRIEND*1..3]-(friend)
RETURN DISTINCT friend
```

Миллисекунды на миллионах узлов.

## Модель данных

Граф = **узлы** (Nodes) + **рёбра** (Relationships). И те и другие могут иметь свойства.

```cypher
// Узлы
(:Person {name: "Alice", age: 30})
(:Company {name: "Acme Inc", founded: 1990})
(:City {name: "Moscow"})

// Рёбра
(:Person)-[:WORKS_AT {since: 2020}]->(:Company)
(:Person)-[:LIVES_IN]->(:City)
(:Person)-[:KNOWS {since: 2015}]->(:Person)
```

## Cypher — язык запросов

Декларативный язык, напоминающий ASCII-арт:

```cypher
// Кто работает в компании, основанной после 2010?
MATCH (p:Person)-[:WORKS_AT]->(c:Company)
WHERE c.founded > 2010
RETURN p.name, c.name

// Кратчайший путь между двумя людьми
MATCH path = shortestPath(
  (alice:Person {name: "Alice"})-[*]-(bob:Person {name: "Bob"})
)
RETURN path

// Рекомендации: люди, которые знают моих друзей, но не меня
MATCH (me:Person {name: "Alice"})-[:KNOWS]->(friend)-[:KNOWS]->(fof)
WHERE NOT (me)-[:KNOWS]-(fof)
RETURN fof.name, COUNT(*) AS common_friends
ORDER BY common_friends DESC
```

## Когда графы эффективнее SQL

| Задача | SQL | Cypher |
|--------|-----|--------|
| Друзья друзей (глубина 3) | Рекурсивный CTE, часы | Миллисекунды |
| Кратчайший путь | Почти невозможно | `shortestPath()` |
| Рекомендации | Много JOIN'ов | Простой обход |
| Поиск циклов | Очень сложно | Встроенные алгоритмы |

## Графовые алгоритмы (GDS Library)

Neo4j Graph Data Science library:

- **Centrality**: PageRank, Betweenness
- **Community Detection**: Louvain, Label Propagation
- **Pathfinding**: Dijkstra, A*, Yen's k-shortest paths
- **Similarity**: Node Similarity, KNN

## Когда графы — правильный выбор

- Социальные сети, рекомендательные системы
- Выявление мошенничества (связи между аккаунтами)
- Управление зависимостями (Bill of Materials)
- Network/IT-инфраструктура (что на чём запущено)
- knowledge graphs

## Когда графы НЕ подходят

- Простые CRUD-операции (список пользователей)
- Аналитика агрегатов (суммы, средние)
- Данные без сложных связей
- Когда команда не готова учить Cypher и графовую модель

## Альтернативы Neo4j

- **ArangoDB**: multi-model (документы + графы)
- **Amazon Neptune**: managed, поддерживает Gremlin и SPARQL
- **PostgreSQL + рекурсивные CTE**: для простых графовых запросов
- **NetworkX** (Python библиотека): для in-memory анализа графов

## Связанные страницы

- [[../05-databases-nosql/nosql-taxonomy|NoSQL-таксономия]]
- [[../05-databases-nosql/nosql-vs-sql-decision|NoSQL vs SQL]]
- [[../04-sql/ctes-and-recursive|Рекурсивные CTE в SQL]]
