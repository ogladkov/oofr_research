from app import app
from flask import render_template, url_for
import time
import get_parsed

import mm, inflation, trade_balance, pmi, invest, metals, \
    brent, coins, crb, fx, rates, auction_days, auction_1w, \
    idx_mmvb, msci, epfr, gspread, gcurve, rts, si, smile, rvi, \
    volat30, volat60, debt_comp, gold_copper, roe_pbv, roe_evebitda


def read_file(text_file):
    file = open(text_file, 'r')
    return file.read()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/macro')
def macro():
    mm
    inflation
    trade_balance
    pmi
    invest

    # Читаем текстовый файл
    text_file = 'macro.txt'
    text_file = r'app/static/text/macro.txt'
    file = read_file(text_file)

    return render_template('macro.html', file=file)


@app.route('/parse_macro')
def parse_macro():
    get_parsed.m2()
    get_parsed.rests()
    get_parsed.inflation()
    get_parsed.trade_balance()
    get_parsed.pmi()
    return render_template('macro.html')


@app.route('/commodities')
def commodities():
    metals
    brent
    coins
    crb

    import gen_commodities_table
    gen_commodities_table

    # Читаем текстовый файл
    text_file = 'commod.txt'
    text_file = r'app/static/text/commodities.txt'
    file = read_file(text_file)

    return render_template('commodities.html', file=file)


@app.route('/parse_commod')
def parse_commod():
    # get_parsed.metals()
    get_parsed.brent()
    # get_parsed.coins()
    get_parsed.crb()
    return render_template('commodities.html')


@app.route('/commodities_table')
def commodities_table():
    gen_commodities_table
    render_template(url_for('index'))


@app.route('/currency_1')
def currency_1():
    print('Test Currency')
    fx
    rates

    import gen_curr_table
    # gen_curr_table
    return render_template('currency_1.html')


@app.route('/currency_2')
def currency_2():
    auction_days
    auction_1w

    # Читаем текстовый файл
    text_file = r'app/static/text/currency.txt'
    file = read_file(text_file)
    return render_template('currency_2.html', file=file)


@app.route('/parse_curr')
def parse_curr():
    get_parsed.usdrub()
    get_parsed.eurrub()
    get_parsed.eurusd()
    get_parsed.fed()
    get_parsed.cbr_rate()
    get_parsed.dep_auctions()
    get_parsed.ruonia()
    get_parsed.mosprime()
    get_parsed.repo_on()
    get_parsed.repo_1w()
    return render_template('currency_1.html')


@app.route('/stocks_1')
def stocks_1():
    idx_mmvb
    msci
    epfr
    import gen_stocks_table
    gen_stocks_table

    # Читаем текстовый файл
    text_file = r'app/static/text/stocks.txt'
    file = read_file(text_file)
    return render_template('stocks_1.html', file=file)


@app.route('/stocks_2')
def stocks_2():
    # import gen_mmvb_table
    import gen_portfolio_table, gen_fc_table
    # gen_mmvb_table
    gen_portfolio_table
    gen_fc_table
    roe_pbv
    roe_evebitda
    return render_template('stocks_2.html')

@app.route('/stocks_3')
def stocks_3():
    import gen_portfolio_table
    gen_portfolio_table


@app.route('/parse_stocks')
def parse_stocks():
    get_parsed.idx_mmvb()
    time.sleep(1)
    get_parsed.mmvb10()
    get_parsed.msci()
    get_parsed.sp()
    get_parsed.djia()
    get_parsed.dax()
    get_parsed.vix()
    return render_template('stocks_1.html')


@app.route('/debts')
def debts():
    # gcurve
    # gspread
    debt_comp
    gold_copper

    # Читаем текстовый файл
    text_file = r'app/static/text/debts.txt'
    file = read_file(text_file)
    return render_template('debts.html', file=file)


@app.route('/parse_debts')
def parse_debts():
    get_parsed.gspread()
    # get_parsed.gcurve()
    # get_parsed.mibor()
    # get_parsed.sp()
    # get_parsed.div_sp()
    # get_parsed.tnx()
    # get_parsed.ofz10()
    # get_parsed.mcx10()
    # get_parsed.fed3m()
    # get_parsed.gold_copper()
    return render_template('debts.html')


@app.route('/spfi')
def spfi():
    rts
    si
    smile
    rvi
    volat30
    volat60
    return render_template('spfi.html')


@app.route('/parse_spfi')
def parse_spfi():
    get_parsed.rts()
    get_parsed.si()
    get_parsed.rvi()
    get_parsed.smile()
    return render_template('spfi.html')


@app.route('/compile')
def compile():
    # Read macro
    text_macro_file = r'app/static/text/macro.txt'
    text_macro_file = read_file(text_macro_file)

    # Read commodities
    text_commodities_file = r'app/static/text/commodities.txt'
    text_commodities_file = read_file(text_commodities_file)

    # Read currency
    text_currency_file = r'app/static/text/currency.txt'
    text_currency_file = read_file(text_currency_file)

    # Read stocks
    text_stocks_file = r'app/static/text/stocks.txt'
    text_stocks_file = read_file(text_stocks_file)

    # Read debts
    text_debts_file = r'app/static/text/debts.txt'
    text_debts_file = read_file(text_debts_file)

    return render_template('compile.html', text_macro_file=text_macro_file,
                           text_commodities_file=text_commodities_file,
                           text_stocks_file=text_stocks_file,
                           text_currency_file=text_currency_file,
                           text_debts_file=text_debts_file
                           )