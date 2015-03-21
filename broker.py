import clientpy2

gthreshold = 0
gticker = 'TWTR'

def on_broker_event(e):
    our_orders = 0 #get_our_orders(e['ticker'], e['price'])
    if gticker == e['ticker']:
        threshold = get_threshold(e['price'])
        if e['action'] == 'ASK':
            print 'TWTR: price: ' + str(e['price'])
            if e['price'] < threshold:
                shares_to_sell = e['shares'] #get_shares_to_sell(our_orders, e['ticker'], e['price'])
                price = get_worth_price(e['ticker'], e['price'])
                clientpy2.bid(e['ticker'], price, shares_to_sell)

                # we want to sell all our shares, including the ones we had before
                shares_to_sell = shares_to_sell + get_our_shares(our_orders, e['ticker']);
                clientpy2.ask(e['ticker'], threshold, shares_to_sell);
                
                # update our shares

                print 'bidding: ' + str(e['ticker']) + ' price: ' + str(price) + ' shares_to_sell: ' + str(shares_to_sell) + '\n'
                print 'asking: ' + str(e['ticker']) + ' price: ' + str(threshold) + ' shares_to_sell: ' + str(shares_to_sell) + '\n'
                return True

            # if is_in_our_orders(e['ticker'], our_orders):
            #     undercut_price = get_undercut_price(e['ticker'], e['price'])
            #     if undercut_price > 0:
            #         shares_to_sell = get_shares_to_sell(our_orders, e['ticker'], e['price'])
            #         clientpy2.ask(e['ticker'], undercut_price, shares_to_sell)
            #         return True
        # if e.type == bid:
            # do later
    return False

def get_threshold(price):
    global gthreshold
    if gthreshold == 0:
        gthreshold = price # - 0.1
    return gthreshold

def get_worth_price(ticker, price):
    return price + 0.1

def get_undercut_price(ticker, price):
    return price + 0.1

def get_our_shares(our_orders, ticker):
    return 0 # TODO: check based on our shares, we want to sell all our shares

def is_in_our_orders(ticker, our_orders):
    print 'is_in_our_orders' + str(ticker) + '\n'
    for action in our_orders:
        if action['action'] == 'ASK':
            return True
    return False

def get_our_orders(ticker, price):
    print 'get_our_orders' + str(ticker) + '\n'
    return clientpy2.my_orders(ticker)