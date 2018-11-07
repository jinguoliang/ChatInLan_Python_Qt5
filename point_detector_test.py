import threading
import time
import unittest

from point_detector import PointDetector, BROADCAST_DATA


class PointDetectorTest(unittest.TestCase):
    """ 探测端点 测试 """

    def setUp(self):
        self.detector = PointDetector()
        self.result = None

    def testDetect(self):
        lock = threading.Lock()
        lock.acquire()

        def callback(x):
            self.result = x
            lock.release()

        self.detector.get_all_point(callback, False)
        lock.acquire()
        self.assertEqual(["192.168.199.118"], self.result)

    def testBroadcast(self):
        threading.Thread(target=self.broadcastThread).start()
        print("listening")
        address = self.detector.listen("test", False)
        print("received")
        self.assertEqual(["192.168.199.118"], address)

    def testListen_Instant(self):
        def callback(address):
            print(address)

        print("Please broadcast message")
        self.detector.listen("test", True, callback=callback)

    def broadcastThread(self):
        time.sleep(2)
        self.detector.broadcast("test")
        print("broadcast")


if __name__ == '__main__':
    unittest.main()