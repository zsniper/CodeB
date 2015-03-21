import clientpy2

def on_event(e):
    our_orders = get_our_orders(e.ticker, e.price)
    if e.type == ask:
        price = get_worth_price(e.ticker, e.price)
        if is_in_our_orders(e.ticker, our_orders):
            undercut_price = get_undercut_price(e.ticker, e.price)
            if undercut_price > 0:
                shares_to_sell = get_shares_to_sell(our_orders, e.ticker, e.price)
                ask(e.ticker, undercut_price, shares_to_sell)
                return True
        elif price > 0:
            shares_to_sell = get_shares_to_sell(our_orders, e.ticker, e.price)
            bid(e.ticker, price, shares_to_sell)
            new_sell_price = get_new_sell_price(our_orders, e.ticker, e.price)
            ask(e.ticker, new_sell_price, shares_to_sell)
            return True
    # if e.type == bid:
        # do later
    return True

def get_worth_price(ticker, price):
    return price + 0.01

def get_undercut_price(ticker, price):
    return price + 0.01

def get_shares_to_sell(our_orders, ticker, price):
    return our_orders.shares
