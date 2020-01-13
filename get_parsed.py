import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.select import Select
import datetime as dt
import time
import os
import numpy as np


tod = str(dt.datetime.now().strftime(format='%m/%d/%Y'))
yr_before = str((dt.datetime.now() - dt.timedelta(days=365)).strftime(format='%m/%d/%Y'))

### Макроэкономика
## Динамика М0, М2 и остатков на корр. счетах ЦБ РФ
# Индикатор денежной массы М2 по данным Банка России (12 мес.)
def m2():
    url_m0 = r'http://cbr.ru/vfs/statistics/ms/mb_bd.xlsx'
    url_m2 = r'http://cbr.ru/vfs/statistics/credit_statistics/M2-M2_SA.xlsx'
    m0 = pd.read_excel(url_m0, header=4).iloc[1:, 0:1]
    m2 = pd.read_excel(url_m2, header=1).iloc[:, :2]
    m0.dropna(inplace=True)
    m0.reset_index(inplace=True)
    m0.columns = ['datetime', 'm0']
    m0['datetime'] = pd.to_datetime(m0['datetime'], format='%Y-%m-%d')
    m2['Date'] = pd.to_datetime(m2['Date'], format='%Y-%m-%d')
    m2.columns = ['datetime', 'm2']
    m0m2 = m0.merge(m2, on='datetime')
    m0m2.to_csv(r'app\static\tables\m2.csv')

def rests():
    yesterday = (dt.datetime.now() - dt.timedelta(days=365)).strftime(format='%d.%m.%Y')

    url_rests = 'http://www.cbr.ru/hd_base/ostat_base/'
    driver = webdriver.Firefox()
    driver.get(url_rests)
    driver.find_element_by_id('UniDbQuery_FromDate').clear()
    driver.find_element_by_id('UniDbQuery_FromDate').send_keys(yesterday)
    driver.find_element_by_id('UniDbQuery_ToDate').click()
    driver.find_element_by_id('UniDbQuery_searchbutton').click()
    html = driver.page_source
    driver.close()

    df_rests = pd.read_html(html)[0]
    df_rests.columns = ['Date', 'Rests', '']
    df_rests = df_rests[1:].iloc[:, 0:2]
    df_rests['Rests'] = df_rests['Rests'].str.replace(' ', '').str.replace(',', '.').astype('float')
    df_rests['Date'] = pd.to_datetime(df_rests['Date'], format='%d.%m.%Y')

    df_rests.to_csv(r'app\static\tables\rests.csv')


# Инфляция
def inflation():
    # infl_url = r'https://www.statbureau.org/en/russia/cpi/index.data.csv'
    # infl = pd.read_csv(infl_url)
    # infl = pd.melt(infl, id_vars='Year')
    # infl.variable = infl.variable.str.strip()
    # infl['Dates'] = infl['Year'].astype('str') + infl['variable']
    # infl.datetime = pd.to_datetime(infl.Dates, format='%Y%B')
    # infl.drop(['Year', 'variable'], axis=1, inplace=True)
    # infl.set_index('Dates', inplace=True)
    # infl.index = pd.to_datetime(infl.index, format='%Y%B')
    # infl = infl.sort_index().dropna().iloc[-12:]
    # infl.columns = ['Inflation']
    # infl.Inflation = infl.Inflation - 100
    # infl.Inflation = infl.Inflation.cumsum()

    inflation_url = r'https://www.investing.com/economic-calendar/russian-cpi-1180'
    driver = webdriver.Firefox()
    driver.get(inflation_url)
    driver.find_element_by_css_selector('#showMoreHistory1180').click()
    time.sleep(1)
    driver.find_element_by_css_selector('#showMoreHistory1180').click()
    time.sleep(1)
    html = driver.page_source
    driver.close()
    df = pd.read_html(html)[0]
    df = df.iloc[:12, [0, 2]]
    df.dropna(inplace=True)
    df['Release Date'] = pd.to_datetime(df['Release Date'].str[:12], format='%b %d, %Y')

    df.to_csv(r'app\static\tables\inflation.csv')


# Торговый баланс
def trade_balance():
    url = r'https://ru.investing.com/economic-calendar/russian-trade-balance-550'
    driver = webdriver.Firefox()
    driver.get(url)
    driver.find_element_by_id("showMoreHistory550").click()

    tb = pd.read_html(driver.page_source)[0]
    driver.close()
    tb = tb.drop(['Время', 'Unnamed: 5'], axis=1)
    tb.columns = ['dates', 'fact', 'forecast', 'prev']
    tb['dates'] = tb['dates'].str.split(' ').str[0]
    tb['dates'] = pd.to_datetime(tb.dates, format='%d.%m.%Y')
    tb['fact'] = tb['fact'].str.replace('B', '').str.replace(',', '.').astype('float32')
    tb.dropna(inplace=True)
    tb.reset_index(inplace=True)
    tb.to_csv(r'app\static\tables\tb.csv')

# PMI
def pmi():
    # source_pmi = r'http://www.ereport.ru/stat.php?razdel=indicat&table=rupmi&time=1'
    # df_pmi = pd.read_html(source_pmi)[0]
    # df_pmi = df_pmi.reset_index()
    # df_pmi = df_pmi.drop('index', axis=1)
    # df_pmi = df_pmi.drop(0)
    # df_pmi.columns = ['Dates', 'PMI']
    # pmi_dates = df_pmi['Dates'].str.split('-', expand=True)
    # df_pmi['Dates'] = pmi_dates.iloc[:, 1] + '-' + pmi_dates.iloc[:, 0] + '-01'
    # df_pmi['Dates'] = pd.to_datetime(df_pmi['Dates'])
    # df_pmi.set_index('Dates', inplace=True)
    # df_pmi['PMI'] = df_pmi['PMI'].astype('float')
    # df_pmi = df_pmi.iloc[-24:]
    # df_pmi.reset_index(inplace=True)
    try:
        pmi_url = r'https://www.investing.com/economic-calendar/russian-markit-manufacturing-pmi-1630'
        driver = webdriver.Firefox()
        driver.get(pmi_url)
        driver.find_element_by_css_selector('#showMoreHistory1630').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#showMoreHistory1630').click()
        time.sleep(1)
        html = driver.page_source
        driver.close()
        df = pd.read_html(html)[0]
        df = df.iloc[:, [0, 2]]
        df.dropna(inplace=True)
        df['Release Date'] = pd.to_datetime(df['Release Date'].str[:12], format='%b %d, %Y')
    except:
        driver.close()
        pmi()

    df.to_csv(r'app\static\tables\pmi.csv')


# Товарный рынок
def metals():
    try:
        url_gold = r'https://www.investing.com/commodities/gold-historical-data'
        url_silver = r'https://www.investing.com/commodities/silver-historical-data'

        driver = webdriver.Firefox()
        driver.get(url_gold)
        driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
        driver.find_element_by_css_selector('#startDate').click()
        driver.find_element_by_css_selector('#startDate').clear()
        driver.find_element_by_css_selector('#startDate').send_keys(yr_before)
        driver.find_element_by_css_selector('#endDate').click()
        driver.find_element_by_css_selector('#endDate').clear()
        driver.find_element_by_css_selector('#endDate').send_keys(tod)
        driver.find_element_by_css_selector('#applyBtn').click()
        time.sleep(1)
        df_gold = pd.DataFrame(pd.read_html(driver.page_source)[0])
        driver.close()

        df_gold = df_gold[['Date', 'Price']]
        df_gold['Date'] = pd.to_datetime(df_gold['Date'], format='%b %d, %Y')
        df_gold['Price'] = df_gold['Price'].replace(',', '')
        df_gold['Price'] = df_gold['Price'].astype('float32')
        df_gold.to_csv(r'app\static\tables\gold.csv')

        driver = webdriver.Firefox()
        driver.get(url_silver)
        driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
        driver.find_element_by_css_selector('#startDate').click()
        driver.find_element_by_css_selector('#startDate').clear()
        driver.find_element_by_css_selector('#startDate').send_keys(yr_before)
        driver.find_element_by_css_selector('#endDate').click()
        driver.find_element_by_css_selector('#endDate').clear()
        driver.find_element_by_css_selector('#endDate').send_keys(tod)
        driver.find_element_by_css_selector('#applyBtn').click()
        time.sleep(1)
        df_silver = pd.DataFrame(pd.read_html(driver.page_source)[0])
        driver.close()

        df_silver = df_silver[['Date', 'Price']]
        df_silver['Date'] = pd.to_datetime(df_silver['Date'], format='%b %d, %Y')
        df_silver['Price'] = df_silver['Price'].astype('float32')
        df_silver.to_csv(r'app\static\tables\silver.csv')
    except:
        driver.close()
        metals()


def brent():
    try:
        url_brent = r'https://www.investing.com/commodities/brent-oil-historical-data'

        driver = webdriver.Firefox()
        driver.get(url_brent)
        driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
        driver.find_element_by_css_selector('#startDate').click()
        driver.find_element_by_css_selector('#startDate').clear()
        driver.find_element_by_css_selector('#startDate').send_keys(yr_before)
        driver.find_element_by_css_selector('#endDate').click()
        driver.find_element_by_css_selector('#endDate').clear()
        driver.find_element_by_css_selector('#endDate').send_keys(tod)
        driver.find_element_by_css_selector('#applyBtn').click()
        time.sleep(1)
        df_brent = pd.DataFrame(pd.read_html(driver.page_source)[0])
        driver.close()

        df_brent = df_brent[['Date', 'Price']]
        df_brent['Date'] = pd.to_datetime(df_brent['Date'], format='%b %d, %Y')
        df_brent['Price'] = df_brent['Price'].replace(',', '')
        df_brent['Price'] = df_brent['Price'].astype('float32')
        df_brent.to_csv(r'app\static\tables\brent.csv')
    except:
        driver.close()
        brent()


def coins():
    url_coins = r'http://www.cbr.ru/Bank-notes_coins/cb/'
    tod = str(dt.datetime.now().strftime(format='%d.%m.%Y'))
    yr_before = str((dt.datetime.now() - dt.timedelta(days=365)).strftime(format='%d.%m.%Y'))

    driver = webdriver.Firefox()

    driver.get(url_coins)

    select = Select(driver.find_element_by_css_selector('#UniDbQuery_cat_num'))
    select.options[3].click()
    driver.find_element_by_css_selector('#UniDbQuery_FromDate').clear()
    driver.find_element_by_css_selector('#UniDbQuery_FromDate').send_keys(yr_before)
    driver.find_element_by_css_selector('#UniDbQuery_ToDate').clear()
    driver.find_element_by_css_selector('#UniDbQuery_ToDate').send_keys(tod)
    driver.find_element_by_css_selector('#UniDbQuery_searchbutton').click()
    html_coin_gold = driver.page_source

    select = Select(driver.find_element_by_css_selector('#UniDbQuery_cat_num'))
    select.options[4].click()
    driver.find_element_by_css_selector('#UniDbQuery_FromDate').clear()
    driver.find_element_by_css_selector('#UniDbQuery_FromDate').send_keys(yr_before)
    driver.find_element_by_css_selector('#UniDbQuery_ToDate').clear()
    driver.find_element_by_css_selector('#UniDbQuery_ToDate').send_keys(tod)
    driver.find_element_by_css_selector('#UniDbQuery_searchbutton').click()
    html_coin_silver = driver.page_source

    driver.close()

    df_coin_gold = pd.read_html(html_coin_gold)
    df_coin_gold = pd.DataFrame(df_coin_gold[0])
    df_coin_gold = df_coin_gold.iloc[1:, [0, 5]]
    df_coin_gold.columns = ['Date', 'Price']
    df_coin_gold['Date'] = pd.to_datetime(df_coin_gold['Date'], format='%d.%m.%Y')
    df_coin_gold['Price'] = df_coin_gold['Price'].str.replace(' ', '').str.replace(',', '.').astype('float')
    df_coin_gold.to_csv(r'app\static\tables\coin_gold.csv')

    df_coin_silver= pd.read_html(html_coin_silver)
    df_coin_silver = pd.DataFrame(df_coin_silver[0])
    df_coin_silver = df_coin_silver.iloc[1:, [0, 5]]
    df_coin_silver.columns = ['Date', 'Price']
    df_coin_silver['Date'] = pd.to_datetime(df_coin_silver['Date'], format='%d.%m.%Y')
    df_coin_silver['Price'] = df_coin_silver['Price'].str.replace(' ', '').str.replace(',', '.').astype('float')
    df_coin_silver.to_csv(r'app\static\tables\coin_silver.csv')

def crb():
    try:
        url_crb = r'https://www.investing.com/indices/thomson-reuters---jefferies-crb-historical-data'

        driver = webdriver.Firefox()
        driver.get(url_crb)
        driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
        driver.find_element_by_css_selector('#startDate').click()
        driver.find_element_by_css_selector('#startDate').clear()
        driver.find_element_by_css_selector('#startDate').send_keys(yr_before)
        driver.find_element_by_css_selector('#endDate').click()
        driver.find_element_by_css_selector('#endDate').clear()
        driver.find_element_by_css_selector('#endDate').send_keys(tod)
        driver.find_element_by_css_selector('#applyBtn').click()
        time.sleep(1)
        df_crb = pd.DataFrame(pd.read_html(driver.page_source)[0])
        driver.close()

        df_crb= df_crb[['Date', 'Price']]
        df_crb['Date'] = pd.to_datetime(df_crb['Date'], format='%b %d, %Y')
        df_crb['Price'] = df_crb['Price'].replace(',', '')
        df_crb['Price'] = df_crb['Price'].astype('float32')
        df_crb.to_csv(r'app\static\tables\crb.csv')
    except:
        driver.close()
        crb()

def usdrub():
    try:
        from_date = str((dt.datetime.now() - dt.timedelta(days=720)).strftime(format='%m/%d/%Y'))
        tod = str(dt.datetime.now().strftime(format='%m/%d/%Y'))

        url_usdrub= r'https://www.investing.com/currencies/usd-rub-historical-data'

        driver = webdriver.Firefox()
        driver.get(url_usdrub)
        driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
        driver.find_element_by_css_selector('#startDate').click()
        driver.find_element_by_css_selector('#startDate').clear()
        driver.find_element_by_css_selector('#startDate').send_keys(from_date)
        driver.find_element_by_css_selector('#endDate').click()
        driver.find_element_by_css_selector('#endDate').clear()
        driver.find_element_by_css_selector('#endDate').send_keys(tod)
        driver.find_element_by_css_selector('#applyBtn').click()
        time.sleep(1)
        df_usdrub = pd.DataFrame(pd.read_html(driver.page_source)[0])
        driver.close()

        df_usdrub = df_usdrub[['Date', 'Price']]
        df_usdrub['Date'] = pd.to_datetime(df_usdrub['Date'], format='%b %d, %Y')
        df_usdrub['Price'] = df_usdrub['Price'].replace(',', '')
        df_usdrub['Price'] = df_usdrub['Price'].astype('float32')
    except:
        driver.close()
        usdrub()
    df_usdrub.to_csv(r'app\static\tables\usdrub.csv')

def eurrub():
    try:
        url_eurrub= r'https://www.investing.com/currencies/eur-rub-historical-data'

        tod = str(dt.datetime.now().strftime(format='%m/%d/%Y'))
        from_date = str((dt.datetime.now() - dt.timedelta(days=720)).strftime(format='%m/%d/%Y'))

        driver = webdriver.Firefox()
        driver.get(url_eurrub)
        driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
        driver.find_element_by_css_selector('#startDate').click()
        driver.find_element_by_css_selector('#startDate').clear()
        driver.find_element_by_css_selector('#startDate').send_keys(from_date)
        driver.find_element_by_css_selector('#endDate').click()
        driver.find_element_by_css_selector('#endDate').clear()
        driver.find_element_by_css_selector('#endDate').send_keys(tod)
        driver.find_element_by_css_selector('#applyBtn').click()
        time.sleep(1)
        df_eurrub = pd.DataFrame(pd.read_html(driver.page_source)[0])
        driver.close()

        df_eurrub = df_eurrub[['Date', 'Price']]
        df_eurrub['Date'] = pd.to_datetime(df_eurrub['Date'], format='%b %d, %Y')
        df_eurrub['Price'] = df_eurrub['Price'].replace(',', '')
        df_eurrub['Price'] = df_eurrub['Price'].astype('float32')
        # df_eurrub = df_eurrub.set_index('Date')[str(from_date):].reset_index()
    except:
        driver.close()
        eurrub()
    df_eurrub.to_csv(r'app\static\tables\eurrub.csv')

def eurusd():
    try:
        url_eurusd= r'https://www.investing.com/currencies/eur-usd-historical-data'

        tod = str(dt.datetime.now().strftime(format='%m/%d/%Y'))
        from_date = str((dt.datetime.now() - dt.timedelta(days=720)).strftime(format='%m/%d/%Y'))

        driver = webdriver.Firefox()
        driver.get(url_eurusd)
        driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
        driver.find_element_by_css_selector('#startDate').click()
        driver.find_element_by_css_selector('#startDate').clear()
        driver.find_element_by_css_selector('#startDate').send_keys(from_date)
        driver.find_element_by_css_selector('#endDate').click()
        driver.find_element_by_css_selector('#endDate').clear()
        driver.find_element_by_css_selector('#endDate').send_keys(tod)
        driver.find_element_by_css_selector('#applyBtn').click()
        time.sleep(1)
        df_eurusd = pd.DataFrame(pd.read_html(driver.page_source)[0])
        driver.close()

        df_eurusd = df_eurusd[['Date', 'Price']]
        df_eurusd['Date'] = pd.to_datetime(df_eurusd['Date'], format='%b %d, %Y')
        df_eurusd['Price'] = df_eurusd['Price'].replace(',', '')
        df_eurusd['Price'] = df_eurusd['Price'].astype('float32')
        # df_eurusd = df_eurusd.set_index('Date')[str(from_date):].reset_index()
    except:
        driver.close()
        eurusd()

    df_eurusd.to_csv(r'app\static\tables\eurusd.csv')


def fed():
    try:
        url_fed= r'https://www.investing.com/economic-calendar/interest-rate-decision-168'

        from_date = str((dt.datetime.now() - dt.timedelta(days=365)).strftime(format='%Y-%m-%d'))

        driver = webdriver.Firefox()
        driver.get(url_fed)
        driver.find_element_by_css_selector('#showMoreHistory168').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#showMoreHistory168').click()
        time.sleep(1)
        html = driver.page_source
        driver.close()

        html = pd.read_html(html)[0]
        fed = pd.DataFrame(html)
        fed = fed[['Release Date', 'Actual']]
        fed.Actual = fed.Actual.str.replace('%', '').astype('float').dropna()
        fed['Release Date'] = pd.to_datetime(fed['Release Date'], format='%b %d, %Y')
        fed = fed.set_index('Release Date')[:str(from_date)].reset_index()
        fed = fed.dropna()
    except:
        driver.close()
        fed()

    fed.to_csv(r'app\static\tables\fed.csv')


def cbr_rate():
    try:
        url_fed= r'https://www.investing.com/economic-calendar/russian-interest-rate-decision-554'

        from_date = str((dt.datetime.now() - dt.timedelta(days=360)).strftime(format='%Y-%m-%d'))

        driver = webdriver.Firefox()
        driver.get(url_fed)
        driver.find_element_by_css_selector('#showMoreHistory554').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#showMoreHistory554').click()
        time.sleep(1)
        driver.find_element_by_css_selector('#showMoreHistory554').click()
        time.sleep(2)
        html = driver.page_source
        driver.close()

        html = pd.read_html(html)[0]
        cbr_rate = pd.DataFrame(html)
        cbr_rate = cbr_rate[['Release Date', 'Actual']]
        cbr_rate.Actual = cbr_rate.Actual.str.replace('%', '').astype('float').dropna()
        cbr_rate['Release Date'] = cbr_rate['Release Date'].str[:-6]
        cbr_rate['Release Date'] = pd.to_datetime(cbr_rate['Release Date'], format='%b %d, %Y')
        cbr_rate = cbr_rate.set_index('Release Date')[:str(from_date)].reset_index()
        cbr_rate = cbr_rate.dropna()
    except:
        driver.close()
        cbr_rate()

    cbr_rate.to_csv(r'app\static\tables\cbr_rate.csv')


def dep_auctions():
    to_date = str(dt.datetime.now().strftime(format='%d.%m.%Y'))
    from_date = str((dt.datetime.now() - dt.timedelta(days=180)).strftime(format='%d.%m.%Y'))

    df_url = r'http://cbr.ru/hd_base/itogidepauct/'

    driver = webdriver.Firefox()
    driver.get(df_url)
    driver.find_element_by_id('UniDbQuery_FromDate').click()
    driver.find_element_by_id('UniDbQuery_FromDate').clear()
    driver.find_element_by_id('UniDbQuery_FromDate').send_keys(from_date)
    driver.find_element_by_id('UniDbQuery_ToDate').click()
    driver.find_element_by_id('UniDbQuery_ToDate').clear()
    driver.find_element_by_id('UniDbQuery_ToDate').send_keys(to_date)
    driver.find_element_by_id('UniDbQuery_searchbutton').click()
    html = driver.page_source
    driver.close()

    df = pd.read_html(html)[0]
    columns = list(df.iloc[0])
    df = df.iloc[1:]
    df.columns = columns
    df = df[['Дата проведения аукциона',
             'Срок депозита',
             'Объем привлеченных денежных средств, (млрд рублей)',
             'Объем предложения (млрд рублей)',
             'Ставка отсечения',
             'Средневзвешенная ставка']]
    df['Объем привлеченных денежных средств, (млрд рублей)'] = df[
        'Объем привлеченных денежных средств, (млрд рублей)'].str.replace(' ', '').str.replace(',', '.').astype('float')
    df['Объем предложения (млрд рублей)'] = df['Объем предложения (млрд рублей)'].str.replace(' ', '').str.replace(',','.').astype('float')
    df['Дата проведения аукциона'] = pd.to_datetime(df['Дата проведения аукциона'], format='%d.%m.%Y')
    df['Ставка отсечения'] = df['Ставка отсечения'].str.replace('%', '').str.replace(',', '.').astype('float')
    df['Средневзвешенная ставка'] = df['Средневзвешенная ставка'].str.replace('%', '').str.replace(',', '.').astype('float')
    df.columns = ['Date', 'Terms', 'Borrowed', 'Offered', 'Cut Rat', 'Avg Rate']
    df_1w = df[df['Terms'] == '1 неделя']
    df_1w.to_csv(r'app\static\tables\dep_auc_1w.csv')
    df_days = df[df['Terms'] != '1 неделя']

    df_days.to_csv(r'app\static\tables\dep_auc_days.csv')


def ruonia():
    to_date = str(dt.datetime.now().strftime(format='%Y-%m-%d'))
    from_date = str((dt.datetime.now() - dt.timedelta(days=365)).strftime(format='%Y-%m-%d'))

    url_ruonia = 'http://ruonia.ru/archive?date_from={0}&date_to={1}&format=csv'.format(from_date, to_date)

    df_ruonia = pd.read_csv(url_ruonia, encoding='Windows-1251', header=1)
    df_ruonia = df_ruonia.iloc[:, 0:2]
    df_ruonia.columns = ['Date', 'Ruonia']
    df_ruonia['Date'] = pd.to_datetime(df_ruonia['Date'], format='%d.%m.%Y')
    df_ruonia['Ruonia'] = df_ruonia['Ruonia'].str.replace(',', '.')
    df_ruonia['Ruonia'] = df_ruonia['Ruonia'].astype('float')

    df_ruonia.to_csv(r'app\static\tables\ruonia.csv')

def mosprime():
    mosprime_url = r'http://www.cbr.ru/hd_base/mosprime/'

    from_date = (dt.datetime.now() - dt.timedelta(days=365)).strftime(format='%d.%m.%Y')
    to_date = dt.datetime.now().strftime(format='%d.%m.%Y')

    driver = webdriver.Firefox()
    driver.get(mosprime_url)
    driver.find_element_by_id('UniDbQuery_FromDate').clear()
    driver.find_element_by_id('UniDbQuery_FromDate').send_keys(from_date)
    driver.find_element_by_id('UniDbQuery_ToDate').clear()
    driver.find_element_by_id('UniDbQuery_ToDate').send_keys(to_date)
    driver.find_element_by_id('UniDbQuery_searchbutton').click()
    html = driver.page_source
    df_mosprime = pd.read_html(html)[0]
    driver.close()

    df_mosprime = df_mosprime[1:]
    df_mosprime.columns = ['date', 'on', '1w', '2w', '1m', '2m', '3m', '6m']
    broken = df_mosprime[df_mosprime['on'] == '—'].index
    df_mosprime = df_mosprime.drop(broken)

    df_mosprime.to_csv(r'app\static\tables\mosprime.csv')


def repo_on():
    tod = str(dt.datetime.now().strftime(format='%d.%m.%Y'))
    yr_before = str((dt.datetime.now() - dt.timedelta(days=365)).strftime(format='%d.%m.%Y'))

    repo_on_url = r'https://www.moex.com/ru/index/MOEXREPO/archive/#/from=2018-09-17&till=2018-10-17&sort=TRADEDATE&order=desc'

    driver = webdriver.Firefox()
    driver.get(repo_on_url)
    time.sleep(3)
    # driver.find_element_by_tag_name('a.btn2').click()
    driver.find_element_by_id('from_date').clear()
    driver.find_element_by_id('from_date').send_keys(yr_before)
    driver.find_element_by_id('to_date').clear()
    driver.find_element_by_id('to_date').send_keys(tod)
    driver.find_element_by_id('searchBtn').click()
    time.sleep(3)
    html = driver.page_source

    repo_on_df = pd.read_html(html)[0]
    repo_on_df = repo_on_df[1:]
    dfs = []
    dfs.append(repo_on_df)

    while len(repo_on_df) == 100:
        driver.find_element_by_xpath('//ul[2]/li[2]/a').click()
        time.sleep(3)
        html = driver.page_source
        repo_on_df = pd.read_html(html)[0]
        repo_on_df = repo_on_df[1:]
        dfs.append(repo_on_df)

    driver.close()

    repo_on_df = pd.DataFrame(None)
    for df in dfs:
        repo_on_df = pd.concat([repo_on_df, df])

    repo_on_df.columns = ['date', 'open', 'high', 'low', 'close', 'vol', 'cap']
    repo_on_df['date'] = pd.to_datetime(repo_on_df['date'], format='%d.%m.%Y')
    repo_on_df = repo_on_df.set_index('date').sort_index()

    cols = ['open', 'high', 'low', 'close']
    repo_on_df[cols] = repo_on_df[cols].astype('float')
    repo_on_df = repo_on_df[cols].applymap(lambda x: x / 10 if x < 100 else x / 100)

    repo_on_df.to_csv(r'app\static\tables\repo_on.csv')


def repo_1w():
    tod = str(dt.datetime.now().strftime(format='%d.%m.%Y'))
    yr_before = str((dt.datetime.now() - dt.timedelta(days=365)).strftime(format='%d.%m.%Y'))

    repo_1w_url = r'https://www.moex.com/ru/index/MOEXREPO1W/archive/#/from=2018-09-17&till=2018-10-17&sort=TRADEDATE&order=desc'

    driver = webdriver.Firefox()
    driver.get(repo_1w_url)
    time.sleep(3)
    # driver.find_element_by_tag_name('a.btn2').click()
    driver.find_element_by_id('from_date').clear()
    driver.find_element_by_id('from_date').send_keys(yr_before)
    driver.find_element_by_id('to_date').clear()
    driver.find_element_by_id('to_date').send_keys(tod)
    driver.find_element_by_id('searchBtn').click()
    time.sleep(3)
    html = driver.page_source

    repo_1w_df = pd.read_html(html)[0]
    repo_1w_df = repo_1w_df[1:]
    dfs = []
    dfs.append(repo_1w_df)

    while len(repo_1w_df) == 100:
        driver.find_element_by_xpath('//ul[2]/li[2]/a').click()
        time.sleep(3)
        html = driver.page_source
        repo_1w_df = pd.read_html(html)[0]
        repo_1w_df = repo_1w_df[1:]
        dfs.append(repo_1w_df)

    driver.close()

    repo_1w_df = pd.DataFrame(None)
    for df in dfs:
        repo_1w_df = pd.concat([repo_1w_df, df])

    repo_1w_df.columns = ['date', 'open', 'high', 'low', 'close', 'vol', 'cap']
    repo_1w_df['date'] = pd.to_datetime(repo_1w_df['date'], format='%d.%m.%Y')
    repo_1w_df = repo_1w_df.set_index('date').sort_index()

    cols = ['open', 'high', 'low', 'close']
    repo_1w_df[cols] = repo_1w_df[cols].astype('float')
    repo_1w_df = repo_1w_df[cols].applymap(lambda x: x / 10 if x < 100 else x / 100)

    repo_1w_df.to_csv(r'app\static\tables\repo_1w.csv')


def idx_mmvb():
    mmvb_end_date = dt.datetime.today()
    end_date_format1 = dt.datetime.strftime(dt.datetime.date(mmvb_end_date), format='%Y%m%d')
    end_date_format2 = dt.datetime.strftime(dt.datetime.date(mmvb_end_date), format='%d.%m.%D')
    end_day = dt.datetime.strftime(dt.datetime.date(mmvb_end_date), format='%d')
    end_month = dt.datetime.strftime(dt.datetime.date(mmvb_end_date), format='%m')
    end_year = dt.datetime.strftime(dt.datetime.date(mmvb_end_date), format='%Y')
    mmvb_start_date = mmvb_end_date - dt.timedelta(days=90)
    mmvb_end_date = mmvb_end_date.strftime('%d.%m.%Y')
    mmvb_start_date = mmvb_start_date.strftime('%Y-%m-%d')

    url_idx_mmvb = r'http://export.finam.ru/MICEXINDEXCF_160101_today.csv?market=6&em=13851&code=MICEXINDEXCF&apply=0&df=1&mf=0&yf=2016&from=01.01.2016&dt={2}&mt={3}&yt={4}&to={1}&p=8&f=MICEXINDEXCF_160101_{1}&e=.csv&cn=MICEXINDEXCF&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=3&sep2=1&datf=1&at=1'.format(end_date_format1, end_date_format2, end_day, end_month, end_year)

    df_mmvb = pd.read_csv(url_idx_mmvb, delimiter=';')
    df_mmvb = df_mmvb[['<DATE>', '<CLOSE>']].astype('str')
    df_mmvb['<DATE>'] = pd.to_datetime(df_mmvb['<DATE>'], format='%Y-%m-%d')
    df_mmvb['<CLOSE>'] = df_mmvb['<CLOSE>'].astype('float')
    df_mmvb.set_index('<DATE>', inplace=True)
    df_mmvb = df_mmvb[mmvb_start_date:].reset_index()

    df_mmvb.to_csv(r'app\static\tables\idx_mmvb.csv')


def mmvb10():
    mmvb_end_date = dt.datetime.today()
    end_date_format1 = dt.datetime.strftime(dt.datetime.date(mmvb_end_date), format='%Y%m%d')
    end_date_format2 = dt.datetime.strftime(dt.datetime.date(mmvb_end_date), format='%d.%m.%D')
    end_day = dt.datetime.strftime(dt.datetime.date(mmvb_end_date), format='%d')
    end_month = dt.datetime.strftime(dt.datetime.date(mmvb_end_date), format='%m')
    end_year = dt.datetime.strftime(dt.datetime.date(mmvb_end_date), format='%Y')
    mmvb_start_date = mmvb_end_date - dt.timedelta(days=90)
    mmvb_end_date = mmvb_end_date.strftime('%d.%m.%Y')
    mmvb_start_date = mmvb_start_date.strftime('%Y-%m-%d')

    url_mmvb_10 = r'http://export.finam.ru/RI.MICEX10INDEX_160101_180122.csv?market=91&em=420451&code=RI.MICEX10INDEX&apply=0&df=1&mf=0&yf=2016&from=01.01.2016&dt={2}&mt={3}&yt={4}&to={1}&p=8&f=RI.MICEX10INDEX_160101_180122&e=.csv&cn=RI.MICEX10INDEX&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=3&sep2=1&datf=1&at=1'.format(end_date_format1, end_date_format2, end_day, end_month, end_year)

    df_mmvb_10 = pd.read_csv(url_mmvb_10, delimiter=';')
    df_mmvb_10 = df_mmvb_10[['<DATE>', '<CLOSE>']].astype('str')
    df_mmvb_10['<DATE>'] = pd.to_datetime(df_mmvb_10['<DATE>'], format='%Y-%m-%d')
    df_mmvb_10['<CLOSE>'] = df_mmvb_10['<CLOSE>'].astype('float')
    df_mmvb_10.set_index('<DATE>', inplace=True)
    df_mmvb_10 = df_mmvb_10[mmvb_start_date:].reset_index()

    df_mmvb_10.to_csv(r'app\static\tables\mmvb_10.csv')

def sp():
    from_date = str((dt.datetime.now() - dt.timedelta(days=720)).strftime(format='%m/%d/%Y'))
    tod = str(dt.datetime.now().strftime(format='%m/%d/%Y'))

    url_sp= r'https://www.investing.com/indices/us-spx-500-historical-data'

    driver = webdriver.Firefox()
    driver.get(url_sp)
    driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
    driver.find_element_by_css_selector('#startDate').click()
    driver.find_element_by_css_selector('#startDate').clear()
    driver.find_element_by_css_selector('#startDate').send_keys(from_date)
    driver.find_element_by_css_selector('#endDate').click()
    driver.find_element_by_css_selector('#endDate').clear()
    driver.find_element_by_css_selector('#endDate').send_keys(tod)
    driver.find_element_by_css_selector('#applyBtn').click()
    time.sleep(1)
    df_sp= pd.DataFrame(pd.read_html(driver.page_source)[0])
    driver.close()

    df_sp = df_sp[['Date', 'Price']]
    df_sp['Date'] = pd.to_datetime(df_sp['Date'], format='%b %d, %Y')
    df_sp['Price'] = df_sp['Price'].replace(',', '')
    df_sp['Price'] = df_sp['Price'].astype('float32')
    # df_sp = df_sp.set_index('Date')[str(from_date):].reset_index()
    df_sp.to_csv(r'app\static\tables\sp.csv')


def djia():
    from_date = str((dt.datetime.now() - dt.timedelta(days=720)).strftime(format='%m/%d/%Y'))
    tod = str(dt.datetime.now().strftime(format='%m/%d/%Y'))

    url_djia= r'https://www.investing.com/indices/us-30-historical-data'

    driver = webdriver.Firefox()
    driver.get(url_djia)
    driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
    driver.find_element_by_css_selector('#startDate').click()
    driver.find_element_by_css_selector('#startDate').clear()
    driver.find_element_by_css_selector('#startDate').send_keys(from_date)
    driver.find_element_by_css_selector('#endDate').click()
    driver.find_element_by_css_selector('#endDate').clear()
    driver.find_element_by_css_selector('#endDate').send_keys(tod)
    driver.find_element_by_css_selector('#applyBtn').click()
    time.sleep(1)
    df_djia= pd.DataFrame(pd.read_html(driver.page_source)[0])
    driver.close()

    df_djia = df_djia[['Date', 'Price']]
    df_djia['Date'] = pd.to_datetime(df_djia['Date'], format='%b %d, %Y')
    df_djia['Price'] = df_djia['Price'].replace(',', '')
    df_djia['Price'] = df_djia['Price'].astype('float32')
    # df_djia = df_djia.set_index('Date')[str(from_date):].reset_index()
    df_djia.to_csv(r'app\static\tables\djia.csv')


def dax():
    from_date = str((dt.datetime.now() - dt.timedelta(days=720)).strftime(format='%m/%d/%Y'))
    tod = str(dt.datetime.now().strftime(format='%m/%d/%Y'))

    url_dax= r'https://www.investing.com/indices/germany-30-historical-data'

    driver = webdriver.Firefox()
    driver.get(url_dax)
    driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
    driver.find_element_by_css_selector('#startDate').click()
    driver.find_element_by_css_selector('#startDate').clear()
    driver.find_element_by_css_selector('#startDate').send_keys(from_date)
    driver.find_element_by_css_selector('#endDate').click()
    driver.find_element_by_css_selector('#endDate').clear()
    driver.find_element_by_css_selector('#endDate').send_keys(tod)
    driver.find_element_by_css_selector('#applyBtn').click()
    time.sleep(1)
    df_dax= pd.DataFrame(pd.read_html(driver.page_source)[0])
    driver.close()

    df_dax = df_dax[['Date', 'Price']]
    df_dax['Date'] = pd.to_datetime(df_dax['Date'], format='%b %d, %Y')
    df_dax['Price'] = df_dax['Price'].replace(',', '')
    df_dax['Price'] = df_dax['Price'].astype('float32')
    # df_dax = df_dax.set_index('Date')[str(from_date):].reset_index()
    df_dax.to_csv(r'app\static\tables\dax.csv')


def vix():
    from_date = str((dt.datetime.now() - dt.timedelta(days=720)).strftime(format='%m/%d/%Y'))
    tod = str(dt.datetime.now().strftime(format='%m/%d/%Y'))

    url_vix= r'https://investing.com/indices/volatility-s-p-500-historical-data'

    driver = webdriver.Firefox()
    driver.get(url_vix)
    driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
    driver.find_element_by_css_selector('#startDate').click()
    driver.find_element_by_css_selector('#startDate').clear()
    driver.find_element_by_css_selector('#startDate').send_keys(from_date)
    driver.find_element_by_css_selector('#endDate').click()
    driver.find_element_by_css_selector('#endDate').clear()
    driver.find_element_by_css_selector('#endDate').send_keys(tod)
    driver.find_element_by_css_selector('#applyBtn').click()
    time.sleep(1)
    df_vix= pd.DataFrame(pd.read_html(driver.page_source)[0])
    driver.close()

    df_vix = df_vix[['Date', 'Price']]
    df_vix['Date'] = pd.to_datetime(df_vix['Date'], format='%b %d, %Y')
    df_vix['Price'] = df_vix['Price'].replace(',', '')
    df_vix['Price'] = df_vix['Price'].astype('float32')
    # df_vix = df_vix.set_index('Date')[str(from_date):].reset_index()
    df_vix.to_csv(r'app\static\tables\vix.csv')


def msci():
    url_msci = r'https://www.investing.com/indices/msci-bric-net-usd-historical-data'

    from_date = str((dt.datetime.now() - dt.timedelta(days=180)).strftime(format='%m/%d/%Y'))

    driver = webdriver.Firefox()
    driver.get(url_msci)
    driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
    driver.find_element_by_id('startDate').click()
    driver.find_element_by_id('startDate').clear()
    driver.find_element_by_id('startDate').send_keys(from_date)
    driver.find_element_by_id('endDate').click()
    driver.find_element_by_id('endDate').clear()
    driver.find_element_by_id('endDate').send_keys(tod)
    driver.find_element_by_id('applyBtn').click()
    time.sleep(1)
    df_msci = pd.DataFrame(pd.read_html(driver.page_source)[0])
    driver.close()

    df_msci = df_msci[['Date', 'Price']]
    df_msci['Date'] = pd.to_datetime(df_msci['Date'], format='%b %d, %Y')
    df_msci['Price'] = df_msci['Price'].replace(',', '')
    df_msci['Price'] = df_msci['Price'].astype('float32')
    df_msci.to_csv(r'app\static\tables\msci.csv')


def gspread():
    tab_path = r'C:\Users\RNCB\PycharmProjects\oofr_research\app\static\tables'

    url_cbonds = 'http://ru.cbonds.info/quotes/?page=1'
    url_filter = 'http://ru.cbonds.info/quotes/?reset=1&search_do=1&search_type=rangedate&trading-ground%5B0%5D=1&emitent%5B0%5D=138&emission%5B0%5D=238&mode=1&tradings-date%5B0%5D={}&tradings-date%5B1%5D=2019-01-17&dir=DESC'.format((dt.datetime.now() - dt.timedelta(days=365)).strftime(format='%Y-%m-%d'))
    login = 'kudryavtsevay@rncb.ru'
    password = 'antonkdr1975'

    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', tab_path)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/plain, application/vnd.ms-excel, text/csv, text/comma-separated-values, application/octet-stream, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    driver = webdriver.Firefox(profile)
    driver.get(url_cbonds)
    # Login CBonds
    driver.find_element_by_id('auth_login').click()
    driver.find_element_by_id('auth_login').send_keys(login)
    driver.find_element_by_id('auth_pwd').click()
    driver.find_element_by_id('auth_pwd').send_keys(password)
    driver.find_element_by_id('auth_submit_btn').click()
    # Save OFZ
    driver.get(url_filter)
    driver.find_element_by_css_selector('.export-csv-btn').click()
    time.sleep(10)
    driver.close()

    df_ofz = pd.read_csv(tab_path + r'\ru_quotes.csv', delimiter=';')
    df_ofz = df_ofz[['Дата торгов', 'Доходность к погашению, эфф. по индикативной цене']]
    df_ofz['Доходность к погашению, эфф. по индикативной цене'] = df_ofz['Доходность к погашению, эфф. по индикативной цене'] * 100
    df_ofz.columns = ['Date', 'Price']
    df_ofz['Date'] = pd.to_datetime(df_ofz['Date'], format='%d.%m.%Y')
    df_ofz.to_csv(tab_path + '/ru_quotes.csv')

    # Save 10T
    tod = str(dt.datetime.now().strftime(format='%m/%d/%Y'))
    yr_before = str((dt.datetime.now() - dt.timedelta(days=365)).strftime(format='%m/%d/%Y'))

    url_t10 = 'https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data'

    driver = webdriver.Firefox()
    driver.get(url_t10)
    driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
    driver.find_element_by_css_selector('#startDate').click()
    driver.find_element_by_css_selector('#startDate').clear()
    driver.find_element_by_css_selector('#startDate').send_keys(yr_before)
    driver.find_element_by_css_selector('#endDate').click()
    driver.find_element_by_css_selector('#endDate').clear()
    driver.find_element_by_css_selector('#endDate').send_keys(tod)
    driver.find_element_by_css_selector('#applyBtn').click()
    time.sleep(1)
    df_t10 = pd.DataFrame(pd.read_html(driver.page_source)[0])
    driver.close()

    df_t10.to_csv(r'C:\Users\RNCB\PycharmProjects\oofr_research\app\static\tables\t10.csv')

    df_t10 = df_t10[['Date', 'Price']]
    df_t10['Date'] = pd.to_datetime(df_t10['Date'], format='%b %d, %Y')
    df_total = pd.merge(df_ofz, df_t10, on='Date', how='inner')
    df_total.columns = ['Date', 'ofz', 't10']
    df_total['spread'] = df_total['ofz'] - df_total['t10']
    ofz_file = tab_path + '\\ru_quotes.csv'
    os.remove(ofz_file)

    df_total.to_csv(r'app\static\tables\spread.csv')


def gcurve():
    # url_gcurve = 'https://www.moex.com/ru/marketdata/indices/state/g-curve/'
    #
    # yesterday = (dt.datetime.now() - dt.timedelta(days=1))
    # while dt.datetime.weekday(dt.datetime.now() - dt.timedelta(days=1)) not in [0, 1, 2, 3, 4]:
    #     yesterday = (dt.datetime.now() - dt.timedelta(days=1))
    # yesterday = yesterday.strftime(format='%d.%m.%Y')
    #
    # week = (dt.datetime.strptime(yesterday, '%d.%m.%Y') - dt.timedelta(days=7)).strftime(format='%d.%m.%Y')
    #
    # driver = webdriver.Firefox()
    # driver.get(url_gcurve)
    #
    # driver.find_element_by_xpath('//div[2]/input').click()
    # driver.find_element_by_xpath('//div[2]/input').clear()
    # driver.find_element_by_xpath('//div[2]/input').send_keys(yesterday)
    # driver.find_element_by_css_selector('button.button80b').click()
    # html_w0 = driver.page_source
    #
    # driver.find_element_by_xpath('//div[2]/input').click()
    # driver.find_element_by_xpath('//div[2]/input').clear()
    # driver.find_element_by_xpath('//div[2]/input').send_keys(week)
    # driver.find_element_by_css_selector('button.button80b').click()
    # html_w_1 = driver.page_source
    #
    # driver.close()
    #
    # text_w0 = pd.read_html(html_w0)[1][0][0].split(',')[2].split(' ')[3]
    # text_w_1 = pd.read_html(html_w_1)[1][0][0].split(',')[2].split(' ')[3]
    #
    # data_w0 = []
    # while len(text_w0) > 3:
    #     data_w0.append(text_w0[:4])
    #     text_w0 = text_w0[4:]
    #
    # data_w_1 = []
    # while len(text_w_1) > 3:
    #     data_w_1.append(text_w_1[:4])
    #     text_w_1 = text_w_1[4:]
    #
    # columns = [0.25, 0.5, 0.75, 1, 2, 3, 5, 7, 10, 15, 20, 30]
    # df_gcurve = pd.DataFrame(data={'r': columns, 'w0': data_w0, 'w1': data_w_1})

    url_gcurve = r'http://www.cbr.ru/hd_base/zcyc_params/'
    df_gcurve = pd.read_html(url_gcurve)
    df_gcurve = df_gcurve[0].dropna()
    df_gcurve.columns = ['date', '0.25', '0.5', '0.75', '1', '2', '3', '5', '7', '10', '15', '20', '30']
    df_gcurve.drop('date', axis=1, inplace=True)
    df = df_gcurve.iloc[[0, 4]].T.reset_index()
    df.columns = ['r', 'w0', 'w1']
    df.to_csv(r'app\static\tables\gcurve.csv')

def mibor():
    driver = webdriver.Firefox()
    driver.get('http://www.cbr.ru/hd_base/mkr/mkr_retro_mibid/')
    driver.find_element_by_id('label_UniDbQuery_SOP').click()
    select = Select(driver.find_element_by_id('UniDbQuery_Currency'))
    select.options[1].click()
    driver.find_element_by_id('UniDbQuery_Dd7').click()
    driver.find_element_by_id('UniDbQuery_Dd30').click()
    driver.find_element_by_id('UniDbQuery_Dd90').click()
    driver.find_element_by_id('UniDbQuery_Dd180').click()
    driver.find_element_by_id('UniDbQuery_Dd360').click()
    driver.find_element_by_id('UniDbQuery_FromDate').clear()
    driver.find_element_by_id('UniDbQuery_FromDate').send_keys('27.12.2008')
    driver.find_element_by_id('UniDbQuery_ToDate').clear()
    driver.find_element_by_id('UniDbQuery_ToDate').send_keys('27.12.2018')
    driver.find_element_by_id('UniDbQuery_searchbutton').click()
    time.sleep(2)
    df = driver.page_source
    df = pd.DataFrame(pd.read_html(df)[0][1:])
    df.columns = ['Date', 'Price']
    df.Price = df.Price.astype('float') / 100
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
    driver.close()
    df.to_csv(r'app\static\tables\mibor.csv')

def div_sp():
    file_div = r'http://www.multpl.com/s-p-500-dividend-yield/table?f=m'
    df_div = pd.read_html(file_div)[0]
    df_div.columns = df_div.iloc[0]
    df_div = df_div[1:]
    df_div['Yield Value'] = df_div['Yield Value'].str.split('%').str[0].astype('float')
    df_div['Date'] = pd.to_datetime(df_div['Date'], format='%b %d, %Y')
    df_div.dropna(inplace=True)
    df_div = df_div[df_div['Date'] > (dt.datetime.now() - dt.timedelta(days=365*10))]
    df_div.to_csv(r'app\static\tables\div_sp.csv')


def tnx():
    url_tnx = 'https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data'
    try:
        driver = webdriver.Firefox()
        driver.get(url_tnx)
        driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
        driver.find_element_by_css_selector('#startDate').clear()
        driver.find_element_by_css_selector('#startDate').send_keys('01/01/2000')
        driver.find_element_by_css_selector('#endDate').clear()
        driver.find_element_by_css_selector('#endDate').send_keys(tod)
        driver.find_element_by_css_selector('#applyBtn').click()
        time.sleep(3)
        df = pd.DataFrame(pd.read_html(driver.page_source)[0])
        driver.close()

        df = df[['Date', 'Price']]
        df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')
        df['Price'] = df['Price'].replace(',', '')
        df['Price'] = df['Price'].astype('float32')
    except:
        driver.close()
        tnx()
    df.to_csv(r'app\static\tables\tnx.csv')


def ofz10():
    url_ofz10 = 'https://investing.com/rates-bonds/russia-10-year-bond-yield-historical-data'
    try:
        driver = webdriver.Firefox()
        driver.get(url_ofz10)
        driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
        driver.find_element_by_css_selector('#startDate').clear()
        driver.find_element_by_css_selector('#startDate').send_keys('01/01/2009')
        driver.find_element_by_css_selector('#endDate').clear()
        driver.find_element_by_css_selector('#endDate').send_keys(tod)
        driver.find_element_by_css_selector('#applyBtn').click()
        time.sleep(3)
        df = pd.DataFrame(pd.read_html(driver.page_source)[0])
        driver.close()

        df = df[['Date', 'Price']]
        df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')
        df['Price'] = df['Price'].replace(',', '')
        df['Price'] = df['Price'].astype('float32')
    except:
        driver.close()
        ofz10()
    df.to_csv(r'app\static\tables\ofz10.csv')


def mcx10():
    url_mcx10 = 'https://www.investing.com/indices/mcx10-historical-data'
    try:
        driver = webdriver.Firefox()
        driver.get(url_mcx10)
        driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
        driver.find_element_by_css_selector('#startDate').clear()
        driver.find_element_by_css_selector('#startDate').send_keys('01/01/2009')
        driver.find_element_by_css_selector('#endDate').clear()
        driver.find_element_by_css_selector('#endDate').send_keys(tod)
        driver.find_element_by_css_selector('#applyBtn').click()
        time.sleep(3)
        df = pd.DataFrame(pd.read_html(driver.page_source)[0])
        driver.close()

        df = df[['Date', 'Price']]
        df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')
        df['Price'] = df['Price'].replace(',', '')
        df['Price'] = df['Price'].astype('float32')
    except:
        driver.close()
        mcx10()
    df.to_csv(r'app\static\tables\mcx10.csv')


def sp():
    url_sp= 'https://www.investing.com/indices/us-spx-500-historical-data'
    try:
        driver = webdriver.Firefox()
        driver.get(url_sp)
        driver.find_element_by_css_selector('#flatDatePickerCanvasHol').click()
        driver.find_element_by_css_selector('#startDate').clear()
        driver.find_element_by_css_selector('#startDate').send_keys('01/01/2009')
        driver.find_element_by_css_selector('#endDate').clear()
        driver.find_element_by_css_selector('#endDate').send_keys(tod)
        driver.find_element_by_css_selector('#applyBtn').click()
        time.sleep(3)
        df = pd.DataFrame(pd.read_html(driver.page_source)[0])
        driver.close()

        df = df[['Date', 'Price']]
        df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')
        df['Price'] = df['Price'].replace(',', '')
        df['Price'] = df['Price'].astype('float32')
    except:
        driver.close()
        sp()
    df.to_csv(r'app\static\tables\sp.csv')


def fed3m():
    this_year = dt.datetime.now().year
    years_range = list(range(1990, this_year + 1))
    for year in years_range:
        fed3m_url = r'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldYear&year=' + str(
            year)
        df_fed3m = pd.read_html(fed3m_url)[0]
        header = df_fed3m.iloc[1, :10]
        df_fed3m = df_fed3m.iloc[2:, :10]
        df_fed3m.columns = header
        df_fed3m = df_fed3m[['Date', '3 mo']]
        if year == years_range[0]:
            df = pd.DataFrame(columns=['Date', '3 mo'])
        df = pd.merge(df, df_fed3m, how='outer')
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')
    df.to_csv(r'app\static\tables\fed3m.csv')


def gold_copper():
    end = dt.datetime.today()
    # start = end - dt.timedelta(days=365)
    start = dt.datetime.strptime('01012000', '%d%m%Y')

    copper_url = r'http://export.finam.ru/LME.Copper_170101_190116.txt?market=24&em=18931&code=LME.Copper&apply=0&df={1}&mf={2}&yf={3}&from={0}&dt={5}&mt={6}&yt={7}&to={4}&p=8&f=LME.Copper_170101_190116&e=.txt&cn=LME.Copper&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=3&sep2=1&datf=1&at=1' \
        .format(start.strftime('%d.%m.%Y'),
                str(start.day),
                str(start.month - 1),
                str(start.year),
                end.strftime('%d.%m.%Y'),
                str(end.day),
                str(end.month - 1),
                str(end.year),
                )
    gold_url = r'http://export.finam.ru/comex.GC_170101_190116.txt?market=24&em=18953&code=comex.GC&apply=0&df={1}&mf={2}&yf={3}&from={0}&dt={5}&mt={6}&yt={7}&to={4}&p=8&f=comex.GC_170101_190116&e=.txt&cn=comex.GC&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=3&sep2=1&datf=1&at=1' \
        .format(start.strftime('%d.%m.%Y'),
                str(start.day),
                str(start.month - 1),
                str(start.year),
                end.strftime('%d.%m.%Y'),
                str(end.day),
                str(end.month - 1),
                str(end.year),
                )
    copper = pd.read_csv(copper_url, sep=';')
    gold = pd.read_csv(gold_url, sep=';')
    def proc_finam(df):
        df = df.iloc[:, [2, -2]]
        df.columns = ['datetime', 'close']
        df.datetime = pd.to_datetime(df.datetime, format='%Y%m%d')
        return df
    copper = proc_finam(copper)
    gold = proc_finam(gold)
    df = gold[['datetime', 'close']].merge(copper[['datetime', 'close']], on='datetime')
    df.columns = ['datetime', 'gold', 'copper']
    df['ratio'] = df['copper'] / df['gold']
    df.to_csv(r'app\static\tables\gold_copper.csv')


def rts():
    rts_end_date = dt.datetime.today()
    rts_start_date = rts_end_date - dt.timedelta(days=90)
    rts_end_date = rts_end_date.strftime('%d.%m.%Y')
    rts_start_date = rts_start_date.strftime('%d.%m.%Y')

    rts_source = 'http://export.finam.ru/SPFB.RTS_170804_171127.csv?market=14&em=17455&code=SPFB.RTS&apply=0&df=4&mf=7&yf=2017&from={}&to={}&p=8&f=SPFB.RTS_170804_171127&e=.csv&cn=SPFB.RTS&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1'.format(
        rts_start_date, rts_end_date)
    df_rts = pd.read_csv(rts_source, delimiter=',')
    df_rts = df_rts[['<DATE>', '<CLOSE>', '<VOL>']].astype('str')
    df_rts['<DATE>'] = pd.to_datetime(df_rts['<DATE>'], format='%Y-%m-%d')
    df_rts['<CLOSE>'] = df_rts['<CLOSE>'].astype('float')
    df_rts['<VOL>'] = df_rts['<VOL>'].astype('float')
    df_rts = df_rts.replace(0.0, np.nan)
    df_rts.dropna(inplace=True)
    df_rts.columns = ['Date', 'Close', 'Vol']

    df_rts.to_csv(r'app\static\tables\rts.csv')


def si():
    si_end_date = dt.datetime.today()
    si_start_date = si_end_date - dt.timedelta(days=90)
    si_start_date = si_start_date.strftime('%d.%m.%Y')

    end_day = dt.datetime.strftime(dt.datetime.date(si_end_date), format='%d')
    end_month = dt.datetime.strftime(dt.datetime.date(si_end_date), format='%m')
    end_year = dt.datetime.strftime(dt.datetime.date(si_end_date), format='%Y')
    si_source = 'http://export.finam.ru/SPFB.Si_170804_171127.csv?market=14&em=19899&code=SPFB.Si&apply=0&df=4&mf=7&yf=2017&from={0}&to={0}&mt={1}&yt={2}&p=8&f=SPFB.Si_170804_171127&e=.csv&cn=SPFB.Si&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1'.format(
        end_day, end_month, end_year)
    df_si = pd.read_csv(si_source, delimiter=',')
    df_si = df_si[['<DATE>', '<CLOSE>', '<VOL>']].astype('str')
    df_si['<DATE>'] = pd.to_datetime(df_si['<DATE>'], format='%Y-%m-%d')
    df_si['<CLOSE>'] = df_si['<CLOSE>'].astype('float')
    df_si['<VOL>'] = df_si['<VOL>'].astype('float')
    df_si = df_si.replace(0.0, np.nan)
    df_si.dropna(inplace=True)
    df_si.columns = ['Date', 'Close', 'Vol']

    df_si.to_csv(r'app\static\tables\si.csv')


def rvi():
    rvi_end_date = dt.datetime.today()
    rvi_start_date = rvi_end_date - dt.timedelta(days=90)
    rvi_start_date = rvi_start_date.strftime('%d.%m.%Y')

    end_day = dt.datetime.strftime(dt.datetime.date(rvi_end_date), format='%d')
    end_month = dt.datetime.strftime(dt.datetime.date(rvi_end_date), format='%m')
    end_year = dt.datetime.strftime(dt.datetime.date(rvi_end_date), format='%Y')

    rvi_source = 'http://export.finam.ru/RI.RVI_170804_171127.csv?market=91&em=420463&code=RI.RVI&apply=0&df=4&mf=7&yf=2017&from={0}&dt={0}&mt={1}&yt={2}&to={0}&p=8&f=RI.RVI_170804_171127&e=.csv&cn=RI.RVI&dtf=1&tmf=1&MSOR=0&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1'.format(
        end_day, end_month, end_year)
    df_rvi = pd.read_csv(rvi_source, delimiter=',')
    df_rvi = df_rvi[['<DATE>', '<CLOSE>']].astype('str')
    df_rvi['<DATE>'] = pd.to_datetime(df_rvi['<DATE>'], format='%Y-%m-%d')
    df_rvi['<CLOSE>'] = df_rvi['<CLOSE>'].astype('float')
    df_rvi = df_rvi.replace(0.0, np.nan)
    df_rvi.dropna(inplace=True)
    df_rvi.columns = ['Date', 'Close']

    df_rvi.to_csv(r'app\static\tables\rvi.csv')


def smile():
    url_smile = 'http://www.option.ru/analysis/option#smile'

    driver = webdriver.Firefox()
    driver.get(url_smile)
    time.sleep(2)
    select = Select(driver.find_element_by_css_selector('#smile_expiration'))
    select.options[-1].click()
    driver.find_element_by_xpath("//div[@id='divsmile']/table/tbody/tr/td[2]/a").click()
    time.sleep(2)
    html = driver.page_source
    time.sleep(2)
    driver.close()

    df_smile = pd.read_html(html)
    df_smile = df_smile[4]
    df_smile.iloc[2:, 1:3]
    df_smile = df_smile.iloc[2:, 1:3]
    df_smile.columns = ['Strike', 'IV']

    df_smile.to_csv(r'app\static\tables\smile.csv')