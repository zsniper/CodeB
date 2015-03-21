import socket
import sys
    
from hello import *
from events import *
from event_loop import *

def run(*commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data="Goldfish" + " " + "fishgold" + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        file1 =""
        while rline:
            #print(rline.strip())
            file1 += rline.strip() + sfile.readline()
            rline = sfile.readline()
            
    finally:
        sock.close()
    return file1


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





