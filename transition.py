import socket


class Server:
    def __init__(self):
        self.server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def listen(self):
        print("listen")
        self.server_sock.bind(("", 8832))
        print("binded")
        self.server_sock.listen()
        print("listened")

        while True:
            client_sock, address = self.server_sock.accept()
            print(address)
            data = client_sock.recv(1024).decode()
            print(data)

class Client:
    def __init__(self):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, address):
        print(address)
        self.client_sock.connect((address[0], 8832))
        self.client_sock.send("haha".encode())
