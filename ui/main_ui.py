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
        root_widget = QtWidgets.QWidget(self)
        root_widget.setObjectName("root")

        self.create_control_part(root_widget)
        self.create_receiver_part(root_widget)
        self.create_list_part(root_widget)
        self.setCentralWidget(root_widget)

    def create_my_ip_part(self, part, parent):

        hbox = QtWidgets.QHBoxLayout(part)
        hbox.setObjectName("hbox")

        label = QtWidgets.QLabel(part)
        label.setObjectName("label")
        label.setText(self.translate("LanTrans", "我的 IP："))
        hbox.addWidget(label)

        self.my_ip_label = QtWidgets.QLabel(part)
        self.my_ip_label.setObjectName("my_ip_label")
        self.my_ip_label.setText("...")
        hbox.addWidget(self.my_ip_label)

        hbox.addStretch(1)

        parent.addItem(hbox)

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
        label.setText(self.translate("LanTrans", "消息："))
        vbox.addWidget(label)

        self.chat_list = QtWidgets.QListWidget(part)
        self.chat_list.setObjectName("chat_list")
        vbox.addWidget(self.chat_list)

        return part

    def create_receiver_part(self, parent):
        part = QtWidgets.QWidget(parent)
        part.setGeometry(QtCore.QRect(30, 20, 471, 171))
        part.setObjectName("part")

        vbox = QtWidgets.QVBoxLayout(part)
        vbox.setObjectName("vbox")

        self.create_my_ip_part(part, vbox)

        label = QtWidgets.QLabel(part)
        label.setObjectName("label")
        label.setText(self.translate("LanTrans", "接收者："))
        vbox.addWidget(label)

        self.receiver_list_widget = QtWidgets.QListWidget(part)
        self.receiver_list_widget.setObjectName("receiver_list")
        vbox.addWidget(self.receiver_list_widget)

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

    def show_message(self, message):
        self.chat_list.addItem(str(message))

    def display_receiver(self, receivers):
        self.receiver_list_widget.clear()
        try:
            self.receiver_list_widget.addItems([r[0] for r in receivers])
        except Exception as e:
            print(e)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = UIMain()
    w.show()
    sys.exit(app.exec_())
