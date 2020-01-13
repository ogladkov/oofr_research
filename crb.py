import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


crb = pd.read_csv(r'app\static\tables\crb.csv')

trace_crb= go.Scatter(
    x=crb['Date'],
    y=crb['Price'],
    showlegend=False,
    name='CRB Jefferies',
    marker=dict(color='purple'),
    line={'width':1},
    yaxis='y1')

data = [trace_crb]

layout = go.Layout(title='CRB Jefferies',
                   xaxis=dict(tickformat='%m.%y', dtick="M1"),
                   width=config.COMMODITIES_WIDTH,
                   height=config.COMMODITIES_HEIGHT,
                   margin=config.MARGINS,
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\crb.html', auto_open=False, config=config)