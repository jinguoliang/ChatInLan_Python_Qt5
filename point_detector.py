import socket
import threading
import time

LISTENER_PORT = 1992

UTF_8 = "utf-8"

BROADCAST_DATA = "I'm sender, where is the receiver"


class PointDetector:
    """ 局域网端点探测器， 负责搜索局域网， 获取一个列表 """

    def __init__(self):
        self.callbacks = []

    def get_all_point(self, callback, is_instant):
        threading.Thread(target=self.listen_thread, args=(is_instant, )).start()
        time.sleep(1)
        self.callbacks.append(callback)
        self.broadcast(BROADCAST_DATA)

    def listen_thread(self, args):
        print("start listen")
        address = self.listen(BROADCAST_DATA, args)
        print("listen received")
        self.callbacks[0](address)
        self.callbacks.clear()

    def broadcast(self, msg):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        a_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        a_socket.sendto(msg.encode(UTF_8), ("<broadcast>", LISTENER_PORT))
        a_socket.close()

    def listen(self, msg, is_instant, callback=None):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        a_socket.bind(("", LISTENER_PORT))
        buf, address = a_socket.recvfrom(len(msg))
        print("received: " + buf.decode(UTF_8))
        result = []

        if not is_instant:
            if buf.decode(UTF_8) == msg:
                result.append(address[0])
                a_socket.close()
            return result

        while True:
            if buf.decode(UTF_8) == msg:
                callback(address[0])
            buf, address = a_socket.recvfrom(len(msg))



if __name__ == '__main__':
    PointDetector().broadcast("test")
