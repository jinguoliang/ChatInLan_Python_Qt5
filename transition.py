import socket
from threading import Thread

BLOCK_SIZE = 1024

TRANSITION_SERVER_PORT = 8832


class Server:
    def __init__(self):
        self.server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def listen(self):
        self.server_sock.bind(("", TRANSITION_SERVER_PORT))
        self.server_sock.listen()

        while True:
            client_sock, address = self.server_sock.accept()
            self.receive_data_from_socket_in_another_thread(client_sock)

    def receive_data_from_socket_in_another_thread(self, client_sock):
        ReceiverThread(client_sock).start()


class ReceiverThread(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self.client_sock = sock

    def run(self):
        data = self.client_sock.recv(BLOCK_SIZE).decode()
        while data:
            print(data)
            data = self.client_sock.recv(BLOCK_SIZE).decode()


class Client:
    def __init__(self):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, address, path):
        data = read_content(path)
        self.client_sock.connect((address[0], TRANSITION_SERVER_PORT))
        self.client_sock.send(data)


def read_content(path):
        f = open(path, 'rb')
        return f.read()
