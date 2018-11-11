from point_detector import *

SCAN_PORT = 9992
SCAN_RESPOND_PORT = 8889


class Waiter:
    def __init__(self):
        self.server_sock = udp_server(SCAN_PORT)
        self.client_sock = udp_sock()

    def loop(self):
        while True:
            print("wait_receiving")
            s, address = self.server_sock.recvfrom(len(BROADCAST_DATA))
            print("DetectListener:", "receiver data = ", s)
            print(address)
            if s.decode(UTF_8) == BROADCAST_DATA:
                print("respond")
                self.client_sock.sendto(BROADCAST_RESPOND_DATA.encode(UTF_8), (address[0], SCAN_RESPOND_PORT))


class Scanner:
    def __init__(self):
        self.server_sock = udp_server(SCAN_RESPOND_PORT)
        self.client_sock = udp_sock()

    def scan(self):
        self.client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client_sock.sendto(BROADCAST_DATA.encode(UTF_8), ("<broadcast>", SCAN_PORT))
        s, address = self.server_sock.recvfrom(len(BROADCAST_RESPOND_DATA))
        if s.decode(UTF_8) == BROADCAST_RESPOND_DATA:
            return address
