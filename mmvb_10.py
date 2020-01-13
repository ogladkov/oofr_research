import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


mmvb_10 = pd.read_csv(r'app\static\tables\mmvb_10.csv')

trace_mmvb_10 = go.Scatter(
    x=mmvb_10['<DATE>'],
    y=mmvb_10['<CLOSE>'],
    showlegend=False,
    name='Динамика индекса ММВБ-10',
    marker=dict(color='teal'),
    line={'width':1},
    yaxis='y1')

data = [trace_mmvb_10]

layout = go.Layout(title='Динамика индекса ММВБ-10',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   xaxis=dict(tickformat='%m.%y', dtick="M1"),
                   width=config.STOCKS_1_WIDTH,
                   height=config.STOCKS_1_HEIGHT,
                   margin=config.MARGINS
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\mmvb_10.html', auto_open=False, config=config)