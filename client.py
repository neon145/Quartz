import socket
import threading

nickname = input("Choose your nickname: ")

host = 'quartz-apmy.onrender.com'
port = 7075

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

def recieve ():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An Error occured")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

recieveThread = threading.Thread(target = recieve)
recieveThread.start()
writeThread = threading.Thread(target = write)
writeThread.start()
