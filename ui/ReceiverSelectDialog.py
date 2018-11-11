import sys

import PyQt5.QtWidgets as qt
from qtpy import QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = qt.QDialog()
    dialog.show()
    sys.exit(app.exec_())
