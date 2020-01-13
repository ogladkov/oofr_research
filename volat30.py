import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


volat_source = r'app\static\tables\volatility.xlsx'
vol30 = pd.read_excel(volat_source)

trace_vol30_iv = go.Scatter(
    x=vol30['dates'],
    y=vol30['iv30'],
    showlegend=False,
    name='IV, %',
    marker=dict(color='blue'),
    line={'width':1},
    yaxis='y1')

trace_vol30_hv = go.Scatter(
    x=vol30['dates'],
    y=vol30['hv30'],
    showlegend=False,
    name='HV, %',
    marker=dict(color='red'),
    line={'width':1},
    yaxis='y1')

data = [trace_vol30_iv, trace_vol30_hv]

layout = go.Layout(title='График волатильности HV = 30d (Индекс РТС)',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                       orientation='h'),
                   xaxis=dict(tickformat='%m.%y',
                              ),
                   width=config.SPFI_WIDTH,
                   height=config.SPFI_HEIGHT,
                   margin=config.MARGINS)

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\volat30.html', auto_open=False, config=config)