```python
import plotly 
import chart_studio.plotly as py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
#pio.renderers.default = "iframe_connected"
import IPython
from IPython.display import IFrame
from IPython.display import HTML, display
```

## Downloading and combining latest data


```python
%run ./data_collection/00-daily-download.py
```


```python
%run ./data_collection/01-daily-combine.py
```

## Load data


```python
df = pd.read_csv('./data/combined/combined.csv')
```

## Create Variables


```python
df['text'] = df['state'].astype(str) + '\n' + 'Positive: ' + df['positive'].astype(str) + ', ' + 'Deaths: '+ df['death'].astype(str) + ', ' + 'Negative: '+ df['negative'].astype(str) + ', ' + 'Total Tested: '+ df['total'].astype(str)
df = df[df['state'] !=("GU")]
df = df[df['state'] !=("PR")]
df = df[df['state'] !=("AS")]
df = df[df['state'] !=("MP")]
df = df[df['state'] !=("PRI")]
df = df[df['state'] !=("VIR")]
df = df[df['state'] !=("VI")]
```


```python
def calculate_num_claims_since_emergency_declaration(x: pd.DataFrame) -> int:    
    declaration_date = x["Emergency Declaration Date"].values[0]
    return x[x.date >= declaration_date].number_of_iclaims.sum()

```


```python
iclaims_since_emergency_by_state = df.groupby("state").apply(calculate_num_claims_since_emergency_declaration)
```


```python
df['iclaims_since_emergency'] = df.state.apply(
    lambda x: iclaims_since_emergency_by_state[x] if x in iclaims_since_emergency_by_state else None)
```


```python
def calculate_num_claims_since_stayathome_order(x: pd.DataFrame) -> int:    
    stayathome_date = x["Stay At Home Order Date"].values[0]
    return x[x.date >= stayathome_date].number_of_iclaims.sum()
iclaims_since_stayathome_by_state = df.groupby("state").apply(calculate_num_claims_since_stayathome_order)
```


```python
df['iclaims_since_stayathome'] = df.state.apply(lambda x: iclaims_since_stayathome_by_state[x] if x in iclaims_since_stayathome_by_state else None)

```


```python
df = df.sort_values(by=['date'])
df = df[df["date"]>="2020-01-30"]
df = df[df["death"].isna()==False]
df = df[df["positive"].isna()==False]
df['pct_death_over_positive'] = 100*(df['death']/df['positive'])
df['death_rate'] = df['death']/df['positive']
df['high_pct_death'] = df['pct_death_over_positive'].apply(lambda x: '1%+ death rate' if x >= 1 else "below 1% death rate")
df['pct_positive_out_of_total_tested'] = 100*(df['positive']/df['total'])
df['positive_over_pop'] = (df['positive']/df['POPESTIMATE2019'])*100
df['positive_per_100k'] = (df['positive_over_pop']/100)*100000
df['pct_pop_tested'] = (df['total']/df['POPESTIMATE2019'])*100
```

## Chloropleth maps


```python
df2 = df[df.date == max(df['date'])]
```


```python
fig = go.Figure(data=go.Choropleth(
    locations=df2['state'],
    z=df2['positive_per_100k'].astype(float),
    locationmode='USA-states',
    colorscale='Oranges',
    autocolorscale=False,
    text=df2['text'],  # hover text
    marker_line_color='white',  # line markers between states
    colorbar_title="Positive per 100,000 people"
))

fig.update_layout(
    title_text='Positive Covid-19 cases per 100,000 people, by State<br>(Hover for breakdown)',
    geo=dict(
        scope='usa',
        projection=go.layout.geo.Projection(type='albers usa'),
        showlakes=True,  # lakes
        lakecolor='rgb(255, 255, 255)'),
)
fig.show();
```


```python
display(IFrame(src='http://alqabandi.co/daml-covid/figure_13.html', height=600, width=900))
#display(HTML(url='alqabandi.co/daml-covid/figure_13.html'))
```



<iframe
    width="900"
    height="600"
    src="http://alqabandi.co/daml-covid/figure_13.html"
    frameborder="0"
    allowfullscreen
></iframe>




```python
#scale = 1000
fig = go.Figure(data=go.Choropleth(
    locations=df2['state'],
    z=df2['iclaims_since_emergency'],
    locationmode='USA-states',
    colorscale='Oranges',
    autocolorscale=False,
    text=df2['text'], # hover text
    marker_line_color='white', # line markers between states
    colorbar_title="Unemployment Insurance Claims"
))

fig.update_layout(
    title_text='Unemployment Insurance Claims since Emergency Declaration,<br>by State (Hover for breakdown)',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='rgb(255, 255, 255)'),
)
#fig.show();
```


```python
display(IFrame(src='http://alqabandi.co/daml-covid/figure_17.html', height=600, width=900))
```



<iframe
    width="900"
    height="600"
    src="http://alqabandi.co/daml-covid/figure_17.html"
    frameborder="0"
    allowfullscreen
></iframe>




```python
#scale = 1000
fig = go.Figure(data=go.Choropleth(
    locations=df2['state'],
    z=df2['inIcuCumulative'],
    locationmode='USA-states',
    colorscale='Oranges',
    autocolorscale=False,
    text=df2['text'], # hover text
    marker_line_color='white', # line markers between states
    colorbar_title="Number of Covid patients in ICU, Cumulative"
))

fig.update_layout(
    title_text='Number of Covid patients in ICU, Cumulative,<br>for ID, MN, WI, OH, VA (Hover for breakdown)',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='rgb(255, 255, 255)'),
)
#fig.show();
```


```python
display(IFrame(src='http://alqabandi.co/daml-covid/figure_19.html', height=600, width=900))
```



<iframe
    width="900"
    height="600"
    src="http://alqabandi.co/daml-covid/figure_19.html"
    frameborder="0"
    allowfullscreen
></iframe>




```python
#scale = 1000
fig = go.Figure(data=go.Choropleth(
    locations=df2['state'],
    z=df2['onVentilatorCumulative'],
    locationmode='USA-states',
    colorscale='Oranges',
    autocolorscale=False,
    text=df2['text'], # hover text
    marker_line_color='white', # line markers between states
    colorbar_title="Number of Covid patients on Ventilators, Cumulative"
))

fig.update_layout(
    title_text='Number of Covid patients on Ventilators, Cumulative,<br>for OR, VA, and AR (Hover for breakdown)',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='rgb(255, 255, 255)'),
)
#fig.show();
```


```python
display(IFrame(src='http://alqabandi.co/daml-covid/figure_20.html', height=600, width=900))
```



<iframe
    width="900"
    height="600"
    src="http://alqabandi.co/daml-covid/figure_20.html"
    frameborder="0"
    allowfullscreen
></iframe>




```python
#scale = 1000
fig = go.Figure(data=go.Choropleth(
    locations=df2['state'],
    z=df2['hospitalizedCumulative'],
    locationmode='USA-states',
    colorscale='Oranges',
    autocolorscale=False,
    text=df2['text'], # hover text
    marker_line_color='white', # line markers between states
    colorbar_title="Number of Covid patients Hospitalized, Cumulative"
))

fig.update_layout(
    title_text='Number of Covid patients Hospitalized, Cumulative<br>(Hover for breakdown)',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='rgb(255, 255, 255)'),
)
#fig.show();
```


```python
display(IFrame(src='http://alqabandi.co/daml-covid/figure_18.html', height=600, width=900))
```



<iframe
    width="900"
    height="600"
    src="http://alqabandi.co/daml-covid/figure_18.html"
    frameborder="0"
    allowfullscreen
></iframe>




```python
#scale = 1000
fig = go.Figure(data=go.Choropleth(
    locations=df2['state'],
    z=(df2['hospitalizedCumulative']/df2['positive'])*100,
    locationmode='USA-states',
    colorscale='Oranges',
    autocolorscale=False,
    text=df2['text'], # hover text
    marker_line_color='white', # line markers between states
    colorbar_title="Hospitalization rate for positive cases (in %)"
))

fig.update_layout(
    title_text='Hospitalization rate for positive cases<br>(Hover for breakdown)',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='rgb(255, 255, 255)'),
)
#fig.show();
```


```python
display(IFrame(src='http://alqabandi.co/daml-covid/figure_21.html', height=600, width=900))
```



<iframe
    width="900"
    height="600"
    src="http://alqabandi.co/daml-covid/figure_21.html"
    frameborder="0"
    allowfullscreen
></iframe>




```python
#scale = 1000
fig = go.Figure(data=go.Choropleth(
    locations=df2['state'],
    z=df2['pct_death_over_positive'],
    locationmode='USA-states',
    colorscale='Oranges',
    autocolorscale=False,
    text=df2['text'], # hover text
    marker_line_color='white', # line markers between states
    colorbar_title="Death rate in %"
))

fig.update_layout(
    title_text='Death rate by state<br>(Hover for breakdown)',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='rgb(255, 255, 255)'),
)
#fig.show();
```


```python
display(IFrame(src='http://alqabandi.co/daml-covid/figure_22.html', height=600, width=900))
```



<iframe
    width="900"
    height="600"
    src="http://alqabandi.co/daml-covid/figure_22.html"
    frameborder="0"
    allowfullscreen
></iframe>




```python
#scale = 1000
fig = go.Figure(data=go.Choropleth(
    locations=df2['state'],
    z=df2['pct_pop_tested'],
    locationmode='USA-states',
    colorscale='Oranges',
    autocolorscale=False,
    text=df2['text'], # hover text
    marker_line_color='white', # line markers between states
    colorbar_title="Percent of state population tested (in %)"
))

fig.update_layout(
    title_text='Percent of State Population tested<br>(Hover for breakdown)',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='rgb(255, 255, 255)'),
)
fig.show();
```


```python
display(IFrame(src='http://alqabandi.co/daml-covid/figure_27.html', height=600, width=900))
```



<iframe
    width="900"
    height="600"
    src="http://alqabandi.co/daml-covid/figure_27.html"
    frameborder="0"
    allowfullscreen
></iframe>




```python
#scale = 1000
fig = go.Figure(data=go.Choropleth(
    locations=df2['state'],
    z=df2['iclaims_since_stayathome'],
    locationmode='USA-states',
    colorscale='Oranges',
    autocolorscale=False,
    text=df2['text'], # hover text
    marker_line_color='white', # line markers between states
    colorbar_title="Number of Unemp. Ins. Claims since Stay-at-home Orders"
))

fig.update_layout(
    title_text='Number of Unemp. Ins. Claims since Stay-at-home Orders, by State<br>(Hover for breakdown)',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
        lakecolor='rgb(255, 255, 255)'),
)
#fig.show();
```


```python
display(IFrame(src='http://alqabandi.co/daml-covid/figure_23.html', height=600, width=900))
```



<iframe
    width="900"
    height="600"
    src="http://alqabandi.co/daml-covid/figure_23.html"
    frameborder="0"
    allowfullscreen
></iframe>




```python

```
