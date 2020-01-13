import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


smile = pd.read_csv(r'app\static\tables\smile.csv')

trace_smile= go.Scatter(
    x=smile['Strike'],
    y=smile['IV'],
    showlegend=True,
    name='Волатильность, %',
    marker=dict(color='orange'),
    line={'width':1},
    yaxis='y1')

data = [trace_smile]

layout = go.Layout(title='Улыбка волатильности (Индекс РТС)',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                       orientation='h'),
                   width=config.SPFI_WIDTH,
                   height=config.SPFI_HEIGHT,
                   margin=config.MARGINS)

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\smile.html', auto_open=False, config=config)