import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


msci = pd.read_csv(r'app\static\tables\msci.csv')

trace_msci = go.Scatter(
    x=msci['Date'],
    y=msci['Price'],
    showlegend=False,
    name='Индекс MSCI-BRICS, USD',
    marker=dict(color='orange'),
    line={'width':1},
    yaxis='y1')

data = [trace_msci]

layout = go.Layout(title='Индекс MSCI-BRICS, USD',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                       orientation='h'
                   ),
                   xaxis=dict(tickformat='%m.%y', dtick="M1"),
                   width=config.STOCKS_1_WIDTH,
                   height=config.STOCKS_1_HEIGHT,
                   margin=config.MARGINS
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\msci.html', auto_open=False, config=config)