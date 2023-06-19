import pathlib, fitz
from PySide6 import QtCore, QtWidgets, QtGui
from widgets.leftLayout import LeftLayout
from screens.initScreen import InitScreen
from screens.managerScreen import ManagerScreen
import numpy as np
import cv2
import sys
import os



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = InitScreen()#ManagerScreen('pdfs/01165256_1grup.pdf',9)#InitScreen()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())

