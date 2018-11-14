import socket
import sys
import time
import traceback
from os import path

from PyQt5 import QtCore


class SendFileThread(QtCore.QThread):
    """通过已经建立好的TCP连接, 读取本独文件通过IO流写入到网络"""
    updateState = QtCore.pyqtSignal(tuple)
    updateRate = QtCore.pyqtSignal(tuple)

    def __init__(self, caller):
        super(SendFileThread, self).__init__()
        self.caller = caller

    def setFile(self, files):
        self.files = files

    def run(self):
        '''send single file to receiver'''
        allFinished = True
        for i in range(len(self.files)):  # 发送列表中的每一个文件
            try:
                filepath = self.files[i]
                fileSize = path.getsize(filepath)

                print("sending:", filepath, "length:", fileSize)
                self.updateState.emit(("message",
                                       "<b><font color='blue'>MESSAGE:&nbsp;</font></b><font color='blue'>正在发送 " + str(
                                           path.basename(filepath)) + "</font>"))
                f = open(filepath, "rb")

                start = time.time()
                staticStart = start  # used to calculate total time comsumpton
                cnt = hasSend = speed = 0

                # 构建当前文件的文件描述
                strmsg = path.basename(filepath) + self.caller.NAME_LEN_SPT + str(fileSize) + self.caller.DELIMITER

                # send what is going to send
                print("sender", "send ack")
                self.caller.clientTcpConn.sendall(strmsg.encode("utf-8"))  # 发送文件描述
                # recv acknowledgement, actually this is used to sperate 2 files' bytes stream between two file

                fuck = self.caller.clientTcpConn.recv(self.caller.stringBufLen)  # 接收文件描述
                print("reciver reply", fuck.decode("utf-8").strip())

                if fileSize == 0:
                    self.updateRate.emit((i, 100, 888))
                    continue

                while True:  # 死循环开始文件传输
                    content = f.read(self.caller.fileIOBufLen)
                    if content is None:  # 如果文件传输完成, 或者异常发生
                        break

                    self.caller.clientTcpConn.sendall(content)
                    end = time.time()

                    cnt += len(content)  # use to calculate speed
                    hasSend += len(content)  # used for rate

                    if hasSend == fileSize:  # finished send this file #文件完成发送, 大小一致
                        self.updateRate.emit((i, 100, -1))
                        break

                    self.updateRate.emit((i, int(hasSend / fileSize * 100), speed))

                    if end - start >= 0.5:  # 每隔0.5秒更新一次速度
                        speed = (cnt / 1024) / (end - start)
                        self.updateRate.emit((i, int(hasSend / fileSize * 100), speed))
                        # print("send finish:", hasSend, fileSize, int(hasSend / fileSize * 100), "speed", speed)
                        start = end
                        cnt = 0

                # receive acknowledgement message #接收server的确认信息
                ack = self.caller.clientTcpConn.recv(self.caller.stringBufLen)
                ack = ack.decode("utf-8")
                ack = ack[0: ack.find(self.caller.EOF)]
                if int(ack) == fileSize:
                    timeDiff = end - staticStart
                    if timeDiff == 0.0:
                        timeDiff = 0.00001;

                    timecomsumption = int(timeDiff * 10) / 10
                    speed = (fileSize / 1024) / timeDiff
                    strspeed = ""
                    if speed < 1024:
                        strspeed = str(int(speed * 100) / 100) + "KB/s"
                    else:
                        strspeed = str(int(speed / 1024 * 100) / 100) + "MB/S"
                    self.updateState.emit(("message",
                                           "<b><font color='green'>MESSAGE:&nbsp;</font></b><font color='green'>完成发送:" + str(
                                               path.basename(filepath)) + "  耗时:" + str(
                                               timecomsumption) + "S  速度:" + strspeed + "</font>"))
                else:
                    print("sender", "Exception raised in transmition")
                    # delete file failed to transmit
            except Exception as e:
                self.updateState.emit(("warning", str(path.basename(filepath)) + "传输失败!\n网络中断或者对方已关闭程序"))
                print("receiver", "warning Network is not available or sender has closed!")
                traceback.print_exc(file=sys.stdout)
                allFinished = False
                break

        self.caller.clientTcpConn.shutdown(socket.SHUT_RDWR)
        self.caller.clientTcpConn.close()
        if allFinished == True:
            self.updateRate.emit((-1, -1, -1))
        else:
            self.updateRate.emit((-2, -2, -2))
