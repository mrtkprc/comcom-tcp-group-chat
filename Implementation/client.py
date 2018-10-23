from socket import *
import threading
import time

class Client():
    def PrintMenu(self):
        1 == 1

    def __init__(self,serverName,serverPort):
        self.serverName = serverName
        self.serverPort = serverPort
        self.clientSocket = socket(AF_INET,SOCK_STREAM)
        self.clientSocket.connect((self.serverName,self.serverPort))
        IncomingFromServer(self.clientSocket).start()
        Listen2Client(self.clientSocket).start()


        #while True:
        #    1 == 1

class IncomingFromServer(threading.Thread):
    def __init__(self,clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket

    def run(self):
        while True:
            
            responseFromServer=self.clientSocket.recv(1024)
            incomingMessage = responseFromServer.decode("utf-8")
            print("\n"+incomingMessage)
            time.sleep(1)

class Listen2Client(threading.Thread):
    def __init__(self,clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket


    def run(self):
        while True:
            choice = input("Enter Your Message: ")
            self.clientSocket.send(choice.encode())
            

            

if __name__=="__main__":
    serverName="192.168.1.25"
    serverPort=12000
    Client(serverName,serverPort)    
