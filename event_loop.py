import time
import clientpy2
import events

def net_worth_compare(item):
    return item['net_worth']

def value_compare(item):
    return item['value']


def value(net_worth, ):
    a = min_sell(ticker)
    return net_worth/a

def event_loop():

    tickers = clientpy2.securities()
    sorted(tickers, key=net_worth_compare)

    max_ticker_value = 0
    max_ticker_name = ''
    min_sell_value = 0

    ticker_values = []
    for ticker in tickers.keys():
        a = tickers.get(ticker).get('net_worth')
        b = min_sell(ticker)
        new_value = a/b
        ticker_values.append({'ticker':ticker,'value':new_value})
        if new_value > max_ticker_value:
            min_sell_value = b
            max_ticker_value = new_value
            max_ticker_name = ticker

    sorted(ticker_values, key=value_compare)


    current_cash = clientpy2.my_cash()
    shares_bought = current_cash//min_sell_value
    clientpy2.bid(max_ticker_name, min_sell_value, shares_bought)

    threshold = 0.0001

    second_ticker_name = ''
    third_ticker_name = ''

    i = 0

    while True:
        max_ticker_name = ticker_values[i]['ticker']
        while clientpy2.my_securities(max_ticker_name, 'dividend_ratio') > threshold:
            second_ticker_name = ticker_values[(i+1)%len(tickers)]['ticker']
            min_sell_value = clientpy2.min_sell(second_ticker_name)

            current_cash = clientpy2.my_cash()
            shares_bought = current_cash//min_sell_value
            
            clientpy2.bid(second_ticker_name, min_sell_value, shares_bought)
        
        sale_price = min_sell(max_ticker_name)
        we_have_left = clientpy2.my_securities(max_ticker_name, 'shares')
        while we_have_left > 0:
            clientpy2.ask(max_ticker_name, sale_price, we_have_left)
            we_have_left = clientpy2.my_securities(max_ticker_name, 'shares')
            sale_price = sale_price - 0.01

        i = (i+1) % len(tickers)




