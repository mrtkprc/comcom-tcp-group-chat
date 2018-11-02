from socket import *
import threading
import time

class Client():
    def __init__(self,serverName,serverPort):
        self.nickname = input("Enter your nickname: ")
        self.serverName = serverName
        self.serverPort = serverPort
        try:
            self.clientSocket = socket(AF_INET,SOCK_STREAM)
        except:
            print("Socket could not be opened.")
            return    

        try:
            self.clientSocket.connect((self.serverName,self.serverPort))
        except:
            print("Socket could not connect to server. Please, make sure whether server is working")
            return    

        self.clientSocket.send(("<!NEW_USER!>:"+self.nickname).encode())
        time.sleep(1)
        IncomingFromServer(self.clientSocket).start()
        Send2Others(self.clientSocket,self.nickname).start()
        

class IncomingFromServer(threading.Thread):
    def __init__(self,clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket

    def run(self):
        while True:
            incomingMessage = ""
            try:
                responseFromServer=self.clientSocket.recv(1024)
                incomingMessage = responseFromServer.decode("utf-8")
            except ConnectionResetError:
                time.sleep(1)
                return
            except:
                print("An error occured in receiving message")    
            
            print("\n"+incomingMessage,end="")
            time.sleep(1)

class Send2Others(threading.Thread):
    def __init__(self,clientSocket,nickname):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.nickname = nickname

    def run(self):
        while True:
            message = input("[You]: ")
            try:
                self.clientSocket.send(message.encode())
            except ConnectionResetError:
                time.sleep(1)
                return
            except:
                print("An error occured in sending message")    
                        

if __name__=="__main__":
    serverName="localhost"
    serverPort=12000
    Client(serverName,serverPort)    
