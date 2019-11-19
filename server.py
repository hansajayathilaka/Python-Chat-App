import socket, select

headerSize = 10
ip = '127.0.0.1'
port = 4444

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind((ip, port))
serverSocket.listen(5)

socketsList = [serverSocket]

clients = {}


def receiveMsg(clientSocket):
    try:
        msgHeader = clientSocket.recv(headerSize)

        if not len(msgHeader):
            return False

        msgLength = int(msgHeader.decode('utf-8').strip())


        return {'header': msgHeader, 'data': clientSocket.recv(msgLength)}

    except:
        return False


while True:
    readSockets, _, exceptionSockets = select.select(socketsList, [], socketsList)

    for notifiedSocket in readSockets:

        if notifiedSocket == serverSocket:
            clientSocket, clientAddress = serverSocket.accept()

            user = receiveMsg(clientSocket)
            if user == False:
                continue

            socketsList.append(clientSocket)
            clients[clientSocket] = user
            print(f'Accepted new Connection from {clientAddress[0]}:{clientAddress[1]}. User Name : {user["data"].decode("utf-8")}')
        else:
            message = receiveMsg(notifiedSocket)

            if message is False:
                print('')
                print(f'Closed Connection from {clients[notifiedSocket]["data"].decode("utf-8")}')
                socketsList.remove(notifiedSocket)
                del clients[notifiedSocket]
                continue

            user = clients[notifiedSocket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            for clientSocket in clients:
                if clientSocket != notifiedSocket:
                    clientSocket.send(user['header'] + user['data'] + message['header'] + message['data'])
    for notifiedSocket in exceptionSockets:
        socketsList.remove(notifiedSocket)
        del clients[notifiedSocket]
