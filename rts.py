import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


rts = pd.read_csv(r'app\static\tables\rts.csv')

trace_rts= go.Scatter(
    x=rts['Date'],
    y=rts['Close'],
    showlegend=True,
    name='РТС',
    marker=dict(color='red'),
    line={'width':1},
    yaxis='y2')

trace_rts_vol= go.Scatter(
    x=rts['Date'],
    y=rts['Vol'],
    fill='tozeroy',
    showlegend=True,
    name='Открытый интерес, млрд руб.',
    marker=dict(color='teal'),
    line={'width':1},
    yaxis='y1')

data = [trace_rts, trace_rts_vol]

layout = go.Layout(title='Фьючерс на индекс РТС',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                       orientation='h'
                   ),
                   xaxis=dict(tickformat='%m.%y', dtick="M1"),
                   width=config.SPFI_WIDTH,
                   height=config.SPFI_HEIGHT,
                   margin=config.MARGINS,
                   yaxis1=dict(
                            range=(0, rts['Vol'].max()*3),
                       color='teal'),
                   yaxis2=dict(
                       overlaying='y1',
                       side='right',
                       color='red'))

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\rts.html', auto_open=False, config=config)