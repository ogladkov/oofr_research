import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


brent = pd.read_csv(r'app\static\tables\brent.csv')

trace_brent = go.Scatter(
    x=brent['Date'],
    y=brent['Price'],
    showlegend=True,
    name='Нефть, $/баррель',
    marker=dict(color='black'),
    line={'width':1},
    yaxis='y1')

data = [trace_brent]

layout = go.Layout(title='Нефть Brent',
                   xaxis=dict(tickformat='%m.%y',
                              dtick="M1",
                              ),
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

config={'showLink': False}
fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig, filename=r'app\templates\brent.html', auto_open=False, config=config)