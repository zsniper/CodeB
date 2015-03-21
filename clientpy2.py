import socket
import sys
    
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
        
def ticker(key):
    data=run("SECURITIES")
    stock = data[data.find(key)+len(key):]
    stock = " ".join(stock.split()[0:3])
    return stock

