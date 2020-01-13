import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


rvi = pd.read_csv(r'app\static\tables\rvi.csv')

trace_rvi= go.Scatter(
    x=rvi['Date'],
    y=rvi['Close'],
    showlegend=False,
    name='RVI',
    marker=dict(color='purple'),
    line={'width':1},
    yaxis='y1')

data = [trace_rvi]

layout = go.Layout(title='Индекс волатильности RVI',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                       orientation='h'),
                   xaxis=dict(tickformat='%m.%y', dtick="M1"),
                   width=config.SPFI_WIDTH,
                   height=config.SPFI_HEIGHT,
                   margin=config.MARGINS)

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\rvi.html', auto_open=False, config=config)