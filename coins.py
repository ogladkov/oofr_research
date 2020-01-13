import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


coin_gold = pd.read_csv(r'app\static\tables\coin_gold.csv')
coin_silver = pd.read_csv(r'app\static\tables\coin_silver.csv')

trace_coin_gold= go.Scatter(
    x=coin_gold['Date'],
    y=coin_gold['Price'],
    showlegend=True,
    name='Монеты (золото)',
    marker=dict(color='red'),
    line={'width':1},
    yaxis='y1')

trace_coin_silver= go.Scatter(
    x=coin_silver['Date'],
    y=coin_silver['Price'],
    showlegend=True,
    name='Монеты (серебро)',
    marker=dict(color='teal'),
    line={'width':1},
    yaxis='y2')

data = [trace_coin_gold, trace_coin_silver]

layout = go.Layout(title='Отпускные цены монет "Георгий Победоносец"',
                   xaxis=dict(tickformat='%m.%y', dtick="M1"),
                   yaxis=dict(tickfont=dict(color='red')),
                   yaxis2=dict(overlaying='y1',
                               tickfont=dict(color='teal'),
                               side='right'),
                   legend=dict(
                           orientation='h',
                           x=0,
                           y=-0.2),
                   width=config.COMMODITIES_WIDTH,
                   height=config.COMMODITIES_HEIGHT,
                   margin=config.MARGINS,
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   )


fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\coins.html', auto_open=False, config=config)