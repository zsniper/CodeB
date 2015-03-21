from clientpy2 import clientpy2
bought_at = {}
# tickers = clientpy2.securities().keys()
# for ticker in tickers:
#     bought_at[ticker]=0
def on_divhack_event(e, rates, tickers_3):

    our_orders = 0 #get_our_orders(e['ticker'], e['price'])
    
    #print 'hello?'

    if e['ticker'] not in bought_at.keys():
        bought_at[e['ticker']] = e['price']




    if e['action'] == 'ASK' and e['ticker'] in tickers_3:
        price = get_worth_price(e['ticker'], e['price'])
        modifier = 0.9
        # if is_in_our_orders(e['ticker'], our_orders):
        #     undercut_price = get_undercut_price(e['ticker'], e['price'])
        #     if undercut_price > 0:
        #         shares_to_sell = get_shares_to_sell(our_orders, e['ticker'], e['price'])
        #         clientpy2.ask(e['ticker'], undercut_price, shares_to_sell)
        #         return True
        new_sell_price = get_new_sell_price(our_orders, e['ticker'], e['price'], rates)
        print 'price: ' + str(price) + ' new_sell_price ' + str(new_sell_price)
        if price*modifier < new_sell_price:
            shares_to_sell = get_shares_to_sell(our_orders, e['ticker'],tickers_3, e['price'])
            clientpy2.bid(e['ticker'], price, shares_to_sell)
            bought_at[e['ticker']]=price
            clientpy2.ask(e['ticker'], new_sell_price, shares_to_sell)
            print 'bidding: ' + ' ticker: ' + str(e['ticker']) + ' price: ' + str(price) + ' shares_to_sell: ' + str(shares_to_sell) + '\n'
            print 'asking: ' + ' ticker: ' + str(e['ticker']) + ' price: ' + str(new_sell_price) + ' shares_to_sell: ' + str(shares_to_sell) + '\n'
            return True
    # if e.type == bid:
        # do later
    return False

def get_worth_price(ticker, price):
    return price + 0.05

def get_undercut_price(ticker, price):
    return price + 0.1

def get_shares_to_sell(our_orders, ticker,tickers_3, price):
    return int((3- tickers_3.index(ticker))*clientpy2.my_cash()/9.0)
    # return our_orders['shares']

def get_new_sell_price(our_orders, ticker, price, rates):
    modifier= 0.15
    rate = rates.get(ticker)
    return bought_at[ticker]*(1 + rate - modifier)
    
def is_in_our_orders(ticker, our_orders):
    print 'is_in_our_orders' + str(ticker) + '\n'
    for action in our_orders:
        if action['action'] == 'ASK':
            return True
    return False

def get_our_orders(ticker, price):
    print 'get_our_orders' + str(ticker) + '\n'
    return clientpy2.my_orders(ticker)

def decrement_prices(rates):
    m_orders = clientpy2.my_orders()

    for key in m_orders.keys():
        clientpy2.bid(key, get_new_sell_price(0, key, 0, rates), m_orders[key]['shares'])
