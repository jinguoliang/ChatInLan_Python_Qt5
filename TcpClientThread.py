import socket
import sys
import time
import traceback
from os import path

from PyQt5 import QtCore


class TcpClientThread(QtCore.QThread):
    """docstring for tcpClientThread"""
    updateState = QtCore.pyqtSignal(tuple)

    def __init__(self, caller):
        super(TcpClientThread, self).__init__()
        self.caller = caller

    def run(self):
        self.tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("sender", "Constructing TCP connection to receiver:",
              self.caller.receiverAddr)  # =========================================
        self.updateState.emit(
            ("message", "<b><font color='blue'>MESSAGE:&nbsp;</font></b>正在连接到接收者:" + str(self.caller.receiverAddr)))

        for i in range(self.caller.connectTimes, -1, -1):
            try:
                # 先接收方发起TCP连接
                self.tcpClient.connect(self.caller.receiverAddr)
                break
            except socket.error:
                self.updateState.emit(
                    ("message", "<b><font color='red'>ERROR:&nbsp;</font></b>TCP连接失败, 尝试剩下的" + str(i) + "次"))
                traceback.print_exc(file=sys.stdout)
                if i == 0:
                    return
                time.sleep(self.caller.connectTimeout)

        # 使用过一次端口号之后要对其减一, 防止下次使用地址不可用
        self.caller.TCPPort -= 1

        # 构建文件描述信息
        msg = ""
        for f in self.caller.files:
            msg += path.basename(f) + self.caller.NAME_LEN_SPT + str(path.getsize(f)) + self.caller.FILES_SPT

        msg += self.caller.DELIMITER
        print("send file desc:", msg)
        # 发送文件描述
        self.tcpClient.sendall(msg.encode("utf-8"))

        print("等待接收确认信息")
        # 充值msg保存接收方(server)的回复信息
        msg = self.tcpClient.recv(self.caller.stringBufLen)

        print("成功建立连接")
        self.updateState.emit(("message", "<b><font color='green'>MESSAGE:&nbsp;</font></b>成功建立连接"))
        if len(msg):  # 如果信息不为空, 说明server已经准备好接收文件了
            self.caller.hasConnectedToRecver = True
            self.caller.clientTcpConn = self.tcpClient  # 将次连接保存到UI, 等用户点start开始文件传输
            print("sender",
                  "receiver is ready to receiv files")  # ======================================================