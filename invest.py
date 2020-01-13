import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config

invests_source = r'app\static\tables\invest.csv'
invests = pd.read_csv(invests_source, sep=';')

trace_invests = go.Bar(x=invests['INV_DATES'],
                     y=invests['INVESTMENTS']/1000,
                     marker=dict(color='teal'),
                     showlegend=True,
                     opacity=0.4,
                     name='Инвестиции, млрд руб.',
                     xaxis='x1',
                     yaxis='y1'
                     )

data = [trace_invests]

layout = go.Layout(title='Инвестиции в основной капитал РФ',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                       orientation='h'
                   ),
                   xaxis1=dict(
                       dtick='M2',
                       tickformat='%m.%y',
                       tickfont=dict(size=8),
                       nticks=6
                   ),
                   yaxis1=dict(
                       range=(0, invests['INVESTMENTS'].max()/1000 * 1.5)),
                   margin=config.MARGINS,
                   width=config.MACRO_WIDTH,
                   height=config.MACRO_HEIGHT
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\invests.html', auto_open=False, config=config)