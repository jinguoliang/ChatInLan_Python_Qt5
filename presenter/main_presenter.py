from threading import Thread

from PyQt5.QtWidgets import *

from net import netutils
from net.client_scan import *
from net.transition import Server, Client
from ui.main_ui import UIMain


class LanTrans(UIMain):

    def __init__(self):
        super().__init__()

        self.scanner = Scanner()
        self.waiter = Waiter()

        self.transition_server = Server()
        self.transition_server.signal.connect(self.show_message)

        self.show_my_ip()

        self.start_listening()

        self.send.clicked.connect(self.send_message)
        self.sendFile.clicked.connect(self.send_file_action)
        self.scan_button.clicked.connect(self.scan_action)

    def show_my_ip(self):
        self.my_ip_label.setText(netutils.get_my_lan_ip())

    def callback(self, data):
        print("callback = " + data)
        self.show_message(data)

    def start_listening(self):
        Thread(target=self.waiter.loop).start()
        self.transition_server.start()

    def scan_action(self):
        Thread(target=self.scan_point).start()

    def scan_point(self):
        self.addresses = self.scanner.scan()
        print(self.addresses)
        self.display_receiver(self.addresses)

    def send_message(self):
        text = self.inputbox.toPlainText()
        self.inputbox.clear()
        for address in self.addresses:
            Client(address).send_text(text)

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
        for address in self.addresses:
            SendFileThread(address, file_path).start()


class SendFileThread(Thread):
    def __init__(self, address, path):
        Thread.__init__(self, target=self.run)
        self.file_path = path
        self.address = address
        self.transition_client = Client(self.address)

    def run(self):
        self.transition_client.send_file(self.file_path)
