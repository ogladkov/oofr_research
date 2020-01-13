import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


gspread = pd.read_csv(r'app\static\tables\spread.csv')
gspread['Date'] = pd.to_datetime(gspread['Date'], format='%Y-%m-%d')

trace_gspread = go.Scatter(
    x=gspread['Date'],
    y=gspread['spread'],
    showlegend=False,
    name='Spread Russia-28 / US10Y, б.п.',
    marker=dict(color='darkkhaki'),
    fill='tozeroy',
    line={'width':1},
    yaxis='y1')

data = [trace_gspread]

layout = go.Layout(title='Spread Russia-28 / USA10Y, б.п.',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                       orientation='h'
                   ),
                   xaxis=dict(tickformat='%m.%y', dtick="M1"),
                   width=config.DEBTS_WIDTH,
                   height=config.DEBTS_HEIGHT,
                   margin=config.MARGINS,
                   yaxis=dict(
                              range=[gspread['spread'].min()/2, gspread['spread'].max()*1.5, ]
                             )
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\gspread.html', auto_open=False, config=config)