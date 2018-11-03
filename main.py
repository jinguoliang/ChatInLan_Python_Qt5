# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LanTrans.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtWidgets

from LanTrans_desktop import LanTrans
from UIMain import UIMain

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main = LanTrans()
    main.show()
    sys.exit(app.exec_())
