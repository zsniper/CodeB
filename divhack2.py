from clientpy2 import clientpy2

def on_divhack_event(e, rates, tickers, persist):
    if e['action'] == 'ASK' and e['ticker'] in tickers:
        #change current bids
        decrement_prices(persist)

        #buy
        if price < sell_price(e['ticker'], persist) and (1 + persist['div_rate'] - 0.015) >= 1:
            clientpy2.bid(e['ticker'], e['price'], int(clientpy2.my_cash()/e['price']/3))
            persist['bought_at'][e['ticker']] = e['price']

            my_sec = clientpy2.my_securities()
            clientpy2.ask(e['ticker'], sell_price(e['ticker'], persist), my_sec[e['ticker']]['shares'])

    return persist

def sell_price(ticker, persist):
    return persist['bought_at'][ticker] * (1 + persist['div_rate'] - 0.015)

def decrement_prices(persist):
    m_orders = clientpy2.my_orders()

    for key in m_orders.keys():
        clientpy2.bid(key, sell_price(key, persist), m_orders[key]['shares'])