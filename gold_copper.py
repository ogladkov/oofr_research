import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


df_gold_copper = pd.read_csv(r'app\static\tables\gold_copper.csv', index_col=0,
                             dayfirst=True)
df_tnx = pd.read_csv(r'app\static\tables\tnx.csv', index_col=0, dayfirst=True)
df_tnx = df_tnx[df_tnx['Date'] >= df_gold_copper.iloc[0]['datetime']]

def make_plot():
    trace_tnx = go.Scatter(x=df_tnx.Date,
                           y=df_tnx.Price,
                           name='10-Year US Treasure Bonds',
                           line={'width': 1},
                           yaxis='y'
                          )
    trace_gold_copper = go.Scatter(x=df_gold_copper.datetime,
                          y=df_gold_copper.ratio,
                          name='Copper / Gold',
                          yaxis='y2',
                          line = {'width': 1},
                         )
    layout = go.Layout(
                       legend=dict(
                                  orientation='h'
                                  ),
                       yaxis=dict(
                                  side='right',
                                  tickfont=dict(color='blue'),
                                 ),
                       yaxis2=dict(
                                   overlaying='y',
                                   side='left',
                                   tickfont=dict(color='orange'),
                                  )
                      )
    data = [trace_tnx, trace_gold_copper]
    layout['width'] = config.DEBTS_WIDTH
    layout['height'] = config.DEBTS_HEIGHT
    layout['title'] = 'Gold / Copper / US10Y'
    layout['margin'] = config.MARGINS
    fig = dict(data=data, layout=layout)
    return fig, data

fig, data = make_plot()

config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\gold_copper.html', auto_open=False, config=config)