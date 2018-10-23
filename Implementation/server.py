from socket import *
import threading
import time
m_addrList = []
m_clientList = []
class ThreadedServer():
    def __init__(self,serverPort):
        
        serverSocket = socket(AF_INET,SOCK_STREAM)            
        serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serverSocket.bind(('',serverPort))
        serverSocket.listen(45)
        count = 0
        print("Count ", count)
        while True:
            client,addr=serverSocket.accept()
            count += 1
            m_clientList.append(client)
            m_addrList.append(addr)
            print("Count ", count)
            ClientWithThread(count,client,addr).start()
        
class ClientWithThread (threading.Thread):
    def __init__(self,threadID,client,addr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.client = client
        self.addr = addr
    def run(self):
        while True:
            message = self.client.recv(1024)
            SendMessageEveryone(self.addr[1],message)
            
def SendMessageEveryone(portID,message):
    for i,addr in enumerate(m_addrList):
        if(addr[1] != portID):
            sendingMessage = message.decode("utf-8")
            sendingMessage = "Terminal "+str(i)+": "+sendingMessage
            m_clientList[i].send(sendingMessage.encode())
    print("")        


if __name__=="__main__":
    serverPort=12000
    ThreadedServer(serverPort)

