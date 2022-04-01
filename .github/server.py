import select
import socket
import response

#  Defining variables to be used throughout the program
HEADER = 64
PORT = 5050
IP = socket.gethostbyname(socket.gethostname())  # Grabs the hosts local IP address
ADDR = (IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # This allows us to reconnect

server.bind(ADDR)
server.listen()
sockets_list = [server]
clients = {}


def receive_message(client):
    try:
        message_header = client.recv(HEADER)

        if not len(message_header):
            return False

        message_length = int(message_header.decode(FORMAT).strip())
        return {"header": message_header, "data": client.recv(message_length)}
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

            print(
                f"Accepted new connection from {client_address[0]}:{client_address[1]} "
                f"username: {user['data'].decode(FORMAT)}")

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode(FORMAT)}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            msg = message['data'].decode(FORMAT)
            username = user['data'].decode(FORMAT)

            print(f"Received message from {username}: {msg}")

            actions = [w for w in msg.split() if w.endswith('?')]
            # Makes a list of a word that ends with ?.

            a = [s.replace("?", "") for s in actions]
            # Removes the questionmark from the verb

            user = clients[notified_socket]

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                    #  Sending message from one client to all other clients connected

                if a:  # Checking if last word from client is a "?"
                    yoda, luke, obiwan, vader = "Yoda", "Luke", "Obi-Wan", "Vader"
                    bots = [yoda, luke, obiwan, vader]
                    #  Defining bots

                    yodaresponse = response.yoda(a[0])
                    lukeresponse = response.luke(a[0])
                    obiwanresponse = response.obiwan(a[0])
                    vaderresponse = response.vader(a[0])
                    #  Sending the last word as parameter to bot functions

                    botresponse = [yodaresponse, lukeresponse, obiwanresponse, vaderresponse]
                    #  Defining the bots responses

                    for responses, botname in zip(botresponse, bots):
                        botprint = botname + ": " + responses
                        print(botprint)  # Printing on server side,

                        botheader = f"{len(botname):<{HEADER}}".encode(FORMAT)
                        botdata = botname.encode(FORMAT)

                        messageheader = f"{len(responses):<{HEADER}}".encode(FORMAT)
                        botmessage = responses.encode(FORMAT)

                        client_socket.send(botheader + botdata + messageheader + botmessage)
                        #  Sending botresponses to all clients

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients
