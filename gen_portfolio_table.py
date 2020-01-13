import pandas as pd
import datetime as dt


greb_shares_link = r'app\static\tables\greb_shares.xlsx'
df = pd.read_excel(greb_shares_link, sheet_name='For use b')
df = df.iloc[:, :-1]
df['Доходность, %'] = (df['Доходность, %'] * 100).round(2)
# df['ROE, %'] = (df['ROE, %'] * 100).round(2)
# df['Цена текущая'] = df['Цена текущая'].round(2)
df['Дата оферты'] = df['Дата оферты'].dt.strftime('%d.%m.%Y')
# df['Дата оферты'] = df['Дата оферты'].astype('str')
print(df.columns)

file_path = r'app\templates\portfolio_table.html'

with open(file_path, 'a', encoding='UTF-8') as portfolio_table_file:
    portfolio_table_file.truncate(0)
    portfolio_table_file.write('<table class="portfolio_table">\n')
    portfolio_table_file.write('<tr>\n')
    for th in df.columns:
        portfolio_table_file.write('    <th>' + th + '</th>\n')
    portfolio_table_file.write('</tr>\n')
    for tr in df.index:
        portfolio_table_file.write('<tr>\n')
        for td in df.loc[tr]:
            portfolio_table_file.write('    <td>' + str(td) + '</td>\n')
        portfolio_table_file.write('</tr>\n')
    portfolio_table_file.write('</table>\n')