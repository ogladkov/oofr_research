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

index_cbr = 'Ключевая ставка ЦБ России'
cbr_rate_file = r'app\static\tables\cbr_rate.csv'
cbr_rate_df = pd.read_csv(cbr_rate_file).set_index(['Release Date']).sort_index()
cbr_rate_df = cbr_rate_df.drop('Unnamed: 0', axis=1)
cbr_rate_df.loc[tod] = cbr_rate_df.iloc[-1]['Actual']
cbr_rate_df.index = pd.to_datetime(cbr_rate_df.index, format='%Y-%m-%d')
cbr_data = [cbr_rate_df[x:]['Actual'][0] for x in terms]

index_fed = 'Учётная ставка ФРС'
fed_file = r'app\static\tables\fed.csv'
fed_df = pd.read_csv(fed_file).set_index(['Release Date']).sort_index()
fed_df = fed_df.drop('Unnamed: 0', axis=1)
fed_df.loc[tod] = fed_df.iloc[-1]['Actual']
fed_df.index = pd.to_datetime(fed_df.index, format='%Y-%m-%d')
fed_data = [fed_df[x:]['Actual'][0] for x in terms]

index_ruonia = 'RUONIA'
ruonia_file = r'app\static\tables\ruonia.csv'
ruonia_df = pd.read_csv(ruonia_file).set_index(['Date']).sort_index()
ruonia_df.loc[tod] = ruonia_df.iloc[-1]['Ruonia']
ruonia_df.index = pd.to_datetime(ruonia_df.index, format='%Y-%m-%d')
ruonia_data = [ruonia_df[x:]['Ruonia'][0] for x in terms]

index_mosprime = 'MosPRIME 3M'
mosprime_file = r'app\static\tables\mosprime.csv'
mosprime_df = pd.read_csv(mosprime_file, parse_dates=[1], dayfirst=False).set_index('date')
mosprime_df.loc[tod] = mosprime_df.iloc[-1]['3m']
mosprime_df = mosprime_df.sort_index()
mosprime_data = [mosprime_df[x:]['3m'][0] for x in terms]
mosprime_data = [x / 100 for x in mosprime_data]

index_usdrub = 'USDRUB'
usdrub_file = r'app\static\tables\usdrub.csv'
usdrub_df = pd.read_csv(usdrub_file, parse_dates=True).set_index('Date')
usdrub_df = usdrub_df.sort_index()
usdrub_data = [usdrub_df[x:]['Price'][0] for x in terms]

index_eurrub = 'EURRUB'
eurrub_file = r'app\static\tables\eurrub.csv'
eurrub_df = pd.read_csv(eurrub_file, parse_dates=True).set_index('Date')
eurrub_df = eurrub_df.sort_index()
eurrub_data = [eurrub_df[x:]['Price'][0] for x in terms]

index_eurusd = 'EURUSD'
eurusd_file = r'app\static\tables\eurusd.csv'
eurusd_df = pd.read_csv(eurusd_file, parse_dates=True).set_index('Date')
eurusd_df = eurusd_df.sort_index()
eurusd_data = [eurusd_df[x:]['Price'][0] for x in terms]

index_bicur = 'Бивалютная корзина'
bicur = pd.concat([eurrub_df['Price'], usdrub_df['Price']], axis=1)
bicur.dropna(inplace=True)
bicur.columns = ['eur', 'usd']
bicur['bicur'] = bicur['usd'] * 0.55 + bicur['eur'] * 0.45
bicur_data = [bicur[x:]['bicur'][0] for x in terms]

index_repo_on = 'РЕПО с ЦК o/n'
repo_on_file = r'app\static\tables\repo_on.csv'
repo_on_df = pd.read_csv(repo_on_file, parse_dates=True).set_index('date')
repo_on_data = [repo_on_df[x:]['close'][0] for x in terms]

index_repo_1w = 'РЕПО с ЦК T+7'
repo_1w_file = r'app\static\tables\repo_1w.csv'
repo_1w_df = pd.read_csv(repo_1w_file, parse_dates=True).set_index('date')
repo_1w_data = [repo_1w_df[x:]['close'][0] for x in terms]

index = [index_cbr, index_fed, index_ruonia, index_repo_on, \
                    index_repo_1w, index_mosprime, index_usdrub, index_eurrub, \
                    index_eurusd, index_bicur]

df_table = pd.DataFrame([cbr_data, fed_data, ruonia_data, repo_on_data, repo_1w_data, \
                        mosprime_data, usdrub_data, eurrub_data, eurusd_data, \
                        bicur_data],
             columns=terms,
             index=index)

df_table.loc['USDRUB'] = df_table.loc['USDRUB'].round(4)
df_table.loc['EURRUB'] = df_table.loc['EURRUB'].round(4)
df_table.loc['EURUSD'] = df_table.loc['EURUSD'].round(4)
df_table.loc['Бивалютная корзина'] = df_table.loc['Бивалютная корзина'].round(4)


file_path = r'app\templates\curr_table.html'

with open(file_path, 'a', encoding='utf8') as curr_table_file:
    curr_table_file.truncate(0)
    curr_table_file.write('<table class="curr_table">\n')
    curr_table_file.write('<tr>\n')
    curr_table_file.write('    <th>&nbsp;</th>\n')
    for th in terms:
        curr_table_file.write('    <th>' + th.split('-')[2] + '.' + th.split('-')[1] + '.' + th.split('-')[0] + '</th>\n')
    curr_table_file.write('</tr>\n')
    for tr in index:
        curr_table_file.write('<tr>\n')
        curr_table_file.write('    <td>' + tr + '</td>\n')
        for td in df_table.loc[tr]:
            curr_table_file.write('    <td>' + str(td) + '</td>\n')
        curr_table_file.write('</tr>\n')
    curr_table_file.write('</table>\n')