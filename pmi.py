import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


pmi = pd.read_csv(r'app\static\tables\pmi.csv')

trace_pmi = go.Scatter(x=pmi['Release Date'],
                     y=pmi['Actual'],
                     marker=dict(color='red'),
                     showlegend=False,
                     name='PMI',
                     line={'width':1},
                     xaxis='x1',
                     yaxis='y1'
                     )

trace_pmi_line = go.Scatter(x=pmi['Release Date'],
                          y=[50 for x in pmi['Release Date']],
                          showlegend=False,
                          yaxis='y1')

data = [trace_pmi, trace_pmi_line]

layout = go.Layout(title='Динамика индекса PMI manufacturing Russia',
                    font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                            orientation='h'
                   ),
                   xaxis=dict(
                       tickformat='%m.%y',
                       dtick='M1'
                   ),
                   yaxis2=dict(
                       overlaying='y1'),
                   margin=config.MARGINS,
                   width=config.MACRO_WIDTH,
                   height=config.MACRO_HEIGHT
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\pmi.html', auto_open=False, config=config)