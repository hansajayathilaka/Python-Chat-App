import socket, select, errno, sys
import tkinter as tk


class Client():
    def __init__(self, ip, port, myUserName):
        # global headerSize
        self.headerSize = 10
        
        # ip = '127.0.0.1'
        # port = 4444
        self.ip = ip
        self.port = port

        self.myUserName = myUserName # input('Enter your Username : ')
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((ip, port))
        self.clientSocket.setblocking(False)

        self.userName = self.myUserName.encode('utf-8')
        self.userNameHeader = f'{len(self.userName):<{self.headerSize}}'.encode('utf-8')
        self.clientSocket.send(bytes(self.userNameHeader + self.userName))
        
    def send(self, message):
        message = message.encode('utf-8')
        messageHeader = f'{len(message):<{self.headerSize}}'.encode('utf-8')
        self.clientSocket.send(messageHeader + message)
        
    def receive(self):
        try:
            while True:
                # receive
                userNameHeader = self.clientSocket.recv(self.headerSize)
                if not len(userNameHeader):
                    print('Connection is closed by the server')
                    #sys.exit()
                userNameHeader = int(userNameHeader.decode('utf-8').strip())
                userName = self.clientSocket.recv(userNameHeader).decode('utf-8')

                messageHeader = int(self.clientSocket.recv(self.headerSize).decode('utf-8').strip())
                message = self.clientSocket.recv(messageHeader).decode('utf-8')

                return userName, message

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading Error', str(e))
                #sys.exit()
                return None
                
        except Exception as e:
            print('General Error', str(e))
            #sys.exit()
            return None

if __name__ == '__main__':
    client = Client('127.0.0.1', 4444, 'qwe')
    while True:
        client.send(input())
        while True:
            msg = client.receive()
            if msg:
                print(msg[0] + ' >> ' + msg[1])
            else:
                break




