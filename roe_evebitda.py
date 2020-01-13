import pandas as pd
import plotly.graph_objs as go
import plotly as py
import config


greb_shares_link = r'app\static\tables\greb_shares.xlsx'
df = pd.read_excel(greb_shares_link, sheet_name='For use eq')

trace_df = go.Scatter(x=df['ROE, %'],
                     y=df['EV/EBITDA(EBIT)'],
                     mode='markers+text',
                     marker=dict(color='orange',
                                 size=12
                                 ),
                     showlegend=False,
                     name='ROE / EV:EBITDA',
                     text=df.iloc[:, 0],
                     textposition='top center',
                     xaxis='x1',
                     yaxis='y1'
                     )

data = [trace_df]

layout = go.Layout(title='Диаграмма стоимости: ROE / EV:EBITDA',
                   font=dict(size=config.LAYOUT_FONT_SIZE),
                   legend=dict(
                            orientation='h'
                   ),
                   yaxis=dict(
                       range=[0, df['EV/EBITDA(EBIT)'].max()+2],
                       title='EV/EBITDA'),
                   margin=config.MARGINS,
                   width=config.STOCKS_2_WIDTH_2,
                   height=config.STOCKS_2_HEIGHT,
                   xaxis=dict(title='ROE, %')
                   )

fig = go.Figure(data=data, layout=layout)
config={'showLink': False}
py.offline.plot(fig, filename=r'app\templates\roe_evebitda.html', auto_open=False, config=config)