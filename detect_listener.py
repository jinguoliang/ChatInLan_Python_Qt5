from threading import Thread

from point_detector import PointDetector, BROADCAST_DATA, BROADCAST_RESPOND_DATA

LISTENER_PORT = 8882

class DetectListener():
    def __init__(self):
        self.detector = PointDetector()
        self.socket = self.detector.create_udp_socket(8882, 100)
        print("created detect listening socket")

    """ 等待检查器，并给与回应 """
    def start(self):
        Thread(target=self.loop_wait).start()

    def loop_wait(self):
        while True:
            print("wait_receiving")
            s, address = self.detector.wait_receive(self.socket)
            print("DetectListener:", "receiver data = ", s)
            print(address)
            if s == BROADCAST_DATA:
                print("respond")
                self.detector.broadcast(BROADCAST_RESPOND_DATA, 1992)
