# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from presenter.main_presenter import LanTrans

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main = LanTrans()
    main.show()
    sys.exit(app.exec_())
