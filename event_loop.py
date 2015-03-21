import time

def event_loop():
    #event_queue = Queue.Queue
    past_orders = {}
    tickers = securities.keys()
    while True:
        orders_npast = push_event(past_orders)
        map(on_event, order_npast['process'])
        past_orders = order_npast['hist']
        time.sleep(0.01)
    #sleep thread

#returns list to process and past orders.
def push_event(past, tickers):
    process = []
    new_past = {}
    for t in tickers:
        o = orders(t) #list of  dictionaries
        new_past[t] = o
        for i in o:
            if i not in past[t]:
                i['ticker'] = t
                process.append(i)
    return {'process':process, 'hist':new_past}

