import time
import clientpy2
import events

def net_worth_compare(item):
    return item['net_worth']

def value(net_worth, ):
    a = min_sell(ticker)
    return net_worth/a

def event_loop():

    tickers = clientpy2.securities()
    sorted(tickers, key=net_worth_compare)

    max_ticker_value = 0
    max_ticker_name = ''
    min_sell_value = 0
    for ticker in tickers.keys():
        a = tickers.get(ticker).get('net_worth')
        b = min_sell(ticker)
        new_value = a/b
        if new_value > max_ticker_value:
            min_sell_value = b
            max_ticker_value = new_value
            max_ticker_name = ticker


    current_cash = clientpy2.my_cash()
    shares_bought1 = current_cash//min_sell_value
    clientpy2.bid(max_ticker_name, min_sell_value, shares_bought)

    while True:
        clientpy2.bid()


    min_sell()

    for ticker in tickers:



def event_loop():
    #event_queue = Queue.Queue
    past_orders = {}
    tickers = clientpy2.securities().keys()
    for t in tickers:
        past_orders[t] = []

    numberoftickers = len(tickers)
    rotation = 0
    activetickers = []

    liquidate = 1

    while True:
        if rotation % 2 == 0:
            activetickers = tickers[0:numberoftickers/2]
        elif rotation % 2 == 1:
            activetickers = tickers[numberoftickers/2:-1]
        order_npast = push_event(past_orders, activetickers)

        for x in order_npast['process']:
            x['liquidate'] = liquidate
            events.on_event(x)

        past_orders = order_npast['hist']
        print 'tick'
        # time.sleep(0.1)
        rotation = (rotation + 1) % 2
        liquidate = liquidate + 1
    #sleep thread

#returns list to process and past orders.
def push_event(past, tickers):
    process = []
    new_past = {}
    for ticker in tickers:



        orders = clientpy2.orders(ticker) #list of  dictionaries
        #rate = clientpy2.my_securities(ticker, 'dividend_ratio')
        new_past[ticker] = orders
        for order in orders:
            if ticker not in past.keys() or order not in past[ticker]:
                order['ticker'] = ticker
        #        order['rate'] = rate
                process.append(order)
    return {'process':process, 'hist':new_past}

