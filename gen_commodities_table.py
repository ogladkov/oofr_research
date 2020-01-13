import datetime as dt
import pandas as pd


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
index = ['CRB Jefferies', 'Brent, $/bbl', 'Gold, $/ounce', 'Silver, $/ounce']

crb_file = r'app\static\tables\crb.csv'
brent_file = r'app\static\tables\brent.csv'
gold_file = r'app\static\tables\gold.csv'
silver_file = r'app\static\tables\silver.csv'
crb_data = [pd.read_csv(crb_file).set_index(['Date']).sort_index()[x:]['Price'][0] for x in terms]
brent_data = [pd.read_csv(brent_file).set_index(['Date']).sort_index()[x:]['Price'][0] for x in terms]
gold_data = [pd.read_csv(gold_file).set_index(['Date']).sort_index()[x:]['Price'][0] for x in terms]
silver_data = [pd.read_csv(silver_file).set_index(['Date']).sort_index()[x:]['Price'][0] for x in terms]

df_table = pd.DataFrame([crb_data, brent_data, gold_data, silver_data],
             columns=terms,
             index=['CRB Jefferies', 'Brent, $/bbl', 'Gold, $/ounce', 'Silver, $/ounce'])

file_path = r'app\templates\commod_table.html'

with open(file_path, 'a') as commod_table_file:
    commod_table_file.truncate(0)
    commod_table_file.write('<table class="commod_table">\n')
    commod_table_file.write('<tr>\n')
    commod_table_file.write('    <th>&nbsp;</th>\n')
    for th in terms:
        commod_table_file.write('    <th>' + th.split('-')[2] + '.' + th.split('-')[1] + '.' + th.split('-')[0] + '</th>\n')
    commod_table_file.write('</tr>\n')
    for tr in index:
        commod_table_file.write('<tr>\n')
        commod_table_file.write('    <td>' + tr + '</td>\n')
        for td in df_table.loc[tr]:
            commod_table_file.write('    <td>' + str(td) + '</td>\n')
        commod_table_file.write('</tr>\n')
    commod_table_file.write('</table>\n')