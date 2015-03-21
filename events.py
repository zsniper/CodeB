import clientpy2

def on_event(e):
    our_orders = 0 #get_our_orders(e['ticker'], e['price'])
    # if e['liquidate'] % 5 == 0:
    #     clientpy2.ask(e['ticker'], e['price']-0.05,5)
    #     print 'asking: ' + str(e['ticker']) + ' price: ' + str(e['price']) + ' shares_to_sell: ' + str(5) + '\n'
    if e['action'] == 'ASK':
        price = get_worth_price(e['ticker'], e['price'])
        # if is_in_our_orders(e['ticker'], our_orders):
        #     undercut_price = get_undercut_price(e['ticker'], e['price'])
        #     if undercut_price > 0:
        #         shares_to_sell = get_shares_to_sell(our_orders, e['ticker'], e['price'])
        #         clientpy2.ask(e['ticker'], undercut_price, shares_to_sell)
        #         return True
        if price > 0:
            shares_to_sell = get_shares_to_sell(our_orders, e['ticker'], e['price'])
            clientpy2.bid(e['ticker'], price, shares_to_sell)
            new_sell_price = get_new_sell_price(our_orders, e['ticker'], e['price']) #, e['rate'])
            clientpy2.ask(e['ticker'], new_sell_price, shares_to_sell)
            print 'bidding: ' + str(e['ticker']) + ' price: ' + str(price) + ' shares_to_sell: ' + str(shares_to_sell) + '\n'
            print 'asking: ' + str(e['ticker']) + ' price: ' + str(new_sell_price) + ' shares_to_sell: ' + str(shares_to_sell) + '\n'
            return True
    # if e.type == bid:
        # do later
    return False

def get_worth_price(ticker, price):
    return price + 0.02

def get_shares_to_sell(our_orders, ticker, price):
    return 5
    # return our_orders['shares']

def get_new_sell_price(our_orders, ticker, price): #, rate):
    return price + 0.05 #(1 + rate) # + 0.15) # + 0.05

def is_in_our_orders(ticker, our_orders):
    print 'is_in_our_orders' + str(ticker) + '\n'
    for action in our_orders:
        if action['action'] == 'ASK':
            return True
    return False

def get_our_orders(ticker, price):
    print 'get_our_orders' + str(ticker) + '\n'
    return clientpy2.my_orders(ticker)
