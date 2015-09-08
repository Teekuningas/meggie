# coding: latin1

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppäkangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies, 
#either expressed or implied, of the FreeBSD Project.


'''
Created on Oct 31, 2013

@author: jaolpeso
'''
from PyQt4 import QtCore,QtGui

from addSubjectDialogUi import Ui_AddSubject
import fileManager
from subject import Subject
from infoDialogMain import InfoDialog
import messageBoxes
import traceback

import os, sys

from infoDialogUi import Ui_infoDialog



class AddSubjectDialog(QtGui.QDialog):
    """
    Class for creating subjects from raw measurement data files.
    
    Properties:
    parent    -- mainWindowMain is the parent class
    """
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_AddSubject()
        self.ui.setupUi(self)
        self.parent = parent
        self.experiment = self.parent.experiment
        self.ui.pushButtonShowFileInfo.setEnabled(False)
        #self.ui.lineEditFileName.textChanged.connect(self.file_path_changed)
        
        #if self.ui.listWidgetFileNames.count() > 0:
        self.ui.listWidgetFileNames.itemClicked.connect(self.file_path_changed)
    
    def accept(self):
        """ Add the new subject. """
        for i in range(self.ui.listWidgetFileNames.count()):
            item = self.ui.listWidgetFileNames.item(i)
            raw_path = item.text()
            raw_path_prefix = raw_path.split('.')[-2]
            subject_name = os.path.basename(raw_path_prefix)
            subject_name_string = str(subject_name)
            
            # Check if the subject is already added to the experiment.
            if len(self.parent.ui.listWidgetSubjects.
                   findItems(subject_name_string, QtCore.Qt.MatchExactly)) > 0:
                message = 'Subject ' + item.text() + ' is already added ' +\
                        'to the experiment. Change the filename of the raw ' +\
                        'every time you want to create a new subject with ' +\
                        'the same raw file.' 
                self.messageBox = messageBoxes.shortMessageBox(message)
                self.messageBox.show()
                return
                 
            try:  
                self.parent.experiment.create_subject(subject_name, 
                                                      self.experiment, raw_path)
            except Exception:
                tb = traceback.format_exc()
                title = 'Problem creating a new subject'
                message = 'There was a problem creating a new subject. ' + \
                      'Please copy the following to your bug report:\n\n' + \
                       str(tb)
                self.messageBox = messageBoxes.longMessageBox(title, message)
                self.messageBox.show()
             
            self.parent.experiment.activate_subject(subject_name)
            
        """
        # Set source file path here temporarily. create_active_subject in
        # experiment sets the real value for this attribute.
        self.parent.experiment._active_subject_raw_path = raw_path
        """
        self.parent.experiment.save_experiment_settings()
        self.parent._initialize_ui()
        
        # To tell the MVC models that the active subject has changed.
        self.parent.reinitialize_models() 
        
        self.close()
        
        
    def on_pushButtonBrowse_clicked(self, checked=None):
        """
        Open file browser for raw data files.
        """
        if checked is None: return
        
        self.fnames = QtGui.QFileDialog.\
                         getOpenFileNames(self, 'Select one or more files' + \
                                         ' to open.', '/home/')
        #if self.fname != '':        
        #    self.ui.lineEditFileName.setText(self.fname)
        if len(self.fnames) > 0:
            for name in self.fnames:
                item = QtGui.QListWidgetItem()
                item.setText(name)
                # TODO add name into the list of filenames
                self.ui.listWidgetFileNames.addItem(item)
            
            
    def on_pushButtonShowFileInfo_clicked(self, checked = None):
        """
        Opens the infoDialog for the raw file selected.
        """
        try:
            self.raw = fileManager.open_raw(self.ui.listWidgetFileNames.currentItem().text(), pre_load = False)
            self.ui.pushButtonShowFileInfo.setEnabled(True)
            
        except IOError as e:
            self.messageBox = messageBoxes.shortMessageBox(str(e))
            self.messageBox.show()
            return
        
        except OSError as e:
            self.messageBox = messageBoxes.shortMessageBox(str(e))
            self.messageBox.show()
            return
        
        except ValueError as e:
            self.messageBox = messageBoxes.shortMessageBox(str(e))
            self.messageBox.show()
            return
            return
            
        info = Ui_infoDialog()
        self.infoDialog = InfoDialog(self.raw, info, True)
        self.infoDialog.show()

        QtGui.QApplication.processEvents()
        
        
    def file_path_changed(self):
        """A slot for enabling or disabling show file info button.
        """
        if self.ui.listWidgetFileNames.currentItem() is not None:
            self.ui.pushButtonShowFileInfo.setEnabled(True)
        else:
            self.ui.pushButtonShowFileInfo.setEnabled(False)