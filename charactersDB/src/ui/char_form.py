'''
Created on 29 nov. 2020

@author: paradoxisme
'''
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from model.base import Character
from peewee import InterfaceError
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
ui_file_dir = os.path.join(current_dir, 'ui_files')
file_name = os.path.join(ui_file_dir, 'char_form.ui')


class CharForm(QWidget):
    def __init__(self, base, character=None):
        QWidget.__init__(self)
        uic.loadUi(file_name, self)
        self._db = base
        self.base_URI_label.setText(base.base_URI)
        self.save_button.clicked.connect(self.save_character)
        if character is None:
            self._character = Character()
        else:
            self._character = character
            self.name_edit.setText(character.name)
            self.URI_edit.setText(character.URI[len(base.base_URI):])
            self.summary_edit.setPlainText(character.summary)

    def save_character(self):
        self._character.URI = self.base_URI_label.text() + self.URI_edit.text()
        self._character.name = self.name_edit.text()
        self._character.summary = self.summary_edit.toPlainText()
        try:
            self._character.save()
        except InterfaceError:
            pass
