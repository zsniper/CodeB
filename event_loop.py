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

    while True:
        if rotation % 2 == 0:
            activetickers = tickers[0:numberoftickers/2]
        elif rotation % 2 == 1:
            activetickers = tickers[numberoftickers/2:-1]
        order_npast = push_event(past_orders, activetickers)

        for x in order_npast['process']:
            events.on_event(x)

        past_orders = order_npast['hist']
        print 'tick'
        time.sleep(0.1)
        rotation = (rotation + 1) % 2
    #sleep thread

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

