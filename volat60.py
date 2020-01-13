import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


volat_source = r'app\static\tables\volatility.xlsx'
vol60 = pd.read_excel(volat_source)

trace_vol60_iv = go.Scatter(
    x=vol60['dates'],
    y=vol60['iv60'],
    showlegend=False,
    name='IV, %',
    marker=dict(color='darkkhaki'),
    yaxis='y1')

trace_vol60_hv = go.Scatter(
    x=vol60['dates'],
    y=vol60['hv60'],
    showlegend=False,
    name='HV, %',
    marker=dict(color='red'),
    yaxis='y1')

data = [trace_vol60_iv, trace_vol60_hv]

layout = go.Layout(title='График волатильности HV = 60d (Индекс РТС)',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                       orientation='h'),
                   xaxis=dict(tickformat='%m.%y',
                              # dtick="M1"
                              ),
                   width=config.SPFI_WIDTH,
                   height=config.SPFI_HEIGHT,
                   margin=config.MARGINS)

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\volat60.html', auto_open=False, config=config)