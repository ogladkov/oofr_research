import pandas as pd
import plotly.graph_objs as go
import plotly as py
brent = pd.read_csv(r'app\static\tables\brent.csv')

trace_brent = go.Scatter(
    x=brent['Date'],
    y=brent['Price'],
    showlegend=False,
    name='Нефть, $/баррель',
    marker=dict(color='black'),
    yaxis='y1')

data = [trace_brent]

layout = go.Layout(title='Нефть Brent',
                   xaxis=dict(tickformat='%m.%y', dtick="M1"))

config={'showLink': False}
fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig, filename=r'app\templates\brent.html', auto_open=False, config=config)