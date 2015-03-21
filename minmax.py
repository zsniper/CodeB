def min_sell(ticker):
        data = run("ORDERS " + ticker).split(" ")
        costs = []
        for i in range(len(data)-2):
            if data[i] == ("ASK") and data[i+1] == (ticker):
                costs.append(data[i+2])
        return min(costs)

def min_buy(ticker):
       data = run("ORDERS " + ticker).split(" ")
       costs = []
       for i in range(len(data)-2):
           if data[i] == ("BID") and data[i+1] == (ticker):
               costs.append(data[i+2])
       return max(costs)