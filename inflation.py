import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


inflation= pd.read_csv(r'app\static\tables\inflation.csv')

trace_inflation= go.Scatter(x=inflation['Release Date'],
                           y=inflation['Actual'],
                           showlegend=True,
                           name='Инфляция РФ, %',
                           line={'width':1},
                           xaxis='x1',
                           yaxis='y1'
                           )

data = [trace_inflation]

layout = go.Layout(title='Инфляция РФ',
                    font=dict(size=config.LAYOUT_FONT_SIZE),
                    legend=dict(
                                orientation='h'),
                    xaxis=dict(
                            tickformat='%m.%y',
                            dtick='M2',
                            nticks=6),
                    margin=config.MARGINS,
                    width=config.MACRO_WIDTH,
                    height=config.MACRO_HEIGHT
                    )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\inflation.html', auto_open=False, config=config)