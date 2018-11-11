from threading import Thread

from PyQt5.QtWidgets import *

from client_scan import *
from main_ui import UIMain
from point_detector import *
from transition import Server, Client


class LanTrans(UIMain):
    def __init__(self):
        super().__init__()

        self.DELIMITER = "    \neofeof    \neofeof"
        self.EOF = "    \neofeof"

        self.detector = PointDetector()

        self.scanner = Scanner()
        self.waiter = Waiter()

        self.transition_server = Server()

        self.startListening()

        self.send.clicked.connect(self.send_file_action)
        self.scan_button.clicked.connect(self.scanAction)

    def startListening(self):
        Thread(target=self.waiter.loop).start()
        Thread(target=self.transition_server.listen).start()

    def loadConfig(self):
        print("load configuration file")
        try:
            f = open("conf.ini", "r")
            for line in f:
                line = line.strip()
                if len(line) > 0 and line[0] != "#":
                    exec("self." + line)

        except FileNotFoundError as e:
            print("configure file not exist, using default")
            return

    def onGetPoint(self, address):
        print("onGetPoint: ", address)

    def scanAction(self):
        Thread(target=self.scanPoint).start()

    def scanPoint(self):
        self.address = self.scanner.scan()
        self.display_receiver(self.address)

    def display_receiver(self, receiver):
        self.receiver_list_widget.addItem(str(receiver))

    def send_file_action(self):

        file_name = self.select_file()
        if file_name is None:
            return

        print(file_name)

        self.send_file(file_name)

    def select_file(self):
        r = QFileDialog.getOpenFileName(self, "选择您想要传输的文件", "~/")
        return r[0]

    def send_file(self, file_path):
        pass
