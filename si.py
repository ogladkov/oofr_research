import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


si = pd.read_csv(r'app\static\tables\si.csv')

trace_si= go.Scatter(
    x=si['Date'],
    y=si['Close'],
    showlegend=True,
    name='Si',
    marker=dict(color='green'),
    line={'width':1},
    yaxis='y1')

trace_si_vol= go.Scatter(
    x=si['Date'],
    y=si['Vol'],
    fill='tozeroy',
    showlegend=True,
    name='Открытый интерес, млрд руб.',
    marker=dict(color='teal'),
    line={'width':1},
    yaxis='y2')

data = [trace_si, trace_si_vol]

layout = go.Layout(title='Фьючерс на курс USD/RUB',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                       orientation='h'
                   ),
                   xaxis=dict(tickformat='%m.%y', dtick="M1"),
                   yaxis1=dict(
                        side='right',
                        color='green'),
                   yaxis2=dict(
                       overlaying='y1',
                       side='left',
                       range=(0, si['Vol'].max()*3),
                       color='teal'),
                   width=config.SPFI_WIDTH,
                   height=config.SPFI_HEIGHT,
                   margin=config.MARGINS)

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\si.html', auto_open=False, config=config)