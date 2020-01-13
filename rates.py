import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


ruonia = pd.read_csv(r'app\static\tables\ruonia.csv')
fed = pd.read_csv(r'app\static\tables\fed.csv')
cbr_rate = pd.read_csv(r'app\static\tables\cbr_rate.csv')

trace_ruonia = go.Scatter(
    x=ruonia['Date'],
    y=ruonia['Ruonia'],
    showlegend=True,
    name='RUONIA',
    marker=dict(color='teal'),
    line={'width':1},
    yaxis='y1')

trace_fed = go.Scatter(
    x=fed['Release Date'],
    y=fed['Actual'],
    showlegend=True,
    name='Учетная ставка ФРС',
    marker=dict(color='orange'),
    line={'width':1},
    yaxis='y1')

trace_cbr_rate = go.Scatter(
    x=cbr_rate['Release Date'],
    y=cbr_rate['Actual'],
    showlegend=True,
    name='Ключевая ставка Банка России',
    marker=dict(color='purple'),
    line={'width':1},
    yaxis='y1')

data = [trace_ruonia, trace_fed, trace_cbr_rate]

layout = go.Layout(title='Индикаторы денежного рынка',
                       xaxis1=dict(
                       tickformat='%m.%y',
                       dtick='M1'),
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
py.offline.plot(fig, filename=r'app\templates\rates.html', auto_open=False, config=config)