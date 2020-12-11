'''
Created on 29 nov. 2020

@author: paradoxisme
'''
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from model.base import Character, Status
from peewee import InterfaceError, IntegrityError
import urllib.parse
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
        self.name_edit.textChanged.connect(self.name_changed)
        self.load_status()
        if character is None:
            self._character = Character()
        else:
            self._character = character
            self.name_edit.setText(character.name)
            self.URI_edit.setText(character.URI[len(base.base_URI):])
            self.summary_edit.setPlainText(character.summary)
            for i, status in enumerate(self._status_list):
                if self._character.status == status:
                    self.status_combo.setCurrentIndex(i)

    def name_changed(self, name):
        self.URI_edit.setText(urllib.parse.quote(name))

    def save_character(self):
        URI = self.base_URI_label.text() + self.URI_edit.text()
        self._character.URI = URI
        self._character.name = self.name_edit.text()
        self._character.summary = self.summary_edit.toPlainText()
        status_index = self.status_combo.currentIndex()
        self._character.status = self._status_list[status_index]
        try:
            self._character.save()
        except InterfaceError:
            pass
        except IntegrityError:
            common_URI = Character.get(URI==URI)
            self._character.URI += '.' + str(common_URI.next_unic_URI_value)
            common_URI.next_unic_URI_value += 1
            common_URI.save()
            self._character.save()

    def load_status(self):
        self._status_list = []
        try:
            querry = Status.select()
            for status in querry:
                self._status_list.append(status)
                self.status_combo.addItem(status.name)
        except InterfaceError:
            pass
