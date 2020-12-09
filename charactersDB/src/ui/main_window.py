'''
Created on 28 nov. 2020

@author: inilog
'''
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QLineEdit
from PyQt5 import uic
from ui.char_form import CharForm
from model.base import DataBase
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
ui_file_dir = os.path.join(current_dir, 'ui_files')
file_name = os.path.join(ui_file_dir, 'mainwindow.ui')


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(file_name, self)
        self.action_new_db.triggered.connect(self.create_DB)
        self.action_ope_db.triggered.connect(self.open_db)
        self.action_new_char.triggered.connect(self.create_char)
        self._db = DataBase()
        self._base_URI = None

    def create_DB(self):
        file_name, _ = QFileDialog(self).getSaveFileName(None, 'Créer', '',
                                                        '*.cdb')
        base_URI, okPressed = QInputDialog.getText(self, "Base URI","Base URI:",
                                                   QLineEdit.Normal, "")
        if file_name and okPressed:
            self._db.create(file_name, base_URI)

    def open_db(self):
        file_name, _ = QFileDialog.getOpenFileName(None, 'Ouvrir', '', '*.cdb')
        if file_name:
            self._db.load(file_name)

    def create_char(self):
        self._char_form = CharForm(self._db)
        self._char_form.show()
