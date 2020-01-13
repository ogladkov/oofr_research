import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


m2 = pd.read_csv(r'app\static\tables\m2.csv')
m2 = m2.iloc[-12:]
rests = pd.read_csv(r'app\static\tables\rests.csv')

trace_m2 = go.Scatter(x=m2['datetime'],
                    y=m2['m2']/1000,
                    marker=dict(color='orange'),
                    showlegend=True,
                    name='M2, трлн руб.',
                    line={'width':1},
                    yaxis='y1')

trace_m0 = go.Scatter(x=m2['datetime'],
                    y=m2['m0']/1000,
                    marker=dict(color='purple'),
                    showlegend=True,
                    name='M0, трлн руб.',
                    line={'width':1},
                    yaxis='y2')

trace_rests = go.Scatter(x=rests['Date'],
                    y=rests['Rests']/1000,
                    fill='tozeroy',
                    marker=dict(color='seagreen',
                                opacity=0.25),
                    showlegend=True,
                    name='Остатки на корр. счетах, трлн руб.',
                    line={'width':1},
                    yaxis='y3')

data = [trace_m2, trace_m0, trace_rests]

layout = go.Layout(title='Динамика М0, М2 и остатков на корр. счетах в ЦБ РФ',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   autosize=False,
                   margin=config.MARGINS,
                   legend=dict(
                       orientation='h'
                   ),
                   xaxis=dict(
                       tickformat='%m.%y',
                       dtick='M2'
                   ),
                   yaxis1=dict(
                        tickfont=dict(
                                color='orange'
                                )),
                   yaxis2=dict(
                        tickfont=dict(
                                color='purple'
                                ),
                       overlaying='y1',
                       side='right'
                   ),
                   yaxis3=dict(
                       range=(0, rests['Rests'].max()/1000*2.5),
                        tickfont=dict(
                                    color='seagreen'
                                ),
                       overlaying='y1',
                       side='left',
                       position=0.04
                   ),
                   width=config.MACRO_WIDTH,
                   height=config.MACRO_HEIGHT
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\mm.html', auto_open=False, config=config)