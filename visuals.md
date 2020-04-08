```python
import plotly 
import chart_studio.plotly as py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
```

## Downloading and combining latest data


```python
%run ./data_collection/00-daily-download.py
```

    Downloading data for state AL
    Downloading data for state AK
    Downloading data for state AZ
    Downloading data for state AR
    Downloading data for state CA
    Downloading data for state CO
    Downloading data for state CT
    Downloading data for state DE
    Downloading data for state FL
    Downloading data for state GA
    Downloading data for state HI
    Downloading data for state ID
    Downloading data for state IL
    Downloading data for state IN
    Downloading data for state IA
    Downloading data for state KS
    Downloading data for state KY
    Downloading data for state LA
    Downloading data for state ME
    Downloading data for state MD
    Downloading data for state MA
    Downloading data for state MI
    Downloading data for state MN
    Downloading data for state MS
    Downloading data for state MO
    Downloading data for state MT
    Downloading data for state NE
    Downloading data for state NV
    Downloading data for state NH
    Downloading data for state NJ
    Downloading data for state NM
    Downloading data for state NY
    Downloading data for state NC
    Downloading data for state ND
    Downloading data for state OH
    Downloading data for state OK
    Downloading data for state OR
    Downloading data for state PA
    Downloading data for state RI
    Downloading data for state SC
    Downloading data for state SD
    Downloading data for state TN
    Downloading data for state TX
    Downloading data for state UT
    Downloading data for state VT
    Downloading data for state VA
    Downloading data for state WA
    Downloading data for state WV
    Downloading data for state WI
    Downloading data for state WY
    Downloading data for state DC
    Downloading data for state VIR
    Downloading data for state PRI
    Downloading data from CovidTracking



```python
%run ./data_collection/01-daily-combine.py
```

    Writing combined data to file data/combined/iclaims.csv
    done
    Writing covidtracking data to file data/combined/covidtracking.csv
    Combining covidtracking and fred, and writing data to file data/combined/combined.csv
    done


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


        <script type="text/javascript">
        window.PlotlyConfig = {MathJaxConfig: 'local'};
        if (window.MathJax) {MathJax.Hub.Config({SVG: {font: "STIX-Web"}});}
        if (typeof require !== 'undefined') {
        require.undef("plotly");
        define('plotly', function(require, exports, module) {
            /**
* plotly.js v1.52.2
* Copyright 2012-2020, Plotly, Inc.
* All rights reserved.
* Licensed under the MIT license
*/
        });
        require(['plotly'], function(Plotly) {
            window._Plotly = Plotly;
        });
        }
        </script>




<div>


            <div id="9829e642-9984-48f7-a5ee-e93ae4c2288f" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};

                if (document.getElementById("9829e642-9984-48f7-a5ee-e93ae4c2288f")) {
                    Plotly.newPlot(
                        '9829e642-9984-48f7-a5ee-e93ae4c2288f',
                        [{"autocolorscale": false, "colorbar": {"title": {"text": "Positive per 100,000 people"}}, "colorscale": [[0.0, "rgb(255,245,235)"], [0.125, "rgb(254,230,206)"], [0.25, "rgb(253,208,162)"], [0.375, "rgb(253,174,107)"], [0.5, "rgb(253,141,60)"], [0.625, "rgb(241,105,19)"], [0.75, "rgb(217,72,1)"], [0.875, "rgb(166,54,3)"], [1.0, "rgb(127,39,4)"]], "locationmode": "USA-states", "locations": ["FL", "CT", "ND", "MD", "LA", "DE", "GA", "NJ", "IL", "NV", "MN", "NC", "UT", "AZ", "IN", "RI", "CA", "WV", "MS", "VT", "KY", "NE", "OH", "DC", "NH", "IA", "AL", "CO", "MO", "OR", "TN", "WA", "MA", "SD", "OK", "ID", "HI", "KS", "AR", "NM", "ME", "TX", "NY", "WI", "VA", "SC", "AK", "PA", "MI", "MT", "WY"], "marker": {"line": {"color": "white"}}, "text": ["FL\nPositive: 14747.0, Deaths: 296.0, Negative: 123415.0, Total Tested: 139569", "CT\nPositive: 7781.0, Deaths: 277.0, Negative: 21255.0, Total Tested: 29036", "ND\nPositive: 237.0, Deaths: 4.0, Negative: 7466.0, Total Tested: 7703", "MD\nPositive: 4371.0, Deaths: 103.0, Negative: 27256.0, Total Tested: 31627", "LA\nPositive: 16284.0, Deaths: 582.0, Negative: 58371.0, Total Tested: 74655", "DE\nPositive: 928.0, Deaths: 16.0, Negative: 7628.0, Total Tested: 8556", "GA\nPositive: 8818.0, Deaths: 329.0, Negative: 24895.0, Total Tested: 33713", "NJ\nPositive: 44416.0, Deaths: 1232.0, Negative: 50558.0, Total Tested: 94974", "IL\nPositive: 13549.0, Deaths: 380.0, Negative: 55183.0, Total Tested: 68732", "NV\nPositive: 2087.0, Deaths: 58.0, Negative: 16552.0, Total Tested: 18639", "MN\nPositive: 1069.0, Deaths: 34.0, Negative: 28191.0, Total Tested: 29260", "NC\nPositive: 3221.0, Deaths: 46.0, Negative: 37861.0, Total Tested: 41082", "UT\nPositive: 1738.0, Deaths: 13.0, Negative: 32909.0, Total Tested: 34647", "AZ\nPositive: 2575.0, Deaths: 73.0, Negative: 30800.0, Total Tested: 33375", "IN\nPositive: 5507.0, Deaths: 173.0, Negative: 23257.0, Total Tested: 28764", "RI\nPositive: 1229.0, Deaths: 30.0, Negative: 7399.0, Total Tested: 8628", "CA\nPositive: 15865.0, Deaths: 374.0, Negative: 115364.0, Total Tested: 145329", "WV\nPositive: 412.0, Deaths: 4.0, Negative: 11647.0, Total Tested: 12059", "MS\nPositive: 1915.0, Deaths: 59.0, Negative: 18632.0, Total Tested: 20547", "VT\nPositive: 575.0, Deaths: 23.0, Negative: 6554.0, Total Tested: 7129", "KY\nPositive: 1008.0, Deaths: 59.0, Negative: 18947.0, Total Tested: 19955", "NE\nPositive: 447.0, Deaths: 10.0, Negative: 6811.0, Total Tested: 7258", "OH\nPositive: 4782.0, Deaths: 167.0, Negative: 46056.0, Total Tested: 50838", "DC\nPositive: 1211.0, Deaths: 22.0, Negative: 6612.0, Total Tested: 7823", "NH\nPositive: 715.0, Deaths: 9.0, Negative: 8019.0, Total Tested: 8783", "IA\nPositive: 1048.0, Deaths: 26.0, Negative: 11670.0, Total Tested: 12718", "AL\nPositive: 2119.0, Deaths: 56.0, Negative: 12797.0, Total Tested: 14916", "CO\nPositive: 5172.0, Deaths: 150.0, Negative: 21703.0, Total Tested: 26875", "MO\nPositive: 3037.0, Deaths: 53.0, Negative: 28932.0, Total Tested: 31969", "OR\nPositive: 1132.0, Deaths: 29.0, Negative: 20669.0, Total Tested: 21801", "TN\nPositive: 4138.0, Deaths: 72.0, Negative: 48736.0, Total Tested: 52874", "WA\nPositive: 8384.0, Deaths: 372.0, Negative: 83391.0, Total Tested: 91775", "MA\nPositive: 15202.0, Deaths: 356.0, Negative: 66142.0, Total Tested: 81344", "SD\nPositive: 320.0, Deaths: 6.0, Negative: 5948.0, Total Tested: 6270", "OK\nPositive: 1472.0, Deaths: 67.0, Negative: 11821.0, Total Tested: 13293", "ID\nPositive: 1170.0, Deaths: 13.0, Negative: 10076.0, Total Tested: 11246", "HI\nPositive: 387.0, Deaths: 5.0, Negative: 13155.0, Total Tested: 13542", "KS\nPositive: 900.0, Deaths: 27.0, Negative: 8614.0, Total Tested: 9514", "AR\nPositive: 946.0, Deaths: 16.0, Negative: 12692.0, Total Tested: 13638", "NM\nPositive: 686.0, Deaths: 12.0, Negative: 21139.0, Total Tested: 21825", "ME\nPositive: 519.0, Deaths: 12.0, Negative: 6088.0, Total Tested: 6607", "TX\nPositive: 8262.0, Deaths: 154.0, Negative: 80387.0, Total Tested: 88649", "NY\nPositive: 138863.0, Deaths: 5489.0, Negative: 201195.0, Total Tested: 340058", "WI\nPositive: 2578.0, Deaths: 92.0, Negative: 28512.0, Total Tested: 31090", "VA\nPositive: 3333.0, Deaths: 63.0, Negative: 25312.0, Total Tested: 28645", "SC\nPositive: 2417.0, Deaths: 51.0, Negative: 21263.0, Total Tested: 23680", "AK\nPositive: 213.0, Deaths: 6.0, Negative: 6700.0, Total Tested: 6913", "PA\nPositive: 14559.0, Deaths: 240.0, Negative: 76719.0, Total Tested: 91278", "MI\nPositive: 18970.0, Deaths: 845.0, Negative: 31362.0, Total Tested: 50332", "MT\nPositive: 319.0, Deaths: 6.0, Negative: 6666.0, Total Tested: 6985", "WY\nPositive: 216.0, Deaths: 0.0, Negative: 3789.0, Total Tested: 4005"], "type": "choropleth", "z": [68.6617961659555, 218.24329990825422, 31.09983177221801, 72.29955935477895, 350.2843963402121, 95.30029863498754, 83.05216812026798, 500.05685534761136, 106.92228054673437, 67.75630844671504, 18.955137498333226, 30.711043122843027, 54.21156484270848, 35.37711385124604, 81.80066631819315, 116.01333256557491, 40.15213216426724, 22.98918559694043, 64.34489671048054, 92.14906031997359, 22.56208097593535, 23.10784488070769, 40.90990752068166, 171.5907496857948, 52.58470366129273, 33.21637871742941, 43.21680703461118, 89.81137527401846, 49.48326888722768, 26.839037142429696, 60.59297947306658, 110.1000368619756, 220.5584821653324, 36.172129600218845, 37.200171545356284, 65.47047813034222, 27.332979252361795, 30.892653521041673, 31.347297571346584, 32.71606792923981, 38.60998116368549, 28.49370226067627, 713.8178968878757, 44.27701542001163, 39.04859212427504, 46.943761102286906, 29.11645900115509, 113.72451577641569, 189.94965082608073, 29.84717125539635, 37.32123388146016]}],
                        {"geo": {"lakecolor": "rgb(255, 255, 255)", "projection": {"type": "albers usa"}, "scope": "usa", "showlakes": true}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Positive Covid-19 cases per 100,000 people, by State<br>(Hover for breakdown)"}},
                        {"responsive": true}
                    ).then(function(){

var gd = document.getElementById('9829e642-9984-48f7-a5ee-e93ae4c2288f');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>



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
fig.show();
```


<div>


            <div id="bd433e21-bbb0-4cc8-b97a-1a08376abe1e" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};

                if (document.getElementById("bd433e21-bbb0-4cc8-b97a-1a08376abe1e")) {
                    Plotly.newPlot(
                        'bd433e21-bbb0-4cc8-b97a-1a08376abe1e',
                        [{"autocolorscale": false, "colorbar": {"title": {"text": "Unemployment Insurance Claims"}}, "colorscale": [[0.0, "rgb(255,245,235)"], [0.125, "rgb(254,230,206)"], [0.25, "rgb(253,208,162)"], [0.375, "rgb(253,174,107)"], [0.5, "rgb(253,141,60)"], [0.625, "rgb(241,105,19)"], [0.75, "rgb(217,72,1)"], [0.875, "rgb(166,54,3)"], [1.0, "rgb(127,39,4)"]], "locationmode": "USA-states", "locations": ["FL", "CT", "ND", "MD", "LA", "DE", "GA", "NJ", "IL", "NV", "MN", "NC", "UT", "AZ", "IN", "RI", "CA", "WV", "MS", "VT", "KY", "NE", "OH", "DC", "NH", "IA", "AL", "CO", "MO", "OR", "TN", "WA", "MA", "SD", "OK", "ID", "HI", "KS", "AR", "NM", "ME", "TX", "NY", "WI", "VA", "SC", "AK", "PA", "MI", "MT", "WY"], "marker": {"line": {"color": "white"}}, "text": ["FL\nPositive: 14747.0, Deaths: 296.0, Negative: 123415.0, Total Tested: 139569", "CT\nPositive: 7781.0, Deaths: 277.0, Negative: 21255.0, Total Tested: 29036", "ND\nPositive: 237.0, Deaths: 4.0, Negative: 7466.0, Total Tested: 7703", "MD\nPositive: 4371.0, Deaths: 103.0, Negative: 27256.0, Total Tested: 31627", "LA\nPositive: 16284.0, Deaths: 582.0, Negative: 58371.0, Total Tested: 74655", "DE\nPositive: 928.0, Deaths: 16.0, Negative: 7628.0, Total Tested: 8556", "GA\nPositive: 8818.0, Deaths: 329.0, Negative: 24895.0, Total Tested: 33713", "NJ\nPositive: 44416.0, Deaths: 1232.0, Negative: 50558.0, Total Tested: 94974", "IL\nPositive: 13549.0, Deaths: 380.0, Negative: 55183.0, Total Tested: 68732", "NV\nPositive: 2087.0, Deaths: 58.0, Negative: 16552.0, Total Tested: 18639", "MN\nPositive: 1069.0, Deaths: 34.0, Negative: 28191.0, Total Tested: 29260", "NC\nPositive: 3221.0, Deaths: 46.0, Negative: 37861.0, Total Tested: 41082", "UT\nPositive: 1738.0, Deaths: 13.0, Negative: 32909.0, Total Tested: 34647", "AZ\nPositive: 2575.0, Deaths: 73.0, Negative: 30800.0, Total Tested: 33375", "IN\nPositive: 5507.0, Deaths: 173.0, Negative: 23257.0, Total Tested: 28764", "RI\nPositive: 1229.0, Deaths: 30.0, Negative: 7399.0, Total Tested: 8628", "CA\nPositive: 15865.0, Deaths: 374.0, Negative: 115364.0, Total Tested: 145329", "WV\nPositive: 412.0, Deaths: 4.0, Negative: 11647.0, Total Tested: 12059", "MS\nPositive: 1915.0, Deaths: 59.0, Negative: 18632.0, Total Tested: 20547", "VT\nPositive: 575.0, Deaths: 23.0, Negative: 6554.0, Total Tested: 7129", "KY\nPositive: 1008.0, Deaths: 59.0, Negative: 18947.0, Total Tested: 19955", "NE\nPositive: 447.0, Deaths: 10.0, Negative: 6811.0, Total Tested: 7258", "OH\nPositive: 4782.0, Deaths: 167.0, Negative: 46056.0, Total Tested: 50838", "DC\nPositive: 1211.0, Deaths: 22.0, Negative: 6612.0, Total Tested: 7823", "NH\nPositive: 715.0, Deaths: 9.0, Negative: 8019.0, Total Tested: 8783", "IA\nPositive: 1048.0, Deaths: 26.0, Negative: 11670.0, Total Tested: 12718", "AL\nPositive: 2119.0, Deaths: 56.0, Negative: 12797.0, Total Tested: 14916", "CO\nPositive: 5172.0, Deaths: 150.0, Negative: 21703.0, Total Tested: 26875", "MO\nPositive: 3037.0, Deaths: 53.0, Negative: 28932.0, Total Tested: 31969", "OR\nPositive: 1132.0, Deaths: 29.0, Negative: 20669.0, Total Tested: 21801", "TN\nPositive: 4138.0, Deaths: 72.0, Negative: 48736.0, Total Tested: 52874", "WA\nPositive: 8384.0, Deaths: 372.0, Negative: 83391.0, Total Tested: 91775", "MA\nPositive: 15202.0, Deaths: 356.0, Negative: 66142.0, Total Tested: 81344", "SD\nPositive: 320.0, Deaths: 6.0, Negative: 5948.0, Total Tested: 6270", "OK\nPositive: 1472.0, Deaths: 67.0, Negative: 11821.0, Total Tested: 13293", "ID\nPositive: 1170.0, Deaths: 13.0, Negative: 10076.0, Total Tested: 11246", "HI\nPositive: 387.0, Deaths: 5.0, Negative: 13155.0, Total Tested: 13542", "KS\nPositive: 900.0, Deaths: 27.0, Negative: 8614.0, Total Tested: 9514", "AR\nPositive: 946.0, Deaths: 16.0, Negative: 12692.0, Total Tested: 13638", "NM\nPositive: 686.0, Deaths: 12.0, Negative: 21139.0, Total Tested: 21825", "ME\nPositive: 519.0, Deaths: 12.0, Negative: 6088.0, Total Tested: 6607", "TX\nPositive: 8262.0, Deaths: 154.0, Negative: 80387.0, Total Tested: 88649", "NY\nPositive: 138863.0, Deaths: 5489.0, Negative: 201195.0, Total Tested: 340058", "WI\nPositive: 2578.0, Deaths: 92.0, Negative: 28512.0, Total Tested: 31090", "VA\nPositive: 3333.0, Deaths: 63.0, Negative: 25312.0, Total Tested: 28645", "SC\nPositive: 2417.0, Deaths: 51.0, Negative: 21263.0, Total Tested: 23680", "AK\nPositive: 213.0, Deaths: 6.0, Negative: 6700.0, Total Tested: 6913", "PA\nPositive: 14559.0, Deaths: 240.0, Negative: 76719.0, Total Tested: 91278", "MI\nPositive: 18970.0, Deaths: 845.0, Negative: 31362.0, Total Tested: 50332", "MT\nPositive: 319.0, Deaths: 6.0, Negative: 6666.0, Total Tested: 6985", "WY\nPositive: 216.0, Deaths: 0.0, Negative: 3789.0, Total Tested: 4005"], "type": "choropleth", "z": [80776.0, 28540.0, 6077.0, 49520.0, 74693.0, 11248.0, 17585.0, 125282.0, 124984.0, 98654.0, 119783.0, 97616.0, 22010.0, 33192.0, 64574.0, 36955.0, 243939.0, 5434.0, 6666.0, 4443.0, 54271.0, 16495.0, 203355.0, 15675.0, 30021.0, 43181.0, 12711.0, 22095.0, 46262.0, 38477.0, 40779.0, 150765.0, 155901.0, 1951.0, 21926.0, 14617.0, 11679.0, 25318.0, 10657.0, 18974.0, 21459.0, 171602.0, 108306.0, 56221.0, 48983.0, 33919.0, 8967.0, 405117.0, 133344.0, 16166.0, 4170.0]}],
                        {"geo": {"lakecolor": "rgb(255, 255, 255)", "projection": {"type": "albers usa"}, "scope": "usa", "showlakes": true}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Unemployment Insurance Claims since Emergency Declaration,<br>by State (Hover for breakdown)"}},
                        {"responsive": true}
                    ).then(function(){

var gd = document.getElementById('bd433e21-bbb0-4cc8-b97a-1a08376abe1e');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>



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
fig.show();
```


<div>


            <div id="14f0a490-a616-4afc-87e3-7a590f867a27" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};

                if (document.getElementById("14f0a490-a616-4afc-87e3-7a590f867a27")) {
                    Plotly.newPlot(
                        '14f0a490-a616-4afc-87e3-7a590f867a27',
                        [{"autocolorscale": false, "colorbar": {"title": {"text": "Number of Covid patients in ICU, Cumulative"}}, "colorscale": [[0.0, "rgb(255,245,235)"], [0.125, "rgb(254,230,206)"], [0.25, "rgb(253,208,162)"], [0.375, "rgb(253,174,107)"], [0.5, "rgb(253,141,60)"], [0.625, "rgb(241,105,19)"], [0.75, "rgb(217,72,1)"], [0.875, "rgb(166,54,3)"], [1.0, "rgb(127,39,4)"]], "locationmode": "USA-states", "locations": ["FL", "CT", "ND", "MD", "LA", "DE", "GA", "NJ", "IL", "NV", "MN", "NC", "UT", "AZ", "IN", "RI", "CA", "WV", "MS", "VT", "KY", "NE", "OH", "DC", "NH", "IA", "AL", "CO", "MO", "OR", "TN", "WA", "MA", "SD", "OK", "ID", "HI", "KS", "AR", "NM", "ME", "TX", "NY", "WI", "VA", "SC", "AK", "PA", "MI", "MT", "WY"], "marker": {"line": {"color": "white"}}, "text": ["FL\nPositive: 14747.0, Deaths: 296.0, Negative: 123415.0, Total Tested: 139569", "CT\nPositive: 7781.0, Deaths: 277.0, Negative: 21255.0, Total Tested: 29036", "ND\nPositive: 237.0, Deaths: 4.0, Negative: 7466.0, Total Tested: 7703", "MD\nPositive: 4371.0, Deaths: 103.0, Negative: 27256.0, Total Tested: 31627", "LA\nPositive: 16284.0, Deaths: 582.0, Negative: 58371.0, Total Tested: 74655", "DE\nPositive: 928.0, Deaths: 16.0, Negative: 7628.0, Total Tested: 8556", "GA\nPositive: 8818.0, Deaths: 329.0, Negative: 24895.0, Total Tested: 33713", "NJ\nPositive: 44416.0, Deaths: 1232.0, Negative: 50558.0, Total Tested: 94974", "IL\nPositive: 13549.0, Deaths: 380.0, Negative: 55183.0, Total Tested: 68732", "NV\nPositive: 2087.0, Deaths: 58.0, Negative: 16552.0, Total Tested: 18639", "MN\nPositive: 1069.0, Deaths: 34.0, Negative: 28191.0, Total Tested: 29260", "NC\nPositive: 3221.0, Deaths: 46.0, Negative: 37861.0, Total Tested: 41082", "UT\nPositive: 1738.0, Deaths: 13.0, Negative: 32909.0, Total Tested: 34647", "AZ\nPositive: 2575.0, Deaths: 73.0, Negative: 30800.0, Total Tested: 33375", "IN\nPositive: 5507.0, Deaths: 173.0, Negative: 23257.0, Total Tested: 28764", "RI\nPositive: 1229.0, Deaths: 30.0, Negative: 7399.0, Total Tested: 8628", "CA\nPositive: 15865.0, Deaths: 374.0, Negative: 115364.0, Total Tested: 145329", "WV\nPositive: 412.0, Deaths: 4.0, Negative: 11647.0, Total Tested: 12059", "MS\nPositive: 1915.0, Deaths: 59.0, Negative: 18632.0, Total Tested: 20547", "VT\nPositive: 575.0, Deaths: 23.0, Negative: 6554.0, Total Tested: 7129", "KY\nPositive: 1008.0, Deaths: 59.0, Negative: 18947.0, Total Tested: 19955", "NE\nPositive: 447.0, Deaths: 10.0, Negative: 6811.0, Total Tested: 7258", "OH\nPositive: 4782.0, Deaths: 167.0, Negative: 46056.0, Total Tested: 50838", "DC\nPositive: 1211.0, Deaths: 22.0, Negative: 6612.0, Total Tested: 7823", "NH\nPositive: 715.0, Deaths: 9.0, Negative: 8019.0, Total Tested: 8783", "IA\nPositive: 1048.0, Deaths: 26.0, Negative: 11670.0, Total Tested: 12718", "AL\nPositive: 2119.0, Deaths: 56.0, Negative: 12797.0, Total Tested: 14916", "CO\nPositive: 5172.0, Deaths: 150.0, Negative: 21703.0, Total Tested: 26875", "MO\nPositive: 3037.0, Deaths: 53.0, Negative: 28932.0, Total Tested: 31969", "OR\nPositive: 1132.0, Deaths: 29.0, Negative: 20669.0, Total Tested: 21801", "TN\nPositive: 4138.0, Deaths: 72.0, Negative: 48736.0, Total Tested: 52874", "WA\nPositive: 8384.0, Deaths: 372.0, Negative: 83391.0, Total Tested: 91775", "MA\nPositive: 15202.0, Deaths: 356.0, Negative: 66142.0, Total Tested: 81344", "SD\nPositive: 320.0, Deaths: 6.0, Negative: 5948.0, Total Tested: 6270", "OK\nPositive: 1472.0, Deaths: 67.0, Negative: 11821.0, Total Tested: 13293", "ID\nPositive: 1170.0, Deaths: 13.0, Negative: 10076.0, Total Tested: 11246", "HI\nPositive: 387.0, Deaths: 5.0, Negative: 13155.0, Total Tested: 13542", "KS\nPositive: 900.0, Deaths: 27.0, Negative: 8614.0, Total Tested: 9514", "AR\nPositive: 946.0, Deaths: 16.0, Negative: 12692.0, Total Tested: 13638", "NM\nPositive: 686.0, Deaths: 12.0, Negative: 21139.0, Total Tested: 21825", "ME\nPositive: 519.0, Deaths: 12.0, Negative: 6088.0, Total Tested: 6607", "TX\nPositive: 8262.0, Deaths: 154.0, Negative: 80387.0, Total Tested: 88649", "NY\nPositive: 138863.0, Deaths: 5489.0, Negative: 201195.0, Total Tested: 340058", "WI\nPositive: 2578.0, Deaths: 92.0, Negative: 28512.0, Total Tested: 31090", "VA\nPositive: 3333.0, Deaths: 63.0, Negative: 25312.0, Total Tested: 28645", "SC\nPositive: 2417.0, Deaths: 51.0, Negative: 21263.0, Total Tested: 23680", "AK\nPositive: 213.0, Deaths: 6.0, Negative: 6700.0, Total Tested: 6913", "PA\nPositive: 14559.0, Deaths: 240.0, Negative: 76719.0, Total Tested: 91278", "MI\nPositive: 18970.0, Deaths: 845.0, Negative: 31362.0, Total Tested: 50332", "MT\nPositive: 319.0, Deaths: 6.0, Negative: 6666.0, Total Tested: 6985", "WY\nPositive: 216.0, Deaths: 0.0, Negative: 3789.0, Total Tested: 4005"], "type": "choropleth", "z": [null, null, null, null, null, null, null, null, null, null, 100.0, null, null, null, null, null, null, null, null, null, null, null, 417.0, null, null, null, null, null, null, null, null, null, null, null, null, 21.0, 6.0, null, 43.0, null, null, null, null, 200.0, 145.0, null, null, null, null, null, null]}],
                        {"geo": {"lakecolor": "rgb(255, 255, 255)", "projection": {"type": "albers usa"}, "scope": "usa", "showlakes": true}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Number of Covid patients in ICU, Cumulative,<br>for ID, MN, WI, OH, VA (Hover for breakdown)"}},
                        {"responsive": true}
                    ).then(function(){

var gd = document.getElementById('14f0a490-a616-4afc-87e3-7a590f867a27');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>



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
fig.show();
```


<div>


            <div id="22752223-4c24-489f-bc32-1860ba4cae73" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};

                if (document.getElementById("22752223-4c24-489f-bc32-1860ba4cae73")) {
                    Plotly.newPlot(
                        '22752223-4c24-489f-bc32-1860ba4cae73',
                        [{"autocolorscale": false, "colorbar": {"title": {"text": "Number of Covid patients on Ventilators, Cumulative"}}, "colorscale": [[0.0, "rgb(255,245,235)"], [0.125, "rgb(254,230,206)"], [0.25, "rgb(253,208,162)"], [0.375, "rgb(253,174,107)"], [0.5, "rgb(253,141,60)"], [0.625, "rgb(241,105,19)"], [0.75, "rgb(217,72,1)"], [0.875, "rgb(166,54,3)"], [1.0, "rgb(127,39,4)"]], "locationmode": "USA-states", "locations": ["FL", "CT", "ND", "MD", "LA", "DE", "GA", "NJ", "IL", "NV", "MN", "NC", "UT", "AZ", "IN", "RI", "CA", "WV", "MS", "VT", "KY", "NE", "OH", "DC", "NH", "IA", "AL", "CO", "MO", "OR", "TN", "WA", "MA", "SD", "OK", "ID", "HI", "KS", "AR", "NM", "ME", "TX", "NY", "WI", "VA", "SC", "AK", "PA", "MI", "MT", "WY"], "marker": {"line": {"color": "white"}}, "text": ["FL\nPositive: 14747.0, Deaths: 296.0, Negative: 123415.0, Total Tested: 139569", "CT\nPositive: 7781.0, Deaths: 277.0, Negative: 21255.0, Total Tested: 29036", "ND\nPositive: 237.0, Deaths: 4.0, Negative: 7466.0, Total Tested: 7703", "MD\nPositive: 4371.0, Deaths: 103.0, Negative: 27256.0, Total Tested: 31627", "LA\nPositive: 16284.0, Deaths: 582.0, Negative: 58371.0, Total Tested: 74655", "DE\nPositive: 928.0, Deaths: 16.0, Negative: 7628.0, Total Tested: 8556", "GA\nPositive: 8818.0, Deaths: 329.0, Negative: 24895.0, Total Tested: 33713", "NJ\nPositive: 44416.0, Deaths: 1232.0, Negative: 50558.0, Total Tested: 94974", "IL\nPositive: 13549.0, Deaths: 380.0, Negative: 55183.0, Total Tested: 68732", "NV\nPositive: 2087.0, Deaths: 58.0, Negative: 16552.0, Total Tested: 18639", "MN\nPositive: 1069.0, Deaths: 34.0, Negative: 28191.0, Total Tested: 29260", "NC\nPositive: 3221.0, Deaths: 46.0, Negative: 37861.0, Total Tested: 41082", "UT\nPositive: 1738.0, Deaths: 13.0, Negative: 32909.0, Total Tested: 34647", "AZ\nPositive: 2575.0, Deaths: 73.0, Negative: 30800.0, Total Tested: 33375", "IN\nPositive: 5507.0, Deaths: 173.0, Negative: 23257.0, Total Tested: 28764", "RI\nPositive: 1229.0, Deaths: 30.0, Negative: 7399.0, Total Tested: 8628", "CA\nPositive: 15865.0, Deaths: 374.0, Negative: 115364.0, Total Tested: 145329", "WV\nPositive: 412.0, Deaths: 4.0, Negative: 11647.0, Total Tested: 12059", "MS\nPositive: 1915.0, Deaths: 59.0, Negative: 18632.0, Total Tested: 20547", "VT\nPositive: 575.0, Deaths: 23.0, Negative: 6554.0, Total Tested: 7129", "KY\nPositive: 1008.0, Deaths: 59.0, Negative: 18947.0, Total Tested: 19955", "NE\nPositive: 447.0, Deaths: 10.0, Negative: 6811.0, Total Tested: 7258", "OH\nPositive: 4782.0, Deaths: 167.0, Negative: 46056.0, Total Tested: 50838", "DC\nPositive: 1211.0, Deaths: 22.0, Negative: 6612.0, Total Tested: 7823", "NH\nPositive: 715.0, Deaths: 9.0, Negative: 8019.0, Total Tested: 8783", "IA\nPositive: 1048.0, Deaths: 26.0, Negative: 11670.0, Total Tested: 12718", "AL\nPositive: 2119.0, Deaths: 56.0, Negative: 12797.0, Total Tested: 14916", "CO\nPositive: 5172.0, Deaths: 150.0, Negative: 21703.0, Total Tested: 26875", "MO\nPositive: 3037.0, Deaths: 53.0, Negative: 28932.0, Total Tested: 31969", "OR\nPositive: 1132.0, Deaths: 29.0, Negative: 20669.0, Total Tested: 21801", "TN\nPositive: 4138.0, Deaths: 72.0, Negative: 48736.0, Total Tested: 52874", "WA\nPositive: 8384.0, Deaths: 372.0, Negative: 83391.0, Total Tested: 91775", "MA\nPositive: 15202.0, Deaths: 356.0, Negative: 66142.0, Total Tested: 81344", "SD\nPositive: 320.0, Deaths: 6.0, Negative: 5948.0, Total Tested: 6270", "OK\nPositive: 1472.0, Deaths: 67.0, Negative: 11821.0, Total Tested: 13293", "ID\nPositive: 1170.0, Deaths: 13.0, Negative: 10076.0, Total Tested: 11246", "HI\nPositive: 387.0, Deaths: 5.0, Negative: 13155.0, Total Tested: 13542", "KS\nPositive: 900.0, Deaths: 27.0, Negative: 8614.0, Total Tested: 9514", "AR\nPositive: 946.0, Deaths: 16.0, Negative: 12692.0, Total Tested: 13638", "NM\nPositive: 686.0, Deaths: 12.0, Negative: 21139.0, Total Tested: 21825", "ME\nPositive: 519.0, Deaths: 12.0, Negative: 6088.0, Total Tested: 6607", "TX\nPositive: 8262.0, Deaths: 154.0, Negative: 80387.0, Total Tested: 88649", "NY\nPositive: 138863.0, Deaths: 5489.0, Negative: 201195.0, Total Tested: 340058", "WI\nPositive: 2578.0, Deaths: 92.0, Negative: 28512.0, Total Tested: 31090", "VA\nPositive: 3333.0, Deaths: 63.0, Negative: 25312.0, Total Tested: 28645", "SC\nPositive: 2417.0, Deaths: 51.0, Negative: 21263.0, Total Tested: 23680", "AK\nPositive: 213.0, Deaths: 6.0, Negative: 6700.0, Total Tested: 6913", "PA\nPositive: 14559.0, Deaths: 240.0, Negative: 76719.0, Total Tested: 91278", "MI\nPositive: 18970.0, Deaths: 845.0, Negative: 31362.0, Total Tested: 50332", "MT\nPositive: 319.0, Deaths: 6.0, Negative: 6666.0, Total Tested: 6985", "WY\nPositive: 216.0, Deaths: 0.0, Negative: 3789.0, Total Tested: 4005"], "type": "choropleth", "z": [null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, null, 82.0, null, null, null, null, null, null, null, null, 39.0, null, null, null, null, null, 108.0, null, null, null, null, null, null]}],
                        {"geo": {"lakecolor": "rgb(255, 255, 255)", "projection": {"type": "albers usa"}, "scope": "usa", "showlakes": true}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Number of Covid patients on Ventilators, Cumulative,<br>for OR, VA, and AR (Hover for breakdown)"}},
                        {"responsive": true}
                    ).then(function(){

var gd = document.getElementById('22752223-4c24-489f-bc32-1860ba4cae73');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>



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
fig.show();
```


<div>


            <div id="b1bfe671-23e4-4d67-aea9-7835f2eb9e6c" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};

                if (document.getElementById("b1bfe671-23e4-4d67-aea9-7835f2eb9e6c")) {
                    Plotly.newPlot(
                        'b1bfe671-23e4-4d67-aea9-7835f2eb9e6c',
                        [{"autocolorscale": false, "colorbar": {"title": {"text": "Number of Covid patients Hospitalized, Cumulative"}}, "colorscale": [[0.0, "rgb(255,245,235)"], [0.125, "rgb(254,230,206)"], [0.25, "rgb(253,208,162)"], [0.375, "rgb(253,174,107)"], [0.5, "rgb(253,141,60)"], [0.625, "rgb(241,105,19)"], [0.75, "rgb(217,72,1)"], [0.875, "rgb(166,54,3)"], [1.0, "rgb(127,39,4)"]], "locationmode": "USA-states", "locations": ["FL", "CT", "ND", "MD", "LA", "DE", "GA", "NJ", "IL", "NV", "MN", "NC", "UT", "AZ", "IN", "RI", "CA", "WV", "MS", "VT", "KY", "NE", "OH", "DC", "NH", "IA", "AL", "CO", "MO", "OR", "TN", "WA", "MA", "SD", "OK", "ID", "HI", "KS", "AR", "NM", "ME", "TX", "NY", "WI", "VA", "SC", "AK", "PA", "MI", "MT", "WY"], "marker": {"line": {"color": "white"}}, "text": ["FL\nPositive: 14747.0, Deaths: 296.0, Negative: 123415.0, Total Tested: 139569", "CT\nPositive: 7781.0, Deaths: 277.0, Negative: 21255.0, Total Tested: 29036", "ND\nPositive: 237.0, Deaths: 4.0, Negative: 7466.0, Total Tested: 7703", "MD\nPositive: 4371.0, Deaths: 103.0, Negative: 27256.0, Total Tested: 31627", "LA\nPositive: 16284.0, Deaths: 582.0, Negative: 58371.0, Total Tested: 74655", "DE\nPositive: 928.0, Deaths: 16.0, Negative: 7628.0, Total Tested: 8556", "GA\nPositive: 8818.0, Deaths: 329.0, Negative: 24895.0, Total Tested: 33713", "NJ\nPositive: 44416.0, Deaths: 1232.0, Negative: 50558.0, Total Tested: 94974", "IL\nPositive: 13549.0, Deaths: 380.0, Negative: 55183.0, Total Tested: 68732", "NV\nPositive: 2087.0, Deaths: 58.0, Negative: 16552.0, Total Tested: 18639", "MN\nPositive: 1069.0, Deaths: 34.0, Negative: 28191.0, Total Tested: 29260", "NC\nPositive: 3221.0, Deaths: 46.0, Negative: 37861.0, Total Tested: 41082", "UT\nPositive: 1738.0, Deaths: 13.0, Negative: 32909.0, Total Tested: 34647", "AZ\nPositive: 2575.0, Deaths: 73.0, Negative: 30800.0, Total Tested: 33375", "IN\nPositive: 5507.0, Deaths: 173.0, Negative: 23257.0, Total Tested: 28764", "RI\nPositive: 1229.0, Deaths: 30.0, Negative: 7399.0, Total Tested: 8628", "CA\nPositive: 15865.0, Deaths: 374.0, Negative: 115364.0, Total Tested: 145329", "WV\nPositive: 412.0, Deaths: 4.0, Negative: 11647.0, Total Tested: 12059", "MS\nPositive: 1915.0, Deaths: 59.0, Negative: 18632.0, Total Tested: 20547", "VT\nPositive: 575.0, Deaths: 23.0, Negative: 6554.0, Total Tested: 7129", "KY\nPositive: 1008.0, Deaths: 59.0, Negative: 18947.0, Total Tested: 19955", "NE\nPositive: 447.0, Deaths: 10.0, Negative: 6811.0, Total Tested: 7258", "OH\nPositive: 4782.0, Deaths: 167.0, Negative: 46056.0, Total Tested: 50838", "DC\nPositive: 1211.0, Deaths: 22.0, Negative: 6612.0, Total Tested: 7823", "NH\nPositive: 715.0, Deaths: 9.0, Negative: 8019.0, Total Tested: 8783", "IA\nPositive: 1048.0, Deaths: 26.0, Negative: 11670.0, Total Tested: 12718", "AL\nPositive: 2119.0, Deaths: 56.0, Negative: 12797.0, Total Tested: 14916", "CO\nPositive: 5172.0, Deaths: 150.0, Negative: 21703.0, Total Tested: 26875", "MO\nPositive: 3037.0, Deaths: 53.0, Negative: 28932.0, Total Tested: 31969", "OR\nPositive: 1132.0, Deaths: 29.0, Negative: 20669.0, Total Tested: 21801", "TN\nPositive: 4138.0, Deaths: 72.0, Negative: 48736.0, Total Tested: 52874", "WA\nPositive: 8384.0, Deaths: 372.0, Negative: 83391.0, Total Tested: 91775", "MA\nPositive: 15202.0, Deaths: 356.0, Negative: 66142.0, Total Tested: 81344", "SD\nPositive: 320.0, Deaths: 6.0, Negative: 5948.0, Total Tested: 6270", "OK\nPositive: 1472.0, Deaths: 67.0, Negative: 11821.0, Total Tested: 13293", "ID\nPositive: 1170.0, Deaths: 13.0, Negative: 10076.0, Total Tested: 11246", "HI\nPositive: 387.0, Deaths: 5.0, Negative: 13155.0, Total Tested: 13542", "KS\nPositive: 900.0, Deaths: 27.0, Negative: 8614.0, Total Tested: 9514", "AR\nPositive: 946.0, Deaths: 16.0, Negative: 12692.0, Total Tested: 13638", "NM\nPositive: 686.0, Deaths: 12.0, Negative: 21139.0, Total Tested: 21825", "ME\nPositive: 519.0, Deaths: 12.0, Negative: 6088.0, Total Tested: 6607", "TX\nPositive: 8262.0, Deaths: 154.0, Negative: 80387.0, Total Tested: 88649", "NY\nPositive: 138863.0, Deaths: 5489.0, Negative: 201195.0, Total Tested: 340058", "WI\nPositive: 2578.0, Deaths: 92.0, Negative: 28512.0, Total Tested: 31090", "VA\nPositive: 3333.0, Deaths: 63.0, Negative: 25312.0, Total Tested: 28645", "SC\nPositive: 2417.0, Deaths: 51.0, Negative: 21263.0, Total Tested: 23680", "AK\nPositive: 213.0, Deaths: 6.0, Negative: 6700.0, Total Tested: 6913", "PA\nPositive: 14559.0, Deaths: 240.0, Negative: 76719.0, Total Tested: 91278", "MI\nPositive: 18970.0, Deaths: 845.0, Negative: 31362.0, Total Tested: 50332", "MT\nPositive: 319.0, Deaths: 6.0, Negative: 6666.0, Total Tested: 6985", "WY\nPositive: 216.0, Deaths: 0.0, Negative: 3789.0, Total Tested: 4005"], "type": "choropleth", "z": [1999.0, null, 33.0, 1106.0, null, null, 1774.0, null, null, null, 242.0, null, 148.0, null, null, null, null, null, 377.0, 45.0, null, null, 1354.0, null, 103.0, 193.0, 271.0, 994.0, null, 404.0, 408.0, null, 1435.0, 23.0, 376.0, 83.0, 26.0, 223.0, 130.0, null, 99.0, null, 32083.0, 745.0, 563.0, 241.0, 23.0, null, null, 28.0, 33.0]}],
                        {"geo": {"lakecolor": "rgb(255, 255, 255)", "projection": {"type": "albers usa"}, "scope": "usa", "showlakes": true}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Number of Covid patients Hospitalized, Cumulative<br>(Hover for breakdown)"}},
                        {"responsive": true}
                    ).then(function(){

var gd = document.getElementById('b1bfe671-23e4-4d67-aea9-7835f2eb9e6c');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>



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
fig.show();
```


<div>


            <div id="9244ac2a-07e8-429f-8289-24f4f4dad230" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};

                if (document.getElementById("9244ac2a-07e8-429f-8289-24f4f4dad230")) {
                    Plotly.newPlot(
                        '9244ac2a-07e8-429f-8289-24f4f4dad230',
                        [{"autocolorscale": false, "colorbar": {"title": {"text": "Hospitalization rate for positive cases (in %)"}}, "colorscale": [[0.0, "rgb(255,245,235)"], [0.125, "rgb(254,230,206)"], [0.25, "rgb(253,208,162)"], [0.375, "rgb(253,174,107)"], [0.5, "rgb(253,141,60)"], [0.625, "rgb(241,105,19)"], [0.75, "rgb(217,72,1)"], [0.875, "rgb(166,54,3)"], [1.0, "rgb(127,39,4)"]], "locationmode": "USA-states", "locations": ["FL", "CT", "ND", "MD", "LA", "DE", "GA", "NJ", "IL", "NV", "MN", "NC", "UT", "AZ", "IN", "RI", "CA", "WV", "MS", "VT", "KY", "NE", "OH", "DC", "NH", "IA", "AL", "CO", "MO", "OR", "TN", "WA", "MA", "SD", "OK", "ID", "HI", "KS", "AR", "NM", "ME", "TX", "NY", "WI", "VA", "SC", "AK", "PA", "MI", "MT", "WY"], "marker": {"line": {"color": "white"}}, "text": ["FL\nPositive: 14747.0, Deaths: 296.0, Negative: 123415.0, Total Tested: 139569", "CT\nPositive: 7781.0, Deaths: 277.0, Negative: 21255.0, Total Tested: 29036", "ND\nPositive: 237.0, Deaths: 4.0, Negative: 7466.0, Total Tested: 7703", "MD\nPositive: 4371.0, Deaths: 103.0, Negative: 27256.0, Total Tested: 31627", "LA\nPositive: 16284.0, Deaths: 582.0, Negative: 58371.0, Total Tested: 74655", "DE\nPositive: 928.0, Deaths: 16.0, Negative: 7628.0, Total Tested: 8556", "GA\nPositive: 8818.0, Deaths: 329.0, Negative: 24895.0, Total Tested: 33713", "NJ\nPositive: 44416.0, Deaths: 1232.0, Negative: 50558.0, Total Tested: 94974", "IL\nPositive: 13549.0, Deaths: 380.0, Negative: 55183.0, Total Tested: 68732", "NV\nPositive: 2087.0, Deaths: 58.0, Negative: 16552.0, Total Tested: 18639", "MN\nPositive: 1069.0, Deaths: 34.0, Negative: 28191.0, Total Tested: 29260", "NC\nPositive: 3221.0, Deaths: 46.0, Negative: 37861.0, Total Tested: 41082", "UT\nPositive: 1738.0, Deaths: 13.0, Negative: 32909.0, Total Tested: 34647", "AZ\nPositive: 2575.0, Deaths: 73.0, Negative: 30800.0, Total Tested: 33375", "IN\nPositive: 5507.0, Deaths: 173.0, Negative: 23257.0, Total Tested: 28764", "RI\nPositive: 1229.0, Deaths: 30.0, Negative: 7399.0, Total Tested: 8628", "CA\nPositive: 15865.0, Deaths: 374.0, Negative: 115364.0, Total Tested: 145329", "WV\nPositive: 412.0, Deaths: 4.0, Negative: 11647.0, Total Tested: 12059", "MS\nPositive: 1915.0, Deaths: 59.0, Negative: 18632.0, Total Tested: 20547", "VT\nPositive: 575.0, Deaths: 23.0, Negative: 6554.0, Total Tested: 7129", "KY\nPositive: 1008.0, Deaths: 59.0, Negative: 18947.0, Total Tested: 19955", "NE\nPositive: 447.0, Deaths: 10.0, Negative: 6811.0, Total Tested: 7258", "OH\nPositive: 4782.0, Deaths: 167.0, Negative: 46056.0, Total Tested: 50838", "DC\nPositive: 1211.0, Deaths: 22.0, Negative: 6612.0, Total Tested: 7823", "NH\nPositive: 715.0, Deaths: 9.0, Negative: 8019.0, Total Tested: 8783", "IA\nPositive: 1048.0, Deaths: 26.0, Negative: 11670.0, Total Tested: 12718", "AL\nPositive: 2119.0, Deaths: 56.0, Negative: 12797.0, Total Tested: 14916", "CO\nPositive: 5172.0, Deaths: 150.0, Negative: 21703.0, Total Tested: 26875", "MO\nPositive: 3037.0, Deaths: 53.0, Negative: 28932.0, Total Tested: 31969", "OR\nPositive: 1132.0, Deaths: 29.0, Negative: 20669.0, Total Tested: 21801", "TN\nPositive: 4138.0, Deaths: 72.0, Negative: 48736.0, Total Tested: 52874", "WA\nPositive: 8384.0, Deaths: 372.0, Negative: 83391.0, Total Tested: 91775", "MA\nPositive: 15202.0, Deaths: 356.0, Negative: 66142.0, Total Tested: 81344", "SD\nPositive: 320.0, Deaths: 6.0, Negative: 5948.0, Total Tested: 6270", "OK\nPositive: 1472.0, Deaths: 67.0, Negative: 11821.0, Total Tested: 13293", "ID\nPositive: 1170.0, Deaths: 13.0, Negative: 10076.0, Total Tested: 11246", "HI\nPositive: 387.0, Deaths: 5.0, Negative: 13155.0, Total Tested: 13542", "KS\nPositive: 900.0, Deaths: 27.0, Negative: 8614.0, Total Tested: 9514", "AR\nPositive: 946.0, Deaths: 16.0, Negative: 12692.0, Total Tested: 13638", "NM\nPositive: 686.0, Deaths: 12.0, Negative: 21139.0, Total Tested: 21825", "ME\nPositive: 519.0, Deaths: 12.0, Negative: 6088.0, Total Tested: 6607", "TX\nPositive: 8262.0, Deaths: 154.0, Negative: 80387.0, Total Tested: 88649", "NY\nPositive: 138863.0, Deaths: 5489.0, Negative: 201195.0, Total Tested: 340058", "WI\nPositive: 2578.0, Deaths: 92.0, Negative: 28512.0, Total Tested: 31090", "VA\nPositive: 3333.0, Deaths: 63.0, Negative: 25312.0, Total Tested: 28645", "SC\nPositive: 2417.0, Deaths: 51.0, Negative: 21263.0, Total Tested: 23680", "AK\nPositive: 213.0, Deaths: 6.0, Negative: 6700.0, Total Tested: 6913", "PA\nPositive: 14559.0, Deaths: 240.0, Negative: 76719.0, Total Tested: 91278", "MI\nPositive: 18970.0, Deaths: 845.0, Negative: 31362.0, Total Tested: 50332", "MT\nPositive: 319.0, Deaths: 6.0, Negative: 6666.0, Total Tested: 6985", "WY\nPositive: 216.0, Deaths: 0.0, Negative: 3789.0, Total Tested: 4005"], "type": "choropleth", "z": [13.55529938292534, null, 13.924050632911392, 25.303134294211848, null, null, 20.117940576094355, null, null, null, 22.63797942001871, null, 8.51553509781358, null, null, null, null, null, 19.68668407310705, 7.82608695652174, null, null, 28.31451275616897, null, 14.405594405594405, 18.416030534351144, 12.789051439358188, 19.218870843000772, null, 35.68904593639576, 9.859835669405511, null, 9.439547427970004, 7.187499999999999, 25.543478260869566, 7.094017094017094, 6.718346253229974, 24.77777777777778, 13.742071881606766, null, 19.07514450867052, null, 23.10406659801387, 28.898370830100855, 16.891689168916894, 9.971038477451385, 10.7981220657277, null, null, 8.77742946708464, 15.277777777777779]}],
                        {"geo": {"lakecolor": "rgb(255, 255, 255)", "projection": {"type": "albers usa"}, "scope": "usa", "showlakes": true}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Hospitalization rate for positive cases<br>(Hover for breakdown)"}},
                        {"responsive": true}
                    ).then(function(){

var gd = document.getElementById('9244ac2a-07e8-429f-8289-24f4f4dad230');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>



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
fig.show();
```


<div>


            <div id="8a6c2323-c64f-47af-8d63-017213e05cfd" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};

                if (document.getElementById("8a6c2323-c64f-47af-8d63-017213e05cfd")) {
                    Plotly.newPlot(
                        '8a6c2323-c64f-47af-8d63-017213e05cfd',
                        [{"autocolorscale": false, "colorbar": {"title": {"text": "Death rate in %"}}, "colorscale": [[0.0, "rgb(255,245,235)"], [0.125, "rgb(254,230,206)"], [0.25, "rgb(253,208,162)"], [0.375, "rgb(253,174,107)"], [0.5, "rgb(253,141,60)"], [0.625, "rgb(241,105,19)"], [0.75, "rgb(217,72,1)"], [0.875, "rgb(166,54,3)"], [1.0, "rgb(127,39,4)"]], "locationmode": "USA-states", "locations": ["FL", "CT", "ND", "MD", "LA", "DE", "GA", "NJ", "IL", "NV", "MN", "NC", "UT", "AZ", "IN", "RI", "CA", "WV", "MS", "VT", "KY", "NE", "OH", "DC", "NH", "IA", "AL", "CO", "MO", "OR", "TN", "WA", "MA", "SD", "OK", "ID", "HI", "KS", "AR", "NM", "ME", "TX", "NY", "WI", "VA", "SC", "AK", "PA", "MI", "MT", "WY"], "marker": {"line": {"color": "white"}}, "text": ["FL\nPositive: 14747.0, Deaths: 296.0, Negative: 123415.0, Total Tested: 139569", "CT\nPositive: 7781.0, Deaths: 277.0, Negative: 21255.0, Total Tested: 29036", "ND\nPositive: 237.0, Deaths: 4.0, Negative: 7466.0, Total Tested: 7703", "MD\nPositive: 4371.0, Deaths: 103.0, Negative: 27256.0, Total Tested: 31627", "LA\nPositive: 16284.0, Deaths: 582.0, Negative: 58371.0, Total Tested: 74655", "DE\nPositive: 928.0, Deaths: 16.0, Negative: 7628.0, Total Tested: 8556", "GA\nPositive: 8818.0, Deaths: 329.0, Negative: 24895.0, Total Tested: 33713", "NJ\nPositive: 44416.0, Deaths: 1232.0, Negative: 50558.0, Total Tested: 94974", "IL\nPositive: 13549.0, Deaths: 380.0, Negative: 55183.0, Total Tested: 68732", "NV\nPositive: 2087.0, Deaths: 58.0, Negative: 16552.0, Total Tested: 18639", "MN\nPositive: 1069.0, Deaths: 34.0, Negative: 28191.0, Total Tested: 29260", "NC\nPositive: 3221.0, Deaths: 46.0, Negative: 37861.0, Total Tested: 41082", "UT\nPositive: 1738.0, Deaths: 13.0, Negative: 32909.0, Total Tested: 34647", "AZ\nPositive: 2575.0, Deaths: 73.0, Negative: 30800.0, Total Tested: 33375", "IN\nPositive: 5507.0, Deaths: 173.0, Negative: 23257.0, Total Tested: 28764", "RI\nPositive: 1229.0, Deaths: 30.0, Negative: 7399.0, Total Tested: 8628", "CA\nPositive: 15865.0, Deaths: 374.0, Negative: 115364.0, Total Tested: 145329", "WV\nPositive: 412.0, Deaths: 4.0, Negative: 11647.0, Total Tested: 12059", "MS\nPositive: 1915.0, Deaths: 59.0, Negative: 18632.0, Total Tested: 20547", "VT\nPositive: 575.0, Deaths: 23.0, Negative: 6554.0, Total Tested: 7129", "KY\nPositive: 1008.0, Deaths: 59.0, Negative: 18947.0, Total Tested: 19955", "NE\nPositive: 447.0, Deaths: 10.0, Negative: 6811.0, Total Tested: 7258", "OH\nPositive: 4782.0, Deaths: 167.0, Negative: 46056.0, Total Tested: 50838", "DC\nPositive: 1211.0, Deaths: 22.0, Negative: 6612.0, Total Tested: 7823", "NH\nPositive: 715.0, Deaths: 9.0, Negative: 8019.0, Total Tested: 8783", "IA\nPositive: 1048.0, Deaths: 26.0, Negative: 11670.0, Total Tested: 12718", "AL\nPositive: 2119.0, Deaths: 56.0, Negative: 12797.0, Total Tested: 14916", "CO\nPositive: 5172.0, Deaths: 150.0, Negative: 21703.0, Total Tested: 26875", "MO\nPositive: 3037.0, Deaths: 53.0, Negative: 28932.0, Total Tested: 31969", "OR\nPositive: 1132.0, Deaths: 29.0, Negative: 20669.0, Total Tested: 21801", "TN\nPositive: 4138.0, Deaths: 72.0, Negative: 48736.0, Total Tested: 52874", "WA\nPositive: 8384.0, Deaths: 372.0, Negative: 83391.0, Total Tested: 91775", "MA\nPositive: 15202.0, Deaths: 356.0, Negative: 66142.0, Total Tested: 81344", "SD\nPositive: 320.0, Deaths: 6.0, Negative: 5948.0, Total Tested: 6270", "OK\nPositive: 1472.0, Deaths: 67.0, Negative: 11821.0, Total Tested: 13293", "ID\nPositive: 1170.0, Deaths: 13.0, Negative: 10076.0, Total Tested: 11246", "HI\nPositive: 387.0, Deaths: 5.0, Negative: 13155.0, Total Tested: 13542", "KS\nPositive: 900.0, Deaths: 27.0, Negative: 8614.0, Total Tested: 9514", "AR\nPositive: 946.0, Deaths: 16.0, Negative: 12692.0, Total Tested: 13638", "NM\nPositive: 686.0, Deaths: 12.0, Negative: 21139.0, Total Tested: 21825", "ME\nPositive: 519.0, Deaths: 12.0, Negative: 6088.0, Total Tested: 6607", "TX\nPositive: 8262.0, Deaths: 154.0, Negative: 80387.0, Total Tested: 88649", "NY\nPositive: 138863.0, Deaths: 5489.0, Negative: 201195.0, Total Tested: 340058", "WI\nPositive: 2578.0, Deaths: 92.0, Negative: 28512.0, Total Tested: 31090", "VA\nPositive: 3333.0, Deaths: 63.0, Negative: 25312.0, Total Tested: 28645", "SC\nPositive: 2417.0, Deaths: 51.0, Negative: 21263.0, Total Tested: 23680", "AK\nPositive: 213.0, Deaths: 6.0, Negative: 6700.0, Total Tested: 6913", "PA\nPositive: 14559.0, Deaths: 240.0, Negative: 76719.0, Total Tested: 91278", "MI\nPositive: 18970.0, Deaths: 845.0, Negative: 31362.0, Total Tested: 50332", "MT\nPositive: 319.0, Deaths: 6.0, Negative: 6666.0, Total Tested: 6985", "WY\nPositive: 216.0, Deaths: 0.0, Negative: 3789.0, Total Tested: 4005"], "type": "choropleth", "z": [2.0071879026242625, 3.559953733453284, 1.6877637130801686, 2.3564401738732554, 3.574060427413412, 1.7241379310344827, 3.731004762984804, 2.7737752161383287, 2.8046350284153814, 2.7791087685673217, 3.1805425631431246, 1.4281279105867744, 0.7479861910241657, 2.8349514563106797, 3.1414563283094243, 2.4410089503661516, 2.357390482193508, 0.9708737864077669, 3.0809399477806787, 4.0, 5.853174603174603, 2.237136465324385, 3.4922626516102047, 1.8166804293971925, 1.2587412587412588, 2.480916030534351, 2.642756016989146, 2.9002320185614847, 1.7451432334540666, 2.5618374558303887, 1.7399710004833253, 4.437022900763359, 2.3417971319563216, 1.875, 4.551630434782608, 1.1111111111111112, 1.2919896640826873, 3.0, 1.6913319238900635, 1.749271137026239, 2.312138728323699, 1.8639554587267004, 3.9528168050524615, 3.5686578743211794, 1.8901890189018902, 2.110053785684733, 2.8169014084507045, 1.6484648670925202, 4.454401686874012, 1.8808777429467085, 0.0]}],
                        {"geo": {"lakecolor": "rgb(255, 255, 255)", "projection": {"type": "albers usa"}, "scope": "usa", "showlakes": true}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Death rate by state<br>(Hover for breakdown)"}},
                        {"responsive": true}
                    ).then(function(){

var gd = document.getElementById('8a6c2323-c64f-47af-8d63-017213e05cfd');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>



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


<div>


            <div id="96ab4d64-8f87-4ea4-897f-bc7b3f18636f" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};

                if (document.getElementById("96ab4d64-8f87-4ea4-897f-bc7b3f18636f")) {
                    Plotly.newPlot(
                        '96ab4d64-8f87-4ea4-897f-bc7b3f18636f',
                        [{"autocolorscale": false, "colorbar": {"title": {"text": "Percent of state population tested (in %)"}}, "colorscale": [[0.0, "rgb(255,245,235)"], [0.125, "rgb(254,230,206)"], [0.25, "rgb(253,208,162)"], [0.375, "rgb(253,174,107)"], [0.5, "rgb(253,141,60)"], [0.625, "rgb(241,105,19)"], [0.75, "rgb(217,72,1)"], [0.875, "rgb(166,54,3)"], [1.0, "rgb(127,39,4)"]], "locationmode": "USA-states", "locations": ["FL", "CT", "ND", "MD", "LA", "DE", "GA", "NJ", "IL", "NV", "MN", "NC", "UT", "AZ", "IN", "RI", "CA", "WV", "MS", "VT", "KY", "NE", "OH", "DC", "NH", "IA", "AL", "CO", "MO", "OR", "TN", "WA", "MA", "SD", "OK", "ID", "HI", "KS", "AR", "NM", "ME", "TX", "NY", "WI", "VA", "SC", "AK", "PA", "MI", "MT", "WY"], "marker": {"line": {"color": "white"}}, "text": ["FL\nPositive: 14747.0, Deaths: 296.0, Negative: 123415.0, Total Tested: 139569", "CT\nPositive: 7781.0, Deaths: 277.0, Negative: 21255.0, Total Tested: 29036", "ND\nPositive: 237.0, Deaths: 4.0, Negative: 7466.0, Total Tested: 7703", "MD\nPositive: 4371.0, Deaths: 103.0, Negative: 27256.0, Total Tested: 31627", "LA\nPositive: 16284.0, Deaths: 582.0, Negative: 58371.0, Total Tested: 74655", "DE\nPositive: 928.0, Deaths: 16.0, Negative: 7628.0, Total Tested: 8556", "GA\nPositive: 8818.0, Deaths: 329.0, Negative: 24895.0, Total Tested: 33713", "NJ\nPositive: 44416.0, Deaths: 1232.0, Negative: 50558.0, Total Tested: 94974", "IL\nPositive: 13549.0, Deaths: 380.0, Negative: 55183.0, Total Tested: 68732", "NV\nPositive: 2087.0, Deaths: 58.0, Negative: 16552.0, Total Tested: 18639", "MN\nPositive: 1069.0, Deaths: 34.0, Negative: 28191.0, Total Tested: 29260", "NC\nPositive: 3221.0, Deaths: 46.0, Negative: 37861.0, Total Tested: 41082", "UT\nPositive: 1738.0, Deaths: 13.0, Negative: 32909.0, Total Tested: 34647", "AZ\nPositive: 2575.0, Deaths: 73.0, Negative: 30800.0, Total Tested: 33375", "IN\nPositive: 5507.0, Deaths: 173.0, Negative: 23257.0, Total Tested: 28764", "RI\nPositive: 1229.0, Deaths: 30.0, Negative: 7399.0, Total Tested: 8628", "CA\nPositive: 15865.0, Deaths: 374.0, Negative: 115364.0, Total Tested: 145329", "WV\nPositive: 412.0, Deaths: 4.0, Negative: 11647.0, Total Tested: 12059", "MS\nPositive: 1915.0, Deaths: 59.0, Negative: 18632.0, Total Tested: 20547", "VT\nPositive: 575.0, Deaths: 23.0, Negative: 6554.0, Total Tested: 7129", "KY\nPositive: 1008.0, Deaths: 59.0, Negative: 18947.0, Total Tested: 19955", "NE\nPositive: 447.0, Deaths: 10.0, Negative: 6811.0, Total Tested: 7258", "OH\nPositive: 4782.0, Deaths: 167.0, Negative: 46056.0, Total Tested: 50838", "DC\nPositive: 1211.0, Deaths: 22.0, Negative: 6612.0, Total Tested: 7823", "NH\nPositive: 715.0, Deaths: 9.0, Negative: 8019.0, Total Tested: 8783", "IA\nPositive: 1048.0, Deaths: 26.0, Negative: 11670.0, Total Tested: 12718", "AL\nPositive: 2119.0, Deaths: 56.0, Negative: 12797.0, Total Tested: 14916", "CO\nPositive: 5172.0, Deaths: 150.0, Negative: 21703.0, Total Tested: 26875", "MO\nPositive: 3037.0, Deaths: 53.0, Negative: 28932.0, Total Tested: 31969", "OR\nPositive: 1132.0, Deaths: 29.0, Negative: 20669.0, Total Tested: 21801", "TN\nPositive: 4138.0, Deaths: 72.0, Negative: 48736.0, Total Tested: 52874", "WA\nPositive: 8384.0, Deaths: 372.0, Negative: 83391.0, Total Tested: 91775", "MA\nPositive: 15202.0, Deaths: 356.0, Negative: 66142.0, Total Tested: 81344", "SD\nPositive: 320.0, Deaths: 6.0, Negative: 5948.0, Total Tested: 6270", "OK\nPositive: 1472.0, Deaths: 67.0, Negative: 11821.0, Total Tested: 13293", "ID\nPositive: 1170.0, Deaths: 13.0, Negative: 10076.0, Total Tested: 11246", "HI\nPositive: 387.0, Deaths: 5.0, Negative: 13155.0, Total Tested: 13542", "KS\nPositive: 900.0, Deaths: 27.0, Negative: 8614.0, Total Tested: 9514", "AR\nPositive: 946.0, Deaths: 16.0, Negative: 12692.0, Total Tested: 13638", "NM\nPositive: 686.0, Deaths: 12.0, Negative: 21139.0, Total Tested: 21825", "ME\nPositive: 519.0, Deaths: 12.0, Negative: 6088.0, Total Tested: 6607", "TX\nPositive: 8262.0, Deaths: 154.0, Negative: 80387.0, Total Tested: 88649", "NY\nPositive: 138863.0, Deaths: 5489.0, Negative: 201195.0, Total Tested: 340058", "WI\nPositive: 2578.0, Deaths: 92.0, Negative: 28512.0, Total Tested: 31090", "VA\nPositive: 3333.0, Deaths: 63.0, Negative: 25312.0, Total Tested: 28645", "SC\nPositive: 2417.0, Deaths: 51.0, Negative: 21263.0, Total Tested: 23680", "AK\nPositive: 213.0, Deaths: 6.0, Negative: 6700.0, Total Tested: 6913", "PA\nPositive: 14559.0, Deaths: 240.0, Negative: 76719.0, Total Tested: 91278", "MI\nPositive: 18970.0, Deaths: 845.0, Negative: 31362.0, Total Tested: 50332", "MT\nPositive: 319.0, Deaths: 6.0, Negative: 6666.0, Total Tested: 6985", "WY\nPositive: 216.0, Deaths: 0.0, Negative: 3789.0, Total Tested: 4005"], "type": "choropleth", "z": [0.6498310320123577, 0.8144084894147372, 1.0108101440565203, 0.5231338741051462, 1.6059003689989275, 0.8786523223286136, 0.3175252601313897, 1.069263323572227, 0.5424003385148827, 0.6051316881352763, 0.5188281788598972, 0.3917016682932746, 1.0807066093816575, 0.458528611567121, 0.4272588280327779, 0.8144532411519775, 0.3678077034541944, 0.6728800706638463, 0.690388821258613, 1.1424880887323334, 0.4466531010662598, 0.3752052307475982, 0.43491800053040863, 1.1084677413641393, 0.6459460870729148, 0.40309723714529316, 0.3042104264880889, 0.4666822719430097, 0.5208859476640704, 0.516888558959461, 0.7742371185739301, 1.2052040652442524, 1.1801808428665175, 0.7087476643542879, 0.33593877741332956, 0.6292999974819047, 0.9564423902725671, 0.32656967288798944, 0.45191801720721425, 1.0408574089732638, 0.4915147313072641, 0.30572963104656137, 1.7480501384810732, 0.5339691270008385, 0.33559763618357596, 0.4599206714531046, 0.9449862961266908, 0.7129985817047647, 0.5039823840473534, 0.653550129212989, 0.6919978782187405]}],
                        {"geo": {"lakecolor": "rgb(255, 255, 255)", "projection": {"type": "albers usa"}, "scope": "usa", "showlakes": true}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Percent of State Population tested<br>(Hover for breakdown)"}},
                        {"responsive": true}
                    ).then(function(){

var gd = document.getElementById('96ab4d64-8f87-4ea4-897f-bc7b3f18636f');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>



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
fig.show();
```


<div>


            <div id="ae41ab49-8207-40d9-b8ec-bb92f2182db1" class="plotly-graph-div" style="height:525px; width:100%;"></div>
            <script type="text/javascript">
                require(["plotly"], function(Plotly) {
                    window.PLOTLYENV=window.PLOTLYENV || {};

                if (document.getElementById("ae41ab49-8207-40d9-b8ec-bb92f2182db1")) {
                    Plotly.newPlot(
                        'ae41ab49-8207-40d9-b8ec-bb92f2182db1',
                        [{"autocolorscale": false, "colorbar": {"title": {"text": "Number of Unemp. Ins. Claims since Stay-at-home Orders"}}, "colorscale": [[0.0, "rgb(255,245,235)"], [0.125, "rgb(254,230,206)"], [0.25, "rgb(253,208,162)"], [0.375, "rgb(253,174,107)"], [0.5, "rgb(253,141,60)"], [0.625, "rgb(241,105,19)"], [0.75, "rgb(217,72,1)"], [0.875, "rgb(166,54,3)"], [1.0, "rgb(127,39,4)"]], "locationmode": "USA-states", "locations": ["FL", "CT", "ND", "MD", "LA", "DE", "GA", "NJ", "IL", "NV", "MN", "NC", "UT", "AZ", "IN", "RI", "CA", "WV", "MS", "VT", "KY", "NE", "OH", "DC", "NH", "IA", "AL", "CO", "MO", "OR", "TN", "WA", "MA", "SD", "OK", "ID", "HI", "KS", "AR", "NM", "ME", "TX", "NY", "WI", "VA", "SC", "AK", "PA", "MI", "MT", "WY"], "marker": {"line": {"color": "white"}}, "text": ["FL\nPositive: 14747.0, Deaths: 296.0, Negative: 123415.0, Total Tested: 139569", "CT\nPositive: 7781.0, Deaths: 277.0, Negative: 21255.0, Total Tested: 29036", "ND\nPositive: 237.0, Deaths: 4.0, Negative: 7466.0, Total Tested: 7703", "MD\nPositive: 4371.0, Deaths: 103.0, Negative: 27256.0, Total Tested: 31627", "LA\nPositive: 16284.0, Deaths: 582.0, Negative: 58371.0, Total Tested: 74655", "DE\nPositive: 928.0, Deaths: 16.0, Negative: 7628.0, Total Tested: 8556", "GA\nPositive: 8818.0, Deaths: 329.0, Negative: 24895.0, Total Tested: 33713", "NJ\nPositive: 44416.0, Deaths: 1232.0, Negative: 50558.0, Total Tested: 94974", "IL\nPositive: 13549.0, Deaths: 380.0, Negative: 55183.0, Total Tested: 68732", "NV\nPositive: 2087.0, Deaths: 58.0, Negative: 16552.0, Total Tested: 18639", "MN\nPositive: 1069.0, Deaths: 34.0, Negative: 28191.0, Total Tested: 29260", "NC\nPositive: 3221.0, Deaths: 46.0, Negative: 37861.0, Total Tested: 41082", "UT\nPositive: 1738.0, Deaths: 13.0, Negative: 32909.0, Total Tested: 34647", "AZ\nPositive: 2575.0, Deaths: 73.0, Negative: 30800.0, Total Tested: 33375", "IN\nPositive: 5507.0, Deaths: 173.0, Negative: 23257.0, Total Tested: 28764", "RI\nPositive: 1229.0, Deaths: 30.0, Negative: 7399.0, Total Tested: 8628", "CA\nPositive: 15865.0, Deaths: 374.0, Negative: 115364.0, Total Tested: 145329", "WV\nPositive: 412.0, Deaths: 4.0, Negative: 11647.0, Total Tested: 12059", "MS\nPositive: 1915.0, Deaths: 59.0, Negative: 18632.0, Total Tested: 20547", "VT\nPositive: 575.0, Deaths: 23.0, Negative: 6554.0, Total Tested: 7129", "KY\nPositive: 1008.0, Deaths: 59.0, Negative: 18947.0, Total Tested: 19955", "NE\nPositive: 447.0, Deaths: 10.0, Negative: 6811.0, Total Tested: 7258", "OH\nPositive: 4782.0, Deaths: 167.0, Negative: 46056.0, Total Tested: 50838", "DC\nPositive: 1211.0, Deaths: 22.0, Negative: 6612.0, Total Tested: 7823", "NH\nPositive: 715.0, Deaths: 9.0, Negative: 8019.0, Total Tested: 8783", "IA\nPositive: 1048.0, Deaths: 26.0, Negative: 11670.0, Total Tested: 12718", "AL\nPositive: 2119.0, Deaths: 56.0, Negative: 12797.0, Total Tested: 14916", "CO\nPositive: 5172.0, Deaths: 150.0, Negative: 21703.0, Total Tested: 26875", "MO\nPositive: 3037.0, Deaths: 53.0, Negative: 28932.0, Total Tested: 31969", "OR\nPositive: 1132.0, Deaths: 29.0, Negative: 20669.0, Total Tested: 21801", "TN\nPositive: 4138.0, Deaths: 72.0, Negative: 48736.0, Total Tested: 52874", "WA\nPositive: 8384.0, Deaths: 372.0, Negative: 83391.0, Total Tested: 91775", "MA\nPositive: 15202.0, Deaths: 356.0, Negative: 66142.0, Total Tested: 81344", "SD\nPositive: 320.0, Deaths: 6.0, Negative: 5948.0, Total Tested: 6270", "OK\nPositive: 1472.0, Deaths: 67.0, Negative: 11821.0, Total Tested: 13293", "ID\nPositive: 1170.0, Deaths: 13.0, Negative: 10076.0, Total Tested: 11246", "HI\nPositive: 387.0, Deaths: 5.0, Negative: 13155.0, Total Tested: 13542", "KS\nPositive: 900.0, Deaths: 27.0, Negative: 8614.0, Total Tested: 9514", "AR\nPositive: 946.0, Deaths: 16.0, Negative: 12692.0, Total Tested: 13638", "NM\nPositive: 686.0, Deaths: 12.0, Negative: 21139.0, Total Tested: 21825", "ME\nPositive: 519.0, Deaths: 12.0, Negative: 6088.0, Total Tested: 6607", "TX\nPositive: 8262.0, Deaths: 154.0, Negative: 80387.0, Total Tested: 88649", "NY\nPositive: 138863.0, Deaths: 5489.0, Negative: 201195.0, Total Tested: 340058", "WI\nPositive: 2578.0, Deaths: 92.0, Negative: 28512.0, Total Tested: 31090", "VA\nPositive: 3333.0, Deaths: 63.0, Negative: 25312.0, Total Tested: 28645", "SC\nPositive: 2417.0, Deaths: 51.0, Negative: 21263.0, Total Tested: 23680", "AK\nPositive: 213.0, Deaths: 6.0, Negative: 6700.0, Total Tested: 6913", "PA\nPositive: 14559.0, Deaths: 240.0, Negative: 76719.0, Total Tested: 91278", "MI\nPositive: 18970.0, Deaths: 845.0, Negative: 31362.0, Total Tested: 50332", "MT\nPositive: 319.0, Deaths: 6.0, Negative: 6666.0, Total Tested: 6985", "WY\nPositive: 216.0, Deaths: 0.0, Negative: 3789.0, Total Tested: 4005"], "type": "choropleth", "z": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 115815.0, 114114.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 186333.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 79999.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}],
                        {"geo": {"lakecolor": "rgb(255, 255, 255)", "projection": {"type": "albers usa"}, "scope": "usa", "showlakes": true}, "template": {"data": {"bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Number of Unemp. Ins. Claims since Stay-at-home Orders, by State<br>(Hover for breakdown)"}},
                        {"responsive": true}
                    ).then(function(){

var gd = document.getElementById('ae41ab49-8207-40d9-b8ec-bb92f2182db1');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});

// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}

// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}

                        })
                };
                });
            </script>
        </div>



```python

```