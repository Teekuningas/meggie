# coding: utf-8

# Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppakangas, Janne Pesonen and
# Atte Rautio>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of the FreeBSD Project.

'''
Created on Oct 31, 2013

@author: jaolpeso
'''
from PyQt4 import QtCore, QtGui

from meggie.ui.general.addSubjectDialogUi import Ui_AddSubject
from meggie.ui.general.infoDialogUi import Ui_infoDialog
from meggie.ui.general.infoDialogMain import InfoDialog

from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general import fileManager

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox

import traceback
import os


class AddSubjectDialog(QtGui.QDialog):
    """
    Class for creating subjects from raw measurement data files.

    Properties:
    parent    -- mainWindowMain is the parent class
    """
    caller = Caller.Instance()

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_AddSubject()
        self.ui.setupUi(self)

        self.parent = parent
        self.ui.pushButtonShowFileInfo.setEnabled(False)

    def accept(self):
        """ Add the new subject. """
        for i in range(self.ui.listWidgetFileNames.count()):
            item = self.ui.listWidgetFileNames.item(i)
            raw_path = item.text()
            basename = os.path.basename(raw_path)
            subject_name = basename.split('.')[0]

            # Check if the subject is already added to the experiment.
            if subject_name in self.caller.experiment.subjects:
                msg = ('Subject ' + subject_name + ' is already added to the '
                       'experiment. Change the filename of the raw every time '
                       'you want to create a new subject with the same raw '
                       'file.')
                messagebox(self.parent, msg)
                return

            try:
                self.caller.experiment.create_subject(subject_name,
                                                      self.caller.experiment,
                                                      basename,
                                                      raw_path=raw_path)
            except Exception as e:
                exc_messagebox(self.parent, e)
                return

        try:
            self.caller.activate_subject(subject_name)
        except Exception as e:
            exc_messagebox(self.parent, e)

        # Set source file path here temporarily. create_active_subject in
        # experiment sets the real value for this attribute.

        self.caller.experiment.save_experiment_settings()
        self.parent.initialize_ui()

        # To tell the MVC models that the active subject has changed.
        self.parent.reinitialize_models()

        self.close()

    def on_pushButtonBrowse_clicked(self, checked=None):
        """Open file browser for raw data files."""
        if checked is None:
            return

        self.fnames = QtGui.QFileDialog.getOpenFileNames(self,
                                                         'Select one or more '
                                                         'files to open.',
                                                         '/home/')

        if len(self.fnames) > 0:
            for name in self.fnames:
                item = QtGui.QListWidgetItem()
                item.setText(name)
                # TODO add name into the list of filenames
                if len(self.ui.listWidgetFileNames.findItems(name, QtCore.Qt.
                                                             MatchExactly)
                       ) > 0:
                    continue
                self.ui.listWidgetFileNames.addItem(item)

    def on_pushButtonShowFileInfo_clicked(self, checked=None):
        """Opens the infoDialog for the raw file selected."""
        if checked is None:
            return

        try:
            self.raw = fileManager.open_raw(self.ui.listWidgetFileNames.
                                            currentItem().text(),
                                            pre_load=False)
            self.ui.pushButtonShowFileInfo.setEnabled(True)

        except Exception as e:
            exc_messagebox(self, e)
            return

        info = Ui_infoDialog()
        self.infoDialog = InfoDialog(self.raw, info, True)
        self.infoDialog.show()

        QtGui.QApplication.processEvents()

    def on_pushButtonRemove_clicked(self, checked=None):
        """Removes selected filenames on the listWidgetFileNames."""
        if checked is None:
            return
        for item in self.ui.listWidgetFileNames.selectedItems():
            i = self.ui.listWidgetFileNames.indexFromItem(item)
            row = i.row()
            self.ui.listWidgetFileNames.takeItem(row)

    def on_listWidgetFileNames_itemSelectionChanged(self):
        items = self.ui.listWidgetFileNames.selectedItems()
        if len(items) > 0:
            self.ui.pushButtonRemove.setEnabled(True)
        else:
            self.ui.pushButtonRemove.setEnabled(False)
        if len(items) == 1:
            self.ui.pushButtonShowFileInfo.setEnabled(True)
        else:
            self.ui.pushButtonShowFileInfo.setEnabled(False)
