import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


gold = pd.read_csv(r'app\static\tables\gold.csv')
silver = pd.read_csv(r'app\static\tables\silver.csv')

trace_gold = go.Scatter(
    x=gold['Date'],
    y=gold['Price'],
    showlegend=True,
    name='Золото, $/унция',
    marker=dict(color='orange'),
    line={'width':1},
    yaxis='y1')

trace_silver = go.Scatter(
    x=silver['Date'],
    y=silver['Price'],
    showlegend=True,
    name='Серебро, $/унция',
    marker=dict(color='gray'),
    line={'width':1},
    yaxis='y2')

data = [trace_gold, trace_silver]

layout = go.Layout(title='Драгметаллы',
                   xaxis=dict(tickformat='%m.%y',
                              dtick="M1"),
                   yaxis=dict(
                            tickfont=dict(color='orange')),
                   yaxis2=dict(
                       overlaying='y1',
                       side='right'),
                       font=dict(size=config.LAYOUT_FONT_SIZE),
                       legend=dict(
                           orientation='h',
                           x=0,
                           y=-0.2
                                   ),
                   width=config.COMMODITIES_WIDTH,
                   height=config.COMMODITIES_HEIGHT,
                   margin=config.MARGINS
                   )


fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\gold_silver.html', auto_open=False, config=config)