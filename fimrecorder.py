#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui_fimwindow import Ui_fimWindow
def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_fimWindow()
    ui.setupUi(window)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
