import socket
import time

MAX_DATA_SIZE = 1024 * 10

LISTENER_PORT = 1992

UTF_8 = "utf-8"
TIMEOUT = 8
BROADCAST_DATA = "I'm sender, where is the receiver"
BROADCAST_RESPOND_DATA = "I'm receiver and I'm here"


class PointDetector:
    """ 局域网端点探测器， 负责搜索局域网， 获取一个列表 """

    def __init__(self):
        self.callbacks = []

    def get_all_point(self, callback, duration, port):
        self.broadcast(BROADCAST_DATA, port)
        self.listen(BROADCAST_RESPOND_DATA, duration, callback=callback)

    def listen_thread(self, args):
        print("start listen")
        address = self.listen(BROADCAST_DATA, args)
        print("listen received")
        self.callbacks[0](address)
        self.callbacks.clear()

    def broadcast(self, msg, port):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        a_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        a_socket.sendto(msg.encode(UTF_8), ("<broadcast>", port))
        a_socket.close()

    def wait_receive(self, sock):
        buf = "".encode(UTF_8)
        address = None
        try:
            buf, address = sock.recvfrom(MAX_DATA_SIZE)
        except Exception as e:
            print(e)
        return buf.decode(UTF_8), address

    def listen(self, msg, duration, callback=None):

        a_socket = self.create_udp_socket(LISTENER_PORT, TIMEOUT)

        s, address = self.wait_receive(a_socket)

        result = []

        if duration == 0:
            if s == msg:
                result.append(address[0])
            a_socket.close()
            return result

        start = time.time()

        while time.time() - start < duration:
            if s == msg:
                callback(address[0])
                break
            s, address = self.wait_receive(a_socket)

        a_socket.close()


def udp_broadcast(msg, port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    a_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    a_socket.sendto(msg.encode(UTF_8), ("<broadcast>", port))
    a_socket.close()


def udp_send(msg, address):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    a_socket.sendto(msg.encode(UTF_8), address)
    a_socket.close()


def udp_server(port):
    a_socket = udp_sock()
    a_socket.settimeout(10)
    a_socket.bind(("", port))
    return a_socket

def udp_sock():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

def udp_waitLoop():
    server_socket = udp_server(8882)
    while True:
        print("wait   _receiving")
        s, address = server_socket.recvfrom(len(BROADCAST_DATA))
        print("DetectListener:", "receiver data = ", s)
        print(address)
        if s.decode(UTF_8) == BROADCAST_DATA:
            print("respond")
            time.sleep(1)
            udp_send(BROADCAST_RESPOND_DATA, (address[0], 9992))

def udp_scan_client():
    udp_broadcast(BROADCAST_DATA, 8882)
    server = udp_server(9992)
    s, address = server.recvfrom(len(BROADCAST_RESPOND_DATA))
    server.close()
    if s.decode(UTF_8) == BROADCAST_RESPOND_DATA:
        return address


if __name__ == '__main__':
    PointDetector().broadcast(BROADCAST_RESPOND_DATA)
    PointDetector().broadcast("test")
