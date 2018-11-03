from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication


class UIMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

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

        verticalLayoutWidget_2 = QtWidgets.QWidget(centralWidget)
        verticalLayoutWidget_2.setGeometry(QtCore.QRect(511, 45, 151, 261))
        verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")

        receiveFileLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget_2)
        receiveFileLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        receiveFileLayout.setObjectName("receiveFileLayout")

        self.addFileBtn = QtWidgets.QPushButton(verticalLayoutWidget_2)
        self.addFileBtn.setObjectName("addFileBtn")
        receiveFileLayout.addWidget(self.addFileBtn)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        receiveFileLayout.addItem(spacerItem)
        savePathBtn = QtWidgets.QPushButton(verticalLayoutWidget_2)
        savePathBtn.setObjectName("savePathBtn")
        receiveFileLayout.addWidget(savePathBtn)

        verticalLayoutWidget_3 = QtWidgets.QWidget(centralWidget)
        verticalLayoutWidget_3.setGeometry(QtCore.QRect(30, 20, 471, 171))
        verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        statusLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget_3)
        statusLayout.setObjectName("statusLayout")
        status = QtWidgets.QLabel(verticalLayoutWidget_3)
        status.setObjectName("status")
        statusLayout.addWidget(status)
        statusText = QtWidgets.QTextBrowser(verticalLayoutWidget_3)
        statusText.setObjectName("statusText")
        statusLayout.addWidget(statusText)
        verticalLayoutWidget_4 = QtWidgets.QWidget(centralWidget)
        verticalLayoutWidget_4.setGeometry(QtCore.QRect(29, 209, 471, 241))
        verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        processdureLayout = QtWidgets.QVBoxLayout(verticalLayoutWidget_4)
        processdureLayout.setObjectName("processdureLayout")
        processdure = QtWidgets.QLabel(verticalLayoutWidget_4)
        processdure.setObjectName("processdure")
        processdureLayout.addWidget(processdure)
        self.fileList = QtWidgets.QListWidget(verticalLayoutWidget_4)
        self.fileList.setObjectName("fileList")
        processdureLayout.addWidget(self.fileList)

        self.setCentralWidget(centralWidget)

        self.addFileBtn.setText(self.translate("LanTrans", "添加"))
        savePathBtn.setText(self.translate("LanTrans", "保存位置"))
        status.setText(self.translate("LanTrans", "状态"))
        processdure.setText(self.translate("LanTrans", "进度"))

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
