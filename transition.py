import socket


class Server:
    def __init__(self):
        self.server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def listen(self):
        self.server_sock.bind(("", 8832))
        self.server_sock.listen()

        while True:
            client_sock, address = self.server_sock.accept()
            data = client_sock.recv(32).decode()
            while data:
                print(data)
                data = client_sock.recv(1024).decode()


class Client:
    def __init__(self):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, address, path):
        data = self.getContent(path)
        self.client_sock.connect((address[0], 8832))
        self.client_sock.send(data)

    def getContent(self, path):
        f = open(path, 'rb')
        return f.read()
