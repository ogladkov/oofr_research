import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


gcurve = pd.read_csv(r'app\static\tables\gcurve.csv')

trace_gcurve_y = go.Scatter(
    x=gcurve['r'],
    y=gcurve['w0']/100,
    showlegend=True,
    name='Текущая неделя',
    marker=dict(color='red'),
    line={'width':1},
    yaxis='y1')

trace_gcurve_w = go.Scatter(
    x=gcurve['r'],
    y=gcurve['w1']/100,
    showlegend=True,
    name='Прошлая неделя',
    marker=dict(color='teal'),
    line={'width':1},
    yaxis='y1')

data = [trace_gcurve_y, trace_gcurve_w]

layout = go.Layout(title='Значения бескупонной доходности',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                       orientation='h'
                   ),
                   width=config.DEBTS_WIDTH,
                   height=config.DEBTS_HEIGHT,
                   margin=config.MARGINS
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\gcurve.html', auto_open=False, config=config)