#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from fimui import ui_fimwindow
import pyloncom
def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = ui_fimwindow.Ui_fimWindow()
    ui.setupUi(window)

    camera = pyloncom.QCamera()
    #ui.actionRecord.toggled.connect(lambda: camera.exampleSlot("test"))
    #ui.actionRecord.toggled[bool].connect(camera.exampleSlot)
    camera.device_status[str].connect(ui.statusbar.showMessage)
    camera.is_grabbing.connect(lambda: ui.statusbar.showMessage("grabbing..."))


    ui.actionRefresh.triggered.connect(camera.refresh)
    #WIP:
    ui.actionRefresh.triggered.connect(camera.grabInBackground)



    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
