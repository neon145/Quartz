import socket
import threading

nickname = input("Choose your nickname: ")

host = '3.6.30.85'
port = 12440

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An Error occurred")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

receiveThread = threading.Thread(target=receive)
receiveThread.start()
writeThread = threading.Thread(target=write)
writeThread.start()
