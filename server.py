import socket
import threading

# Starting the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 1000))  # Listen on all interfaces, port 80 (HTTP default)

server.listen()
print("Listening.......")

# Chat user data
clients = []
nicknames = []

# Broadcasting messages to all connected clients
def broadcast(message, client):
    for c in clients:
        if c != client:
            try:
                c.send(message)
            except:
                # Handle client removal
                index = clients.index(c)
                clients.remove(c)
                c.close()

                nickname = nicknames[index]
                broadcast(f'{nickname} left the chat'.encode('ascii'), server)
                nicknames.remove(nickname)
                break

# Handle messages from clients
def handle_message(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            # Handle client removal
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'), server)
            nicknames.remove(nickname)
            break

# Handling users joining
def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined the chat!".format(nickname).encode('ascii'), server)
        client.send('Connected to the chat server!'.encode('ascii'))

        thread = threading.Thread(target=handle_message, args=(client,))
        thread.start()

receive()
