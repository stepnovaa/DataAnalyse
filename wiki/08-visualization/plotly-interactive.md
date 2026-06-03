# Plotly — интерактивная визуализация

## Plotly vs Matplotlib

| | Matplotlib | Plotly |
|---|---|---|
| **Вид** | Статический | Интерактивный |
| **Стиль** | Академический | Современный |
| **Кривая обучения** | Крутая | Пологий старт |
| **Производительность** | Быстрая | Медленнее на больших данных |
| **Экспорт** | PNG, PDF, SVG | HTML, PNG (через kaleido) |
| **Когда** | Публикации, отчёты | Дашборды, исследование данных |

## Plotly Express (высокоуровневый API)

```python
import plotly.express as px

# Scatter
px.scatter(df, x='price', y='sales', color='category',
           size='quantity', hover_data=['name'])

# Line
px.line(df, x='date', y='revenue', color='product',
        line_dash='region')

# Bar
px.bar(df, x='category', y='revenue', color='year', barmode='group')

# Histogram
px.histogram(df, x='price', nbins=50, color='category', marginal='box')

# Box
px.box(df, x='category', y='price', color='region')

# Heatmap
px.imshow(df.corr(), text_auto='.2f', aspect='auto')

# Map
px.scatter_mapbox(df, lat='lat', lon='lon', color='value', size='count',
                   mapbox_style='carto-darkmatter', zoom=3)

# Pie (ладно, вот pie, но лучше bar)
px.pie(df, names='category', values='revenue', hole=0.3)  # donut
```

## Plotly Graph Objects (низкоуровневый API)

```python
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['date'], y=df['revenue'],
                         mode='lines+markers', name='Revenue'))
fig.update_layout(
    title='Revenue Over Time',
    xaxis_title='Date',
    yaxis_title='Revenue ($)',
    template='plotly_dark',
    hovermode='x unified'
)
```

## Интерактивность

### Встроенная

- **Hover**: информация при наведении — настраивается `hover_data`
- **Zoom**: выделение области мышкой
- **Pan**: перетаскивание графика
- **Legend кликабельна**: скрыть/показать серии

### Кнопки и выпадающие списки

```python
fig.update_layout(
    updatemenus=[dict(
        type='buttons',
        buttons=[
            dict(label='Linear', method='update', args=[{'type': 'scatter'}]),
            dict(label='Log', method='update', args=[{'yaxis': {'type': 'log'}}]),
        ]
    )]
)
```

## Dash — дашборды на Plotly

```python
import dash
from dash import dcc, html

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(options=['A', 'B', 'C'], value='A', id='dropdown'),
    dcc.Graph(id='chart')
])
```

См. [[../08-visualization/dashboard-design|Дизайн дашбордов]].

## Экспорт

```python
# Статический PNG (нужен kaleido: pip install kaleido)
fig.write_image('chart.png', width=1200, height=800, scale=2)

# Интерактивный HTML
fig.write_html('chart.html')

# В Jupyter — просто `fig.show()` — интерактивный
```

## Связанные страницы

- [[../08-visualization/matplotlib-seaborn|Matplotlib + Seaborn]]
- [[../08-visualization/dashboard-design|Дизайн дашбордов]]
- [[../08-visualization/bi-tools-landscape|BI-инструменты]]
