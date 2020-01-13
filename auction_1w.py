import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


auction_days = pd.read_csv(r'app\static\tables\dep_auc_1w.csv')

trace_borrowed = go.Scatter(
    x=auction_days['Date'],
    y=auction_days['Borrowed'],
    showlegend=True,
    name='Привлеченные средства, трлн руб.',
    marker=dict(color='orange'),
    yaxis='y1')

trace_offered = go.Scatter(
    x=auction_days['Date'],
    y=auction_days['Offered'],
    showlegend=True,
    name='Предложение Банка России, трлн руб.',
    marker=dict(color='#000',
                opacity=0.1,),
    fill='tozeroy',
    yaxis='y1')

trace_cut = go.Scatter(
    x=auction_days['Date'],
    y=auction_days['Cut Rat'],
    showlegend=True,
    name='Ставка отсечения, %',
    marker=dict(color='red',
                line=dict(width=1)),
    yaxis='y3')

trace_avg = go.Scatter(
    x=auction_days['Date'],
    y=auction_days['Avg Rate'],
    showlegend=True,
    name='Средневзвешенная ставка, %',
    marker=dict(color='blue',
                line=dict(width=1)),
    yaxis='y3')

data = [trace_offered, trace_borrowed, trace_cut, trace_avg]

layout = go.Layout(title='Недельный аукцион ЦБ РФ',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                       orientation='h',
                       font=dict(size=config.LEGEND_FONT_SIZE)
                   ),
                   yaxis1=dict(
                       range=[0,auction_days['Borrowed'].max()*3]
                              ),
                   xaxis1=dict(
                       dtick='M1',
                       tickformat='%m.%y',
                   ),
                   yaxis3=dict(
                       overlaying='y1',
                       side='right',
                   ),
                   width=config.CURRENCY_2_WIDTH,
                   height=config.CURRENCY_2_HEIGHT,
                   margin=config.MARGINS
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\auction_1w.html', auto_open=False, config=config)