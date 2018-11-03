import socket
import sys
import traceback

from PyQt5 import QtCore
from qtpy import QtWidgets


class UdpClient(QtCore.QThread):
    updateState = QtCore.pyqtSignal(tuple)
    """此线程用于在局域网中发送广播信息, 通过接收者的返回信息得到接收者的IP地址"""

    def __init__(self):
        super(UdpClient, self).__init__()
        self.searchTimeout = 1000
        self.searchTimes = 10
        self.DELIMITER = "    \neofeof    \neofeof"
        self.UDPPort = 8888
        self.stringBufLen = 1024 * 8
        self.TCPPort = 65500
        self.EOF = "    \neofeof"
        print("inited")



    def run(self):
        print("start run")
        udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpClient.settimeout(self.searchTimeout)
        udpClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        msg = "Lantrans Desktop UDPCLIENT"  # 向局域网中广播自己的主机名
        msg += self.DELIMITER

        buf = None
        address = None

        print("sender", "start broadcasting")

        # 广播多次信息代码设置的是5次, 每次隔2秒
        for i in range(self.searchTimes, -1, -1):  # try trytimes to search
            try:
                # 广播信息
                udpClient.sendto(msg.encode("utf-8"), ("<broadcast>", self.UDPPort))  ##################send
                # self.udpClient.sendto(msg.encode("utf-8"), ("127.0.0.1", 8888))
            except OSError as e:
                self.updateState.emit(("message", "<b><font color='red'>ERROR:&nbsp;</font></b>" + str(e)))
                traceback.print_exc(file=sys.stdout)
                return
            print("send finish")
            try:
                # 得到接收方的回复信息
                buf, address = udpClient.recvfrom(
                    self.stringBufLen)  ################################################recv
                print("receive")
                if address is not None and buf is not None:
                    break
            except socket.timeout as e:
                print("sender", "timeout error, remain", i, "to try")
                traceback.print_exc(file=sys.stdout)

        if address is None:
            print("failed to search server")
        else:
            # 接收方将TCP使用的端口号发送过来
            strPort = buf.decode("utf-8")
            strPort = strPort[0: strPort.find(self.EOF)]
            tempPort = int(strPort)  # 将缓冲区的的端口号读成字符串在转化为整数
            self.TCPPort = tempPort  # 将端口号保存到UI线程的全局变量中

            ld = list(address)
            ld[1] = tempPort
            address = tuple(ld)
            print("sender", "get server address:", address)
        self.udpClient.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    client = UdpClient()
    client.start()
    sys.exit(app.exec_())

