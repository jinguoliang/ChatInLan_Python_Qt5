import socket
from threading import Thread

from PyQt5.QtCore import QThread, pyqtSignal

BLOCK_SIZE = 1024

TRANSITION_SERVER_PORT = 8832


class Server(QThread):
    signal = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.server_sock.bind(("", TRANSITION_SERVER_PORT))
        self.server_sock.listen()

        while True:
            client_sock, address = self.server_sock.accept()
            self.receive_data_from_socket_in_another_thread(client_sock)

    def receive_data_from_socket_in_another_thread(self, client_sock):
        thread = ReceiverThread(client_sock)
        thread.callback = self.callback
        thread.start()

    def callback(self, data):
        self.signal.emit(str(data))


class ReceiverThread(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self.client_sock = sock
        self.callback = None

    def run(self):
        data = self.client_sock.recv(BLOCK_SIZE).decode()
        while data:
            print(data)
            self.callback(data)
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
