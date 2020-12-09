'''
Created on 29 nov. 2020

@author: paradoxisme
'''
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from model.base import Character
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
ui_file_dir = os.path.join(current_dir, 'ui_files')
file_name = os.path.join(ui_file_dir, 'char_form.ui')


class CharForm(QWidget):
    def __init__(self, base):
        QWidget.__init__(self)
        uic.loadUi(file_name, self)
        self._db = base
        self.base_URI_label.setText(base.base_URI)
        self.save_button.clicked.connect(self.save_character)
        self._cheracter = Character()

    def save_character(self):
        self._cheracter.URI = self.base_URI_label.text() + self.URI_edit.text()
        self._cheracter.name = self.name_edit.text()
        self._cheracter.summary = self.summary_edit.toHtml()
        self._cheracter.save()
