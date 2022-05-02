import socket
import sys
import errno

# These are the variables that are used in the program.
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)

# This is the code that is used to connect to the server.
my_username = input("Username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ADDR))
client.setblocking(False)  # Receive functionality won't be blocking

username = my_username.encode(FORMAT)
username_header = f"{len(username):<{HEADER}}".encode(FORMAT)
client.send(username_header + username)


print("You are connected, press q and hit enter to quit")


while True:
    message = input(f"{my_username} > ")

    # This is the code that is used to close the connection with the server.
    if message == "q":
        print("Closing connection with server")
        client.close()
        break

    # This is the code that is used to send the message to the server.
    if message:
        message = message.encode(FORMAT)
        message_header = f"{len(message):<{HEADER}}".encode(FORMAT)
        client.send(message_header + message)

    # This is the code that is used to receive the message from the server.
    try:
        while True:
            # receive messages
            username_header = client.recv(HEADER)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()

            username_length = int(username_header.decode(FORMAT).strip())
            username = client.recv(username_length).decode(FORMAT)

            message_header = client.recv(HEADER)
            message_length = int(message_header.decode(FORMAT).strip())
            message = client.recv(message_length).decode(FORMAT)

            print(f"{username} > {message}")


    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()
        pass
