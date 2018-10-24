from socket import *
import threading
import time
m_addrList = []
m_clientList = []
m_userList = []
class ThreadedServer():
    def __init__(self,serverPort):
        try:
            serverSocket = socket(AF_INET,SOCK_STREAM)
        except:
            print("Server couldn't start to work")
            return                

        try:    
            serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        except:
            print("An error occured while socket settings was changing")                
            return

        try:    
            serverSocket.bind(('',serverPort))
        except:
            print("Server couldn't be bound")                    
            return

        try:    
            serverSocket.listen(45)
        except:
            print("Server couldn't start to listen clients")                    
            return

        count = 0
        print("Server started.")
        while True:
            client,addr=serverSocket.accept()
            count += 1
            m_clientList.append(client)
            m_addrList.append(addr)
            print("Current Client Count: ", count)
            ClientWithThread(count,client,addr).start()
        
class ClientWithThread (threading.Thread):
    def __init__(self,threadID,client,addr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.client = client
        self.addr = addr
        
    def run(self):
        while True:
            try:
                message = self.client.recv(1024)
                splitted_message = message.decode("utf-8").split(":")
                if len(splitted_message) == 2 and splitted_message[0] == "<!NEW_USER!>":
                    self.nickname = splitted_message[1]
                    m_userList.append(self.nickname)
                else:
                    SendMessageEveryone(self.addr[1],message,self.nickname)

            except ConnectionResetError:
                return
            except Exception as ex:
                print("An error occured in receiving message")
                print(type(ex).__name__)
            
def SendMessageEveryone(portID,message,senderNickName):
    for i,addr in enumerate(m_addrList):
        if(addr[1] != portID):
            try:
                sendingMessage = message.decode("utf-8")
                sendingMessage = senderNickName+": "+sendingMessage
                m_clientList[i].send(sendingMessage.encode())
            except ConnectionResetError:
                time.sleep(1)
                return
            except Exception as ex:
                print("An error occured in sending message")    
                print (type(ex).__name__)


if __name__=="__main__":
    serverPort=12000
    ThreadedServer(serverPort)

