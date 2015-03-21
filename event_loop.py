import time
import clientpy2
import events

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

    try: 
        while True:
            print 'hi'
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
    finally:
        clientpy2.closeSocket()


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

