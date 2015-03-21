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
        dividend_rates[key] = sec[key]['dividend_ratio']

    #Initializing past values
    past_orders = {}
    tickers = clientpy2.securities().keys()
    for t in tickers:
            past_orders[t] = []

    #Queue for next stock
    next_ticker = Queue.Queue()
    for key in dividend_rates.keys():
        next_ticker.put(key)

    active_tickers = []
    active_tickers.append(next_ticker.get())
    active_tickers.append(next_ticker.get())
    active_tickers.append(next_ticker.get())
    active_tickers.append(next_ticker.get())

    persist = {}

    while True:        
        dividend_rates = update_dividends(dividend_rates);
        print dividend_rates
        order_npast = push_event(past_orders, tickers)

        persist['div_rates'] = dividend_rates
        # map(broker.on_broker_event, order_npast['process'])
        #map((lambda x: divhack.on_divhack_event(x, dividend_rates, active_tickers)), order_npast['process'])
        for event in order_npast['process']:
            persist = divhack.on_divhack_event(event, tickers, persist)

        past_orders = order_npast['hist']
        cycle_ticker(next_ticker, active_tickers)
        print 'tick'
        time.sleep(0.5)
    #sleep thread

def cycle_ticker(ticker_queue, active):
    sec = clientpy2.my_securities()
    for ticker in active:
    #for i in range(len(active)):
        if sec[ticker]['shares'] == 0:
            ticker_queue.put(ticker)
            active[active.index(ticker)] = ticker_queue.get()

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
            dividend_rates[key] = securities[key]['dividend_ratio']
    return dividend_rates