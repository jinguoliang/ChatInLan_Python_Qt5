import socket

LISTENER_PORT = 1992

UTF_8 = "utf-8"

BROADCAST_DATA = "wahaha"


class PointDetector:
    """ 局域网端点探测器， 负责搜索局域网， 获取一个列表 """

    def get_all_point(self):
        return []

    def broadcast(self):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        a_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        a_socket.sendto(BROADCAST_DATA.encode(UTF_8), ("<broadcast>", LISTENER_PORT))
        a_socket.close()

    def listen(self):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        a_socket.bind(("", LISTENER_PORT))
        buf, address = a_socket.recvfrom(len(BROADCAST_DATA))
        a_socket.close()
        return buf.decode("utf-8"), address

