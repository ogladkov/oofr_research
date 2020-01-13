import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


trade_balance= pd.read_csv(r'app\static\tables\tb.csv')

trace_trade_balance = go.Scatter(x=trade_balance['dates'],
                               y=trade_balance['fact'],
                                 marker=dict(color='darkkhaki'),
                               showlegend=True,
                               name='Торговый баланс, млрд долларов',
                               line={'width':1},
                               xaxis='x1',
                               yaxis='y1'
                               )

data = [trace_trade_balance]

layout = go.Layout(title='Сальдо торгового баланса РФ',
                font=dict(size=config.LAYOUT_FONT_SIZE),
                           legend=dict(
                               orientation='h'
                           ),
                autosize=False,
                xaxis=dict(
                   tickformat='%m.%y',
                   dtick='M2',
                   nticks=6),
                margin=config.MARGINS,
                width=config.MACRO_WIDTH,
                height=config.MACRO_HEIGHT
                )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\trade_balance.html', auto_open=False, config=config)