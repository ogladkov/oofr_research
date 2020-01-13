import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


df_sp = pd.read_csv(r'app\static\tables\sp.csv', index_col=0, dayfirst=True)
df_div = pd.read_csv(r'app\static\tables\div_sp.csv', index_col=0, dayfirst=True)
# df_mmvb = pd.read_csv(r'app\static\tables\mcx10.csv', index_col=0, dayfirst=True)
df_fed3m = pd.read_csv(r'app\static\tables\fed3m.csv', index_col=0, dayfirst=True)
df_fed3m = df_fed3m[df_fed3m['Date'] > '2008']
df_tnx = pd.read_csv(r'app\static\tables\tnx.csv', index_col=0, dayfirst=True)
df_tnx = df_tnx [df_tnx ['Date'] > '2008']

def make_plot():
    trace_tnx = go.Scatter(x=df_tnx.Date,
                           y=df_tnx.Price,
                           name='10-Year US Treasure Bonds',
                           line={'width': 1},
                           yaxis='y'
                          )
    trace_sp = go.Scatter(x=df_sp.Date,
                          y=df_sp.Price,
                          name='S&P(500)',
                          line={'width': 1},
                          yaxis='y2'
                         )
    trace_div = go.Scatter(x=df_div['Date'],
                          y=df_div['Yield Value'],
                          name='S&P(500) Div Yield',
                           line={'width': 1},
                          yaxis='y'
                         )
    trace_fed3m = go.Scatter(x=df_fed3m['Date'],
                           y=df_fed3m['3 mo'],
                           name='FED 3M',
                             line={'width': 1},
                           yaxis='y'
                           )
    # trace_mmvb = go.Scatter(x=df_mmvb.Date,
    #                           y=df_mmvb.Price,
    #                           name='ММВБ',
    #                           yaxis='y2'
    #                          )
    # trace_ofz10 = go.Scatter(x=df_ofz10.Date,
    #                           y=df_ofz10.Price,
    #                           name='ОФЗ 10 лет',
    #                           yaxis='y'
    #                          )
    # trace_mibor = go.Scatter(x=df_mibor.Date,
    #                           y=df_mibor.Price,
    #                           name='MIBOR',
    #                           yaxis='y'
    #                          )
    layout = go.Layout(
                       legend=dict(
                                  orientation='h'
                                  ),
                       yaxis=dict(
                                  side='left',
                                  tickfont=dict(color='red'),
                                 ),
                       yaxis2=dict(
                                   overlaying='y',
                                   side='right'
                                  )
                      )
    data = [trace_tnx, trace_div, trace_sp, trace_fed3m]
    layout['width'] = config.DEBTS_WIDTH
    layout['height'] = config.DEBTS_HEIGHT
    layout['title'] = 'US Equities and Rates'
    layout['margin'] = config.MARGINS
    fig = dict(data=data, layout=layout)
    return fig, data

fig, data = make_plot()

# trace_gspread = go.Scatter(
#     x=gspread['Date'],
#     y=gspread['spread'],
#     showlegend=False,
#     name='Spread Russia-28 / USA10Y, б/п',
#     marker=dict(color='darkkhaki'),
#     fill='tozeroy',
#     yaxis='y1')
#
# data = [trace_gspread]
#
# layout = go.Layout(title='Spread Russia-28 / USA10Y, б/п',
#                    font=dict(size=config.LAYOUT_FONT_SIZE),
#                    legend=dict(
#                        orientation='h'
#                    ),
#                    xaxis=dict(tickformat='%m.%y', dtick="M1"),
#                    width=config.DEBTS_WIDTH,
#                    height=config.DEBTS_HEIGHT,
#                    margin=config.MARGINS,
#                    yaxis=dict(
#                               range=[gspread['spread'].min()/2, gspread['spread'].max()*1.5, ]
#                              )
#                    )

# fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\debt_comp.html', auto_open=False, config=config)