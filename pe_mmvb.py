import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config

pe_mmvb = pd.read_csv(r'app\static\tables\funds2.csv', delimiter=';', decimal=',', parse_dates=True, dayfirst=True, index_col=0, encoding='latin1')

trace_pe_mmvb_pe = go.Scatter(
    x=pe_mmvb.index,
    y=pe_mmvb['PE_PE'],
    showlegend=True,
    name='P/E',
    marker=dict(color='orange'),
    yaxis='y1')

trace_pe_mmvb_consensus = go.Scatter(
    x=pe_mmvb.index,
    y=pe_mmvb['PE_TARGET'],
    showlegend=True,
    name='P/E consensus',
    marker=dict(color='teal'),
    yaxis='y1')

data = [trace_pe_mmvb_pe, trace_pe_mmvb_consensus]

layout = go.Layout(title='P/E индекса ММВБ-10',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                       orientation='h'
                   ),
                   xaxis=dict(tickformat='%m.%y', dtick="M1"),
                   width=config.STOCKS_2_WIDTH,
                   height=config.STOCKS_2_HEIGHT,
                   margin=config.MARGINS
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\pe_mmvb.html', auto_open=False, config=config)