import time
import clientpy2
import events

secs = {}

def net_worth_compare(item):
    return int(secs[item]['net_worth'])

def value_compare(item):
    return int(item['value'])

def event_loop():
    global secs
    try: 
        secs = clientpy2.securities()
        #print secs['HOG']['net_worth']
        tickers = secs.keys()

        # lst = []
        # for t in tickers:
        #     lst.append(int(secs[t]['net_worth']))

        # sorted(lst)


        # sorted(tickers, key=net_worth_compare)
        # print tickers

        max_ticker_value = 0
        max_ticker_name = ''
        min_sell_value = 0

        ticker_values = []
        for ticker in tickers:
            a = float(secs[ticker]['net_worth'])
            b = float(clientpy2.min_sell(ticker))
            new_value = a/b
            ticker_values.append({'ticker':ticker,'value':new_value})
            if new_value > max_ticker_value:
                min_sell_value = b
                max_ticker_value = new_value
                max_ticker_name = ticker

        print 'ticker_values1: ' + str(ticker_values)
        ticker_values = sorted(ticker_values, key=value_compare)[::-1]
        print 'ticker_values2: ' + str(ticker_values)


        current_cash = float(clientpy2.my_cash())
        shares_bought = current_cash//min_sell_value
        clientpy2.bid(max_ticker_name, min_sell_value, shares_bought)
        print 'bid: max_ticker_name: ' + str(max_ticker_name) + ' min_sell_value: ' + str(min_sell_value) + ' shares_bought: ' + str(shares_bought)

        threshold = 0.00075

        second_ticker_name = ''
        third_ticker_name = ''

        i = 0

        while True:
            max_ticker_name = ticker_values[i]['ticker']
            while clientpy2.my_securities(max_ticker_name, 'dividend_ratio') > threshold:
                second_ticker_name = ticker_values[(i+1)%len(tickers)]['ticker']
                min_sell_value = float(clientpy2.min_sell(second_ticker_name))

                current_cash = float(clientpy2.my_cash())
                shares_bought = current_cash//min_sell_value
                
                clientpy2.bid(second_ticker_name, min_sell_value, shares_bought)
                print 'bid: second_ticker_name: ' + str(second_ticker_name) + ' min_sell_value: ' + str(min_sell_value) + ' shares_bought: ' + str(shares_bought)
            
            sale_price = float(clientpy2.min_sell(max_ticker_name))
            we_have_left = int(clientpy2.my_securities(max_ticker_name, 'shares'))
            while we_have_left > 0:
                clientpy2.ask(max_ticker_name, sale_price, we_have_left)
                print 'ask: max_ticker_name: ' + str(max_ticker_name) + ' sale_price: ' + str(sale_price) + ' we_have_left: ' + str(we_have_left)
                we_have_left = int(clientpy2.my_securities(max_ticker_name, 'shares'))
                sale_price = sale_price - 0.01

            i = (i+1) % len(tickers)
    finally:
        clientpy2.closeSocket()




