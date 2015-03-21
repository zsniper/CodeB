import time
import clientpy2
import broker
import divhack2
import Queue


def event_loop2():
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

    persist = {}
    persist['bought_at'] = {}

    #Queue for next stock
    next_ticker = Queue.Queue()
    for key in dividend_rates.keys():
        next_ticker.put(key)
        persist['bought_at'][key] = 0
        persist[key] = {}
        persist[key]['liquidate'] = False 

    active_tickers = []
    active_tickers.append(next_ticker.get())
    active_tickers.append(next_ticker.get())
    active_tickers.append(next_ticker.get())
    active_tickers.append(next_ticker.get()) 

    while True:        
        sec = clientpy2.my_securities()

        dividend_rates = update_dividends(dividend_rates, sec);
        persist['div_rate'] = dividend_rates
        
        persist = cycle_ticker(next_ticker, active_tickers, persist, sec)


        for key in active_tickers:
            mini = {}
            min_val = 999999
            for ask in filter(lambda x: x['action'] == 'ASK', clientpy2.orders(key)):
                ask['ticker'] = key
                if ask['price'] < min_val:
                    mini = ask
            persist = divhack2.on_divhack_event(mini, active_tickers, persist)

        persist = divhack2.inc_liquidate(persist, active_tickers)
        
        print 'tick'

def cycle_ticker(ticker_queue, active, persist, sec):
    for ticker in active:
    #for i in range(len(active)):
        if sec[ticker]['shares'] == 0:
            ticker_queue.put(ticker)
            new_ticker = ticker_queue.get()
            active[active.index(ticker)] = new_ticker
            persist[new_ticker]['liquidate'] = False    
        return persist

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

def update_dividends(dividend_rates, securities):
    divs = securities.keys()
    for key in divs:
        if securities[key] != 0:
            dividend_rates[key] = securities[key]['dividend_ratio']
    return dividend_rates