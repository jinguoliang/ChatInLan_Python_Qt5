import socket

SCAN_PORT = 9992

UTF_8 = "utf-8"

BROADCAST_DATA = "I'm sender, where is the receiver"
BROADCAST_RESPOND_DATA = "I'm receiver and I'm here"


def udp_server(port):
    a_socket = udp_sock()
    a_socket.settimeout(5)
    a_socket.bind(("", port))
    return a_socket


def udp_sock():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


class Waiter:
    def __init__(self):
        self.server_sock = udp_server(SCAN_PORT)

    def loop(self):
        while True:
            try:
                print("wait_receiving")
                s, address = self.server_sock.recvfrom(len(BROADCAST_DATA))
                print(address)
            except Exception as e:
                print(e)
                continue

            if s.decode(UTF_8) == BROADCAST_DATA:
                print("respond...")
                self.server_sock.sendto(BROADCAST_RESPOND_DATA.encode(UTF_8), address)
                print("responded")


class Scanner:
    def __init__(self):
        self.client_sock = udp_sock()
        self.client_sock.settimeout(2)
        self.client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def scan(self):
        self.client_sock.sendto(BROADCAST_DATA.encode(UTF_8), ("<broadcast>", SCAN_PORT))

        addresses = []
        s, address = self.wait_response()

        while s == BROADCAST_RESPOND_DATA:
            addresses.append(address)
            s, address = self.wait_response()

        return addresses

    def wait_response(self):
        try:
            s, address = self.client_sock.recvfrom(len(BROADCAST_RESPOND_DATA))
            print(address)
        except Exception as e:
            print(e)
            s = "".encode()
            address = None
        finally:
            return s.decode(), address
