'''
Created on 28 nov. 2020

@author: paradoxisme
'''
import sys
from PyQt5.QtWidgets import QApplication
import ui.main_window


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ui.main_window.MainWindow()
    main_window.show()
    sys.exit(app.exec_())
