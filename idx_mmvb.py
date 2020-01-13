import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


idx_mmvb = pd.read_csv(r'app\static\tables\idx_mmvb.csv')

trace_idx_mmvb = go.Scatter(
    x=idx_mmvb['<DATE>'],
    y=idx_mmvb['<CLOSE>'],
    showlegend=False,
    name='Индекс ММВБ',
    marker=dict(color='purple'),
    line={'width':1},
    yaxis='y1')

data = [trace_idx_mmvb]

layout = go.Layout(title='Индекс ММВБ',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   xaxis=dict(tickformat='%m.%y', dtick="M1"),
                   width=config.STOCKS_1_WIDTH,
                   height=config.STOCKS_1_HEIGHT,
                   margin=config.MARGINS
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\idx_mmvb.html', auto_open=False, config=config)