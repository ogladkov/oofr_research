import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


usdrub = pd.read_csv(r'app\static\tables\usdrub.csv')
eurusd = pd.read_csv(r'app\static\tables\eurusd.csv')
eurrub = pd.read_csv(r'app\static\tables\eurrub.csv')

trace_usdrub = go.Scatter(
    x=usdrub['Date'],
    y=usdrub['Price'],
    showlegend=True,
    name='USD/RUB',
    marker=dict(color='teal'),
    line={'width':1},
    yaxis='y1')

trace_eurusd = go.Scatter(
    x=eurusd['Date'],
    y=eurusd['Price'],
    showlegend=True,
    name='EUR/USD',
    marker=dict(color='orange'),
    line={'width':1},
    yaxis='y2')

trace_eurrub = go.Scatter(
    x=eurrub['Date'],
    y=eurrub['Price'],
    showlegend=True,
    name='EUR/RUB',
    marker=dict(color='purple'),
    line={'width':1},
    yaxis='y1')

data = [trace_usdrub, trace_eurusd, trace_eurrub]

layout = go.Layout(title='Валютные рынки',
                   xaxis1=dict(
                       tickformat='%m.%y',
                       dtick='M2'
                   ),
                   yaxis=dict(side='right'),
                   yaxis2=dict(
                            tickfont=dict(color='orange'),
                           overlaying='y1'),
                   width=config.CURRENCY_1_WIDTH,
                   height=config.CURRENCY_1_HEIGHT,
                   margin=config.MARGINS,
                   legend=dict(
                                orientation='h',
                                x=0,
                                y=-0.1
                                )
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\fx.html', auto_open=False, config=config)