import socket
import sys
    
from hello import *
from events import *
from event_loop import *

HOST = "codebb.cloudapp.net"
PORT = 17429
g_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
g_sock.connect((HOST, PORT))
g_sfile = g_sock.makefile()
data="Goldfish" + " " + "fishgold" + "\n"
g_sock.sendall(data)

def run(*commands):
    data = "\n".join(commands) + "\n"

    #try:
        

    g_sock.sendall(data)
    rline = g_sfile.readline()
    
    # finally:
    #     sock.close()
    return rline

def closeSocket():
    global g_sock
    g_sock.sendall("Goldfish" + " " + "fishgold" + "\nCLOSE_CONNECTION\n")
    g_sock.close()


#THE GIVEN FUNCTIONS
def my_cash():
    return float(run("MY_CASH").split()[1])
def my_securities(ticker=False, key = False):
    data = run("MY_SECURITIES").split()[1:]
    dic = {}
    for i in range(len(data)/3):
            dic[data[i*3]] = {'shares':int(data[i*3 +1]),'dividend_ratio':float(data[i*3 + 2])}
    if ticker:
        if key:
            return dic.get(ticker).get(key)
        return dic.get(ticker)
    return dic
def my_orders(ticker=False):
    data = run("MY_ORDERS").split()[1:]
    dic = {}
    for i in range(len(data)/4):
            dic[data[i*4 +1]] = {'action':data[i*4],'price':float(data[i*4 +2]),'shares':int(data[i*4 + 3])}
    if ticker:
        return dic.get(ticker)
    return dic
def securities(ticker=False, key = False):
    data = run("SECURITIES").split()[1:]
    dic = {}
    for i in range(len(data)/4):
            dic[data[i*4]] = {'net_worth':float(data[i*4 +1]),'dividend_ratio':float(data[i*4 + 2]), 'volatility':float(data[i*4 +3])}
    if ticker:
        if key:
            return dic.get(ticker).get(key)
        return dic.get(ticker)
    return dic

def orders(ticker):
    data = run("ORDERS " +ticker).split()[1:]
    dic = []
    for i in range(len(data)/4):
            dic.append({'action': data[i*4],'price':float(data[i*4 +2]),'shares':int(data[i*4 + 3])})
    return dic
def bid(ticker, price, shares):
    run("BID " + ticker + " " + str(price) + " " + str(shares))
def ask(ticker, price, shares):
    run("ASK " + ticker + " " + str(price) + " " + str(shares))
def clear_bid(ticker):
    run("CLEAR_BID " + ticker)
def clear_ask(ticker):
    run("CLEAR_ASK " + ticker)
def subscribe(user, password):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()
def unsubscribe():
    run("UNSUBSCRIBE")
def close_connection():
    run("CLOSE_CONNECTION")


def min_sell(ticker):
    data = run("ORDERS " + ticker).split(" ")
    costs = []
    for i in range(len(data)-2):
        if data[i] == ("ASK") and data[i+1] == (ticker):
            costs.append(data[i+2])
    return min(costs)

def max_buy(ticker):
   data = run("ORDERS " + ticker).split(" ")
   costs = []
   for i in range(len(data)-2):
       if data[i] == ("BID") and data[i+1] == (ticker):
           costs.append(data[i+2])
   return max(costs)



