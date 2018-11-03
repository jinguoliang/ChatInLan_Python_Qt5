import threading
import time
import unittest

from point_detector import PointDetector, BROADCAST_DATA


class PointDetectorTest(unittest.TestCase):
    """ 探测端点 测试 """

    def setUp(self):
        self.detector = PointDetector()

    def testDetect(self):
        self.assertEqual([], self.detector.get_all_point())

    def testBroadcast(self):
        threading.Thread(target=self.broadcastThread).start()
        print("listening")
        msg, _ = self.detector.listen()
        print("received")
        self.assertEqual(BROADCAST_DATA, msg)

    def broadcastThread(self):
        time.sleep(5)
        self.detector.broadcast()
        print("broadcast")


if __name__ == '__main__':
    unittest.main()
