import select
import socket
import response

HEADER = 64
PORT = 5050
IP = socket.gethostbyname(socket.gethostname()) #Grabs the hosts local IP address
ADDR = (IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #This allows us to reconnect

server.bind(ADDR)
#test
server.listen()

sockets_list = [server]

clients = {}

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER)

        if not len(message_header):
            return false

        message_length = int(message_header.decode(FORMAT).strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server:
            client, client_address = server.accept()

            user = receive_message(client)
            if user is False:
                continue

            sockets_list.append(client)

            clients[client] = user

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode(FORMAT)}")

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode(FORMAT)}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]

            print(f"Received message from {user['data'].decode(FORMAT)}: {message['data'].decode(FORMAT)}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients
