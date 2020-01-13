import pandas as pd


table = r'https://smart-lab.ru/q/index_stocks/MICEX10INDEX/'
mmvb_table = pd.read_html(table)[0]
mmvb_table = mmvb_table.iloc[:, [2,3,6,11]]
mmvb_table.columns = mmvb_table.iloc[0]
mmvb_table.set_index('Название', inplace=True)
mmvb_table = mmvb_table[1:]

file_path = r'app\templates\mmvb_table.html'

with open(file_path, 'a', encoding='utf8') as mmvb_table_file:
    mmvb_table_file.truncate(0)
    mmvb_table_file.write('<table class="mmvb_table">\n')
    mmvb_table_file.write('<tr>\n')
    mmvb_table_file.write('    <th>Акции, участвующие в расчете индекса "ММВБ 10"</th>\n')
    for th in mmvb_table.columns:
        mmvb_table_file.write('<th>{}</th>'.format(th))
    mmvb_table_file.write('</tr>\n')
    for tr in mmvb_table.index:
        mmvb_table_file.write('<tr>\n')
        mmvb_table_file.write('<td>{}</td>'.format(tr))
        for td in mmvb_table.loc[tr]:
            mmvb_table_file.write('<td>{}</td>'.format(td))
        mmvb_table_file.write('</tr>\n')
    mmvb_table_file.write('</table>\n')