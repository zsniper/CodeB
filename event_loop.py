import time
import clientpy2
import broker
import divhack
import Queue


def event_loop():
    #finding original dividend rates.
    dividend_rates = {}
    sec = clientpy2.securities()
    for key in sec.keys():
        dividend_rates[key] = sec[key]['dividend_rates']

    #Initializing past values
    past_orders = {}
    tickers = clientpy2.securities().keys()
    for t in tickers:
            past_orders[t] = []

    #Queue for next stock
    next_ticker = Queue.Queue()
    for key in dividend_rates.keys():
        next_ticker.put(key)

    active_tickers = [].append(next_ticker.get()).append(next_ticker.get()).append(next_ticker.get()).append(next_ticker.get())

    while True:
        
        update_dividends(dividend_rates);
        order_npast = push_event(past_orders, tickers)

        map(broker.on_broker_event, order_npast['process'])
        map((lambda x: divhack.on_divhack_event(x, active)), order_past['process'])
        past_orders = order_npast['hist']
        cycle_ticker(ticker_queue, active)
        print 'tick'
        time.sleep(0.5)
    #sleep thread

def cycle_ticker(ticker_queue, active):
    sec = clientpy2.my_securities()
    for ticker in active:
    #for i in range(len(active)):
        if sec[ticker]['shares'] == 0:
            ticker_queue.put(ticker)
            active.index(ticker) = ticker_queue.get()

#returns list to process and past orders.
def push_event(past, tickers):
    process = []
    new_past = {}
    for t in tickers:
        o = clientpy2.orders(t) #list of  dictionaries
        new_past[t] = o
        for i in o:
            if i not in past[t]:
                i['ticker'] = t
                process.append(i)
    return {'process':process, 'hist':new_past}

def update_dividends(dividend_rates):
    securities = clientpy2.my_securities()
    divs = securities.keys()
    for key in divs:
        if securities[key] != 0:
            dividend_rates[key] = securities[key]['dividend_rates']
    return dividend_rates