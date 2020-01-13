import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config

pe_epfr = pd.read_csv(r'app\static\tables\funds2.csv', delimiter=';', decimal=',', parse_dates=True, dayfirst=True, index_col=0, encoding='latin1')
pe_epfr.reset_index(inplace=True)
pe_epfr.PRITOK = pe_epfr.PRITOK.replace(' ', '0')
pe_epfr.OTTOK = pe_epfr.OTTOK.replace(' ', '0')
pe_epfr.fillna(0, inplace=True)
pe_epfr[['PRITOK', 'OTTOK']] = pe_epfr[['PRITOK', 'OTTOK']].astype('int')
pe_epfr['EPFR_DATES'] = pd.to_datetime(pe_epfr['EPFR_DATES'], format='%d.%m.%Y')

trace_epfr_income = go.Bar(
    x=pe_epfr['EPFR_DATES'],
    y=pe_epfr['PRITOK']/1000000,
    showlegend=True,
    name='Приток инвестиций, млн долларов США',
    marker=dict(color='orange'),
    yaxis='y1')

trace_epfr_outcome = go.Bar(
    x=pe_epfr['EPFR_DATES'],
    y=pe_epfr['OTTOK']*(-1)/1000000,
    showlegend=True,
    name='Отток инвестиций, млн долларов США',
    marker=dict(color='teal'),
    yaxis='y1')

data = [trace_epfr_income, trace_epfr_outcome]

layout = go.Layout(title='Приток/отток средств иностранных фондов в Россию (EPFR)',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                       orientation='h'
                   ),
                   xaxis=dict(tickformat='%m.%y',
                               dtick="M1",
                              tickfont=dict(size=8),
                               ),
                 width = config.STOCKS_1_WIDTH,
                 height = config.STOCKS_1_HEIGHT,
                 margin = config.MARGINS
                  )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\epfr.html', auto_open=False, config=config)