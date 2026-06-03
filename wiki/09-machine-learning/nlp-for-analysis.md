# NLP для аналитики

## Зачем аналитику NLP

Много данных — текст: отзывы, комментарии, тикеты поддержки, чаты. NLP превращает текст в числа, с которыми можно работать аналитическими методами.

## Базовые техники

### Предобработка текста

```python
import re
# Нижний регистр, удаление пунктуации, лишних пробелов
text = re.sub(r'[^\w\s]', '', text.lower()).strip()
```

### Tokenization

```python
from nltk.tokenize import word_tokenize
tokens = word_tokenize(text)
```

### Стоп-слова

```python
from nltk.corpus import stopwords
stop_words = set(stopwords.words('russian'))
tokens = [t for t in tokens if t not in stop_words]
```

### Частотный анализ

```python
from collections import Counter
word_freq = Counter(tokens).most_common(20)
```

### Word Clouds

```python
from wordcloud import WordCloud
wc = WordCloud(width=800, height=400, background_color='white')
wc.generate(' '.join(tokens))
```

## Анализ тональности (Sentiment)

```python
from textblob import TextBlob
# Для английского
polarity = TextBlob(text).sentiment.polarity  # -1 (нег.) до +1 (поз.)

# Для русского — Dostoevsky (трансформеры)
from transformers import pipeline
classifier = pipeline('sentiment-analysis', model='blanchefort/rubert-base-cased-sentiment')
result = classifier(text)
```

## Тематическое моделирование (Topic Modeling)

### LDA (Latent Dirichlet Allocation)

```python
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(max_features=1000)
X = vectorizer.fit_transform(texts)

lda = LatentDirichletAllocation(n_components=5, random_state=42)
lda.fit(X)

# Топ-слова для каждой темы
for i, topic in enumerate(lda.components_):
    top_words = [vectorizer.get_feature_names_out()[j] for j in topic.argsort()[-10:]]
    print(f'Topic {i}: {top_words}')
```

### BERTopic (современный подход)

```python
from bertopic import BERTopic
model = BERTopic(language='russian')
topics, _ = model.fit_transform(texts)
```

## Извлечение именованных сущностей (NER)

```python
import spacy
nlp = spacy.load('ru_core_news_sm')
doc = nlp('Apple купила стартап в Москве за $1 млрд')
for ent in doc.ents:
    print(ent.text, ent.label_)  # Apple ORG, Москва LOC, $1 млрд MONEY
```

## Когда NLP в аналитике

- **Анализ отзывов**: о чём пишут? довольны или нет?
- **Классификация тикетов**: автоматическая маршрутизация
- **Поиск инсайтов**: что чаще всего упоминают клиенты?
- **Извлечение данных**: цены, даты, имена из текста

## Современные LLM-подходы

См. [[../12-modern-trends/llm-for-data-analysis|LLM в аналитике]] — современный способ делать NLP без обучения моделей.

## Связанные страницы

- [[../09-machine-learning/supervised-learning|Обучение с учителем]] — классификация текстов
- [[../12-modern-trends/llm-for-data-analysis|LLM в аналитике]]
- [[../06-data-processing/data-cleaning|Очистка данных]] — чистка текстов
