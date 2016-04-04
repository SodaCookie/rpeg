#!python3.4

from PyQt5 import QtGui, QtWidgets
import sys
import os

import editor.design as design

class Editor(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = Editor()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()