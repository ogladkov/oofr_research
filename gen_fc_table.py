import pandas as pd
import numpy as np


greb_shares_link = r'app\static\tables\greb_shares.xlsx'
df = pd.read_excel(greb_shares_link, sheet_name='For use eq')
df = df.loc[:, :'Ожидаемая див. доходность, %']
df[['ROE, %', 'Потенциал', 'Ожидаемая див. доходность, %']] = df[['ROE, %', 'Потенциал', 'Ожидаемая див. доходность, %']] * 100
df[['ROE, %', 'Потенциал', 'Ожидаемая див. доходность, %']] = df[['ROE, %', 'Потенциал', 'Ожидаемая див. доходность, %']].round(2)
df = df.replace(np.nan, '')
print(df)

file_path = r'C:\Users\RNCB\PycharmProjects\oofr_research\app\templates\fc.html'
with open(file_path, 'a', encoding='UTF-8') as fc_table_file:
    fc_table_file.truncate(0)
    fc_table_file.write('<table class="fc_table">\n')
    fc_table_file.write('<tr>\n')
    for th in df.columns:
        fc_table_file.write('    <th>' + th + '</th>\n')
    fc_table_file.write('</tr>\n')
    for tr in df.index:
        fc_table_file.write('<tr>\n')
        for td in df.loc[tr]:
            fc_table_file.write('    <td>' + str(td) + '</td>\n')
        fc_table_file.write('</tr>\n')
    fc_table_file.write('</table>\n')