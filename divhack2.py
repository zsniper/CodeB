from clientpy2 import clientpy2
from random import randint

def on_divhack_event(e, tickers, persist):
    #print tickers
    if e['action'] == 'ASK' and e['ticker'] in tickers:
        #print e['ticker']

        #change current bids
        #print tickers
        #decrement_prices(persist) #actually increments lol
        
        #buy
        #if e['price'] < sell_price(e['ticker'], persist) and (1 + persist['div_rate'] - 0.015) >= 1:
        #if e['price'] < sell_price(e['ticker'], persist):
        if randint(0,3) == 1:
            cash = clientpy2.my_cash()
            clientpy2.bid(e['ticker'], e['price'], int(cash/e['price']/3))
            print "bid" + " " + e['ticker'] +" " + str(e['price']) +" " + str(int(cash/e['price']/3))
            #print "BID " + e['ticker'] + " " + e['price'] + " " + int(cash/e['price']/3)
            persist['bought_at'][e['ticker']] = e['price']

            my_sec = clientpy2.my_securities()
            clientpy2.ask(e['ticker'], sell_price(e['ticker'], persist), my_sec[e['ticker']]['shares'])
            print "ask" + " " + e['ticker'] +" " + str(sell_price(e['ticker'], persist)) +" " + str(my_sec[e['ticker']]['shares'])
            #print "ASK " + e['ticker'] + " " + sell_price(e['ticker'], persist) + " " + my_sec[e['ticker']]['shares']

    return persist

def inc_liquidate(persist, active):
    m_orders = clientpy2.my_orders()

    persist = liquidate(m_orders, persist) #when to give up
    for key in active:
        if persist[key]['liquidate']: #initialize
            clientpy2.bid(key, m_orders[key]['price'] - 0.01, m_orders[key]['shares'])
            print "bid" + " " + key + " " + str(m_orders[key]['price'] - 0.01) + " " + str(m_orders[key]['shares'])
    return persist

def liquidate(m_orders, persist):
    sum = 0
    for key in m_orders.keys():
        sum = sum + m_orders[key]['shares']

    for key in m_orders.keys():
        if m_orders[key]['shares'] / 4 > 0.5 or persist['div_rate'] < 1e-4:
            persist[key]['liquidate'] = True
            #clientpy2.bid(key, m_orders[key]['price'], m_orders[key]['shares'] - 0.03)
            #print "bid"
    return persist

def sell_price(ticker, persist):
    return persist['bought_at'][ticker] + 0.10
    #return persist['bought_at'][ticker] * (1 + persist['div_rate'][ticker] - 0.015)

#def decrement_prices(persist):
#    m_orders = clientpy2.my_orders()
#
#    for key in m_orders.keys():
#        clientpy2.bid(key, sell_price(key, persist), m_orders[key]['shares'])
#        print "bid"