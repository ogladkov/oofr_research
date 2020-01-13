import pandas as pd
import datetime as dt


now_month = int(dt.datetime.now().strftime(format='%m'))

if now_month == 1 or now_month == 4 or now_month == 7 or now_month == 10:
    diff_month = 0
elif now_month == 5 or now_month == 6 or now_month == 7 or now_month == 8:
    diff_month = 1
elif now_month == 9 or now_month == 10 or now_month == 11 or now_month == 12:
    diff_month = 2

tod = (dt.datetime.now() - dt.timedelta(days=1)).strftime(format='%Y-%m-%d')
tod_14 = (dt.datetime.now() - dt.timedelta(days=15)).strftime(format='%Y-%m-%d')
q1 = str((dt.datetime.now() - dt.timedelta(days=91)).strftime(format='%Y-%m')) + '-01'
q2 = str((dt.datetime.now() - dt.timedelta(days=181)).strftime(format='%Y-%m')) + '-01'
q3 = str((dt.datetime.now() - dt.timedelta(days=271)).strftime(format='%Y-%m')) + '-01'
q4 = str((dt.datetime.now() - dt.timedelta(days=361)).strftime(format='%Y-%m')) + '-01'
q5 = str((dt.datetime.now() - dt.timedelta(days=451)).strftime(format='%Y-%m')) + '-01'

terms = [q5, q4, q3, q2, q1, tod_14, tod]

index_mmvb = 'ММВБ'
mmvb_file = r'C:\Users\RNCB\PycharmProjects\oofr_research\app\static\tables\idx_mmvb.csv'
mmvb_df = pd.read_csv(mmvb_file).set_index(['<DATE>']).sort_index()
mmvb_df = mmvb_df.drop('Unnamed: 0', axis=1)
mmvb_df.loc[tod] = mmvb_df.iloc[-1]['<CLOSE>']
mmvb_df.index = pd.to_datetime(mmvb_df.index, format='%Y-%m-%d')
mmvb_df = [mmvb_df[x:]['<CLOSE>'][0] for x in terms]

index_rts = 'РТС'
rts_file = r'C:\Users\RNCB\PycharmProjects\oofr_research\app\static\tables\rts.csv'
rts_df = pd.read_csv(rts_file).set_index(['Date']).sort_index()
rts_df = rts_df.drop('Unnamed: 0', axis=1)
rts_df.loc[tod] = rts_df.iloc[-1]['Close']
rts_df.index = pd.to_datetime(rts_df.index, format='%Y-%m-%d')
rts_df = [rts_df[x:]['Close'][0]/100 for x in terms]

index_rvi = 'RVI'
rvi_file = r'C:\Users\RNCB\PycharmProjects\oofr_research\app\static\tables\rvi.csv'
rvi_df = pd.read_csv(rvi_file).set_index(['Date']).sort_index()
rvi_df = rvi_df.drop('Unnamed: 0', axis=1)
rvi_df.loc[tod] = rvi_df.iloc[-1]['Close']
rvi_df.index = pd.to_datetime(rvi_df.index, format='%Y-%m-%d')
rvi_df = [rvi_df[x:]['Close'][0] for x in terms]

index_sp = 'S&P500(SPX)'
sp_file = r'C:\Users\RNCB\PycharmProjects\oofr_research\app\static\tables\sp.csv'
sp_df = pd.read_csv(sp_file).set_index(['Date']).sort_index()
sp_df = sp_df.drop('Unnamed: 0', axis=1)
sp_df.loc[tod] = sp_df.iloc[-1]['Price']
sp_df.index = pd.to_datetime(sp_df.index, format='%Y-%m-%d')
sp_df = [sp_df[x:]['Price'][0] for x in terms]

index_djia = 'DJIA'
djia_file = r'C:\Users\RNCB\PycharmProjects\oofr_research\app\static\tables\djia.csv'
djia_df = pd.read_csv(djia_file).set_index(['Date']).sort_index()
djia_df = djia_df.drop('Unnamed: 0', axis=1)
djia_df.loc[tod] = djia_df.iloc[-1]['Price']
djia_df.index = pd.to_datetime(djia_df.index, format='%Y-%m-%d')
djia_df = [djia_df[x:]['Price'][0] for x in terms]

index_dax = 'DAX'
dax_file = r'C:\Users\RNCB\PycharmProjects\oofr_research\app\static\tables\dax.csv'
dax_df = pd.read_csv(dax_file).set_index(['Date']).sort_index()
dax_df = dax_df.drop('Unnamed: 0', axis=1)
dax_df.loc[tod] = dax_df.iloc[-1]['Price']
dax_df.index = pd.to_datetime(dax_df.index, format='%Y-%m-%d')
dax_df = [dax_df[x:]['Price'][0] for x in terms]

index_vix = 'VIX'
vix_file = r'C:\Users\RNCB\PycharmProjects\oofr_research\app\static\tables\vix.csv'
vix_df = pd.read_csv(vix_file).set_index(['Date']).sort_index()
vix_df = vix_df.drop('Unnamed: 0', axis=1)
vix_df.loc[tod] = vix_df.iloc[-1]['Price']
vix_df.index = pd.to_datetime(vix_df.index, format='%Y-%m-%d')
vix_df = [vix_df[x:]['Price'][0] for x in terms]

index = [index_mmvb, index_rts, index_sp, index_djia, index_dax, index_rvi, index_vix]

df_table = pd.DataFrame([mmvb_df, rts_df, sp_df, djia_df, dax_df, rvi_df, vix_df],
           columns=terms,
           index=index)

file_path = r'app\templates\stocks_table.html'

with open(file_path, 'a', encoding='utf8') as stocks_table_file:
    stocks_table_file.truncate(0)
    stocks_table_file.write('<table class="stocks_table">\n')
    stocks_table_file.write('<tr>\n')
    stocks_table_file.write('    <th>&nbsp;</th>\n')
    for th in terms:
        stocks_table_file.write('    <th>' + th.split('-')[2] + '.' + th.split('-')[1] + '.' + th.split('-')[0] + '</th>\n')
    stocks_table_file.write('</tr>\n')
    for tr in index:
        stocks_table_file.write('<tr>\n')
        stocks_table_file.write('    <td>' + tr + '</td>\n')
        for td in df_table.loc[tr]:
            stocks_table_file.write('    <td>' + str(td) + '</td>\n')
        stocks_table_file.write('</tr>\n')
    stocks_table_file.write('</table>\n')