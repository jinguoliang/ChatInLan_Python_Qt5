from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication


class UIMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.scan_button = None
        self.send = None

        self.translate = QtCore.QCoreApplication.translate

        self.setObjectName("clazz")
        self.setEnabled(True)
        self.setFixedSize(689, 497)
        self.setWindowTitle(self.translate("LanTrans", "LanTrans"))

        self.construct_ui()
        self.construct_menu_bar()
        self.construct_status_bar()

        QtCore.QMetaObject.connectSlotsByName(self)

    def construct_ui(self):
        centralWidget = QtWidgets.QWidget(self)
        centralWidget.setObjectName("centralwidget")

        self.create_control_part(centralWidget)
        self.create_receiver_part(centralWidget)
        self.create_list_part(centralWidget)

        self.setCentralWidget(centralWidget)

    def create_control_part(self, parent):
        part = QtWidgets.QWidget(parent)
        part.setGeometry(QtCore.QRect(511, 45, 151, 261))
        part.setObjectName("part")

        vbox = QtWidgets.QVBoxLayout(part)
        vbox.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        vbox.setObjectName("vbox")

        self.scan_button = QtWidgets.QPushButton(part)
        self.scan_button.setObjectName("scan_button")
        self.scan_button.setText(self.translate("LanTrans", "扫描"))

        vbox.addWidget(self.scan_button)

        space = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        vbox.addItem(space)

        self.send = QtWidgets.QPushButton(part)
        self.send.setObjectName("send")
        self.send.setText(self.translate("LanTrans", "发送"))
        vbox.addWidget(self.send)

        return part

    def create_list_part(self, parent):
        part = QtWidgets.QWidget(parent)
        part.setGeometry(QtCore.QRect(29, 209, 471, 241))
        part.setObjectName("part")

        vbox = QtWidgets.QVBoxLayout(part)
        vbox.setObjectName("vbox")

        label = QtWidgets.QLabel(part)
        label.setObjectName("label")
        label.setText(self.translate("LanTrans", "进度："))
        vbox.addWidget(label)

        self.fileList = QtWidgets.QListWidget(part)
        self.fileList.setObjectName("fileList")
        vbox.addWidget(self.fileList)

        return part

    def create_receiver_part(self, parent):
        part = QtWidgets.QWidget(parent)
        part.setGeometry(QtCore.QRect(30, 20, 471, 171))
        part.setObjectName("part")

        vbox = QtWidgets.QVBoxLayout(part)
        vbox.setObjectName("vbox")

        label = QtWidgets.QLabel(part)
        label.setObjectName("label")
        label.setText(self.translate("LanTrans", "接收者："))
        vbox.addWidget(label)


        text = QtWidgets.QTextBrowser(part)
        text.setObjectName("text")
        vbox.addWidget(text)

        return part

    def construct_status_bar(self):
        status_bar = QtWidgets.QStatusBar(self)
        status_bar.setObjectName("status_bar")
        self.setStatusBar(status_bar)

    def construct_menu_bar(self):
        menu_bar = QtWidgets.QMenuBar(self)
        menu_bar.setGeometry(QtCore.QRect(0, 0, 689, 25))
        menu_bar.setObjectName("menu_bar")

        menu_file = QtWidgets.QMenu(menu_bar)
        menu_file.setObjectName("menu_file")
        menu_file.setTitle(self.translate("LanTrans", "文件"))

        menu_about = QtWidgets.QMenu(menu_bar)
        menu_about.setObjectName("menu_about")
        menu_about.setTitle(self.translate("LanTrans", "帮助"))

        self.setMenuBar(menu_bar)

        action_exit = QtWidgets.QAction(self)
        action_exit.setObjectName("action_exit")
        action_exit.setText(self.translate("LanTrans", "退出"))
        menu_file.addAction(action_exit)

        action_about = QtWidgets.QAction(self)
        action_about.setObjectName("action_about")
        action_about.setText(self.translate("LanTrans", "关于"))
        menu_about.addAction(action_about)

        menu_bar.addAction(menu_file.menuAction())
        menu_bar.addAction(menu_about.menuAction())


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = UIMain()
    w.show()
    sys.exit(app.exec_())
