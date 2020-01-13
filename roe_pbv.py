import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


greb_shares_link = r'app\static\tables\greb_shares.xlsx'
df = pd.read_excel(greb_shares_link, sheet_name='For use eq')

trace_df = go.Scatter(x=df['ROE, %'],
                     y=df['P/BV'],
                     mode='markers+text',
                     marker=dict(color='teal',
                                 size=12
                                 ),
                     showlegend=False,
                     name='ROE / P:BV',
                     text=df.iloc[:, 0],
                     textposition='top center',
                     xaxis='x1',
                     yaxis='y1'
                     )

data = [trace_df]

layout = go.Layout(title='Диаграмма стоимости: ROE / P:BV',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                            orientation='h'
                   ),
                   margin=config.MARGINS,
                   width=config.STOCKS_2_WIDTH_1,
                   height=config.STOCKS_2_HEIGHT,
                   xaxis=dict(title='ROE, %',
                              range=[df['ROE, %'].min()-0.05, df['ROE, %'].max()+0.1]),
                   yaxis=dict(title='P/BV')
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\roe_pbv.html', auto_open=False, config=config)