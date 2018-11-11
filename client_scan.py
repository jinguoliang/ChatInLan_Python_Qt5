from point_detector import *

SCAN_PORT = 9992
SCAN_RESPOND_PORT = 8889


class Waiter:
    def __init__(self):
        self.server_sock = udp_server(SCAN_PORT)

    def loop(self):
        while True:
            print("wait_receiving")
            s, address = self.server_sock.recvfrom(len(BROADCAST_DATA))
            print("DetectListener:", "receiver data = ", s)
            print(address)
            if s.decode(UTF_8) == BROADCAST_DATA:
                print("respond")
                self.server_sock.sendto(BROADCAST_RESPOND_DATA.encode(UTF_8), address)


class Scanner:
    def __init__(self):
        self.client_sock = udp_sock()
        self.client_sock.settimeout(3)
        self.client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def scan(self):
        self.client_sock.sendto(BROADCAST_DATA.encode(UTF_8), ("<broadcast>", SCAN_PORT))
        print("sendto")

        addresses = []
        s, address = self.waitResponse()

        while s == BROADCAST_RESPOND_DATA:
            addresses.append(address)
            s, address = self.waitResponse()
        print(addresses)
        return addresses

    def waitResponse(self):
        try:
            s, address = self.client_sock.recvfrom(len(BROADCAST_RESPOND_DATA))
            print(address)
        except Exception as e:
            print(e)
            s = "".encode()
            address = None
        finally:
            return s.decode(), address
