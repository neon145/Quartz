# Socket used for communication
# Threading used for running multiple processes at once
import socket
import threading

# Connection data
host = 'quartz-apmy.onrender.com'
port = 10000

# Starting the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM connection ensures TCP connection
server.bind((host,port))
server.listen()

# Quartz User data
clients = []
nicknames = []

# Broadcasting messages to all connected clients
def broadcast (message):
    for client in clients:
        client.send(message)

# Handle messages from clients 
def handle_message (client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nickname[index]
            broadcast(f'{nickname.encode("ascii")} left')
            nicknames.remove(nickname)
            break

# Handling users joining
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle_message, args=(client,))
        thread.start()

receive()
