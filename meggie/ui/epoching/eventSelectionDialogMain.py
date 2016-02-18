# coding: utf-8
from meggie.code_meggie.general.wrapper import wrap_mne_call

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Lepp�kangas, Janne Pesonen and Atte Rautio>
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

"""
Created on Mar 19, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Atte Rautio
Contains the EventSelectionDialog-class that holds the logic for
EventSelectionDialog-window.
"""

import numpy as np
from xlrd import XLRDError
from PyQt4 import QtCore,QtGui
import mne

from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.epoching.events import Events
from meggie.code_meggie.general import fileManager

from meggie.ui.epoching.eventSelectionDialogUi import Ui_EventSelectionDialog
from meggie.ui.epoching.groupEpochingDialogMain import GroupEpochingDialog
from meggie.ui.epoching.fixedLengthEpochDialogMain import FixedLengthEpochDialog
from meggie.ui.general import messageBoxes
from meggie.ui.widgets.batchingWidgetMain import BatchingWidget


class EventSelectionDialog(QtGui.QDialog):
    """
    Class containing the logic for EventSelectionDialog. It is used for
    collecting desired events from continuous data.
    """
    caller = Caller.Instance()
    #custom signals:
    epoch_params_ready = QtCore.pyqtSignal(dict)

    def __init__(self, parent): #, params = None):
        """Initialize the event selection dialog.

        Keyword arguments:

        parent -- Set the parent of this dialog
        params -- A dictionary containing parameter values to fill the
                  the different fields in the dialog with.
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_EventSelectionDialog()
        self.ui.setupUi(self)
        self.fixedLengthDialog = None
        self.ui.lineEditName.setText('Event')
        self.used_names = []
        ch_names = self.caller.experiment.active_subject.working_file.ch_names
        stim_channels = [x for x in ch_names if x.startswith('STI')]
        active = 0
        for idx, channel in enumerate(stim_channels):
            self.ui.comboBoxStimChannel.addItem(channel)
            if channel == self.caller.experiment.active_subject.stim_channel:
                active = idx
        self.ui.comboBoxStimChannel.setCurrentIndex(active)
        
        #if params is not None:
        #    self.fill_parameters(params)
            
        self.batching_widget = BatchingWidget(self, self.ui.scrollAreaWidgetContents)
        for subject in self.caller.experiment.get_subjects():
            self.batching_widget.data[subject.subject_name] = {}
            self.batching_widget.data[subject.subject_name]['events'] = []
            self.batching_widget.data[subject.subject_name]['fixed_length_events'] = [] 

    def initialize(self, epochs_name):
        """
        Method for initializing the dialog. Used for modifying existing epoch
        collection.
        Keyword arguments
        epoch_name -- Name of the epoch collection.
        """
        subject = self.caller.experiment.active_subject
        epochs = subject.get_epochs(epochs_name)
        rejection = subject._epochs[epochs_name].params['reject']
        if 'grad' in rejection.keys():
            self.ui.checkBoxGrad.setChecked(True)
            self.ui.doubleSpinBoxGradReject_3.setValue(rejection['grad'] /
                                                       1e-13)
        else:
            self.ui.checkBoxGrad.setChecked(False)
        if 'mag' in rejection.keys():
            self.ui.checkBoxMag.setChecked(True)
            self.ui.doubleSpinBoxMagReject_3.setValue(rejection['mag'] / 1e-15)
        else:
            self.ui.checkBoxMag.setChecked(False)
        if 'eeg' in rejection.keys():
            self.ui.checkBoxEeg.setChecked(True)
            self.ui.doubleSpinBoxEEGReject_3.setValue(rejection['eeg'] / 1e-6)
        else:
            self.ui.checkBoxEeg.setChecked(False)
        if 'eog' in rejection.keys():
            self.ui.checkBoxEog.setChecked(True)
            self.ui.doubleSpinBoxEOGReject_3.setValue(rejection['eog'] / 1e-6)
        else:
            self.ui.checkBoxEog.setChecked(False)

        self.ui.lineEditCollectionName.setText(epochs_name)
        self.ui.doubleSpinBoxTmin.setValue(epochs.tmin)
        self.ui.doubleSpinBoxTmax.setValue(epochs.tmax)
        event_name = epochs.event_id.keys()[0]
        self.ui.lineEditName.setText(event_name)
        event_id = epochs.event_id.values()[0]
        self.ui.spinBoxEventID.setValue(event_id)
        events = list()
        for event in epochs.events:
            events.append([int(event[0]), int(event[1]), int(event[2])])
        self.add_events(events, event_name)

    def update_events(self, subject):
        """Add a list of events or a single event to the ui's eventlist.

        Keyword arguments:

        events     -- Events to add.
        event_name -- The user-defined name of the events. Default is 'event'.
        """
        self.ui.listWidgetEvents.clear()
        subject_name = subject.subject_name

        if 'events' in self.batching_widget.data[subject_name]:
            events = self.batching_widget.data[subject_name]['events']
            for event in events:
                item = QtGui.QListWidgetItem(
                    '%s, %s (%s, %s)' % (event['event_id'], event['event_name'],
                    'mask=' + str(event['mask']),
                    'stim=' + str(event['stim']))
                ) #str(len(event)) + ' events found'))
                self.ui.listWidgetEvents.addItem(item)

        if 'fixed_length_events' in self.batching_widget.data[subject_name]:
            fixed_length_events = self.batching_widget.data[subject_name]['fixed_length_events']
            for event in fixed_length_events:
                item = QtGui.QListWidgetItem(
                    '%s, %s (%s, %s, %s)' % (event['event_id'], event['event_name'],
                    'start ' + str(event['tmin']), 'end ' + str(event['tmax']),
                    'interval ' + str(event['interval']))
                ) #, str(len(event)) + ' events found'))
                self.ui.listWidgetEvents.addItem(item)
            

        #self.ui.listWidgetEvents.sortItems()
        #if self.used_names.count(event_name) < 1:    
        #    self.used_names.append(event_name)

    def selection_changed(self, subject_name, params_dict):
        """Unpickles parameter file from subject path and updates the values
        on dialog.
        """
        
        self.ui.comboBoxStimChannel.clear()
        for subject in self.caller.experiment.get_subjects():
            if subject_name == subject.subject_name:
                
                #params_dict includes 'events' and 'fixed_length_events' keys
                if len(params_dict) > 2:
                    dic = params_dict
                else:
                    dic = self.get_default_values(subject)
                    
                rejection = dic['reject']
                
                if 'grad' in rejection.keys():
                    self.ui.checkBoxGrad.setChecked(True)
                    self.ui.doubleSpinBoxGradReject_3.setValue(
                        rejection['grad'])
                else:
                    self.ui.checkBoxGrad.setChecked(False)
                if 'mag' in rejection.keys():
                    self.ui.checkBoxMag.setChecked(True)
                    self.ui.doubleSpinBoxMagReject_3.setValue(rejection['mag'])
                else:
                    self.ui.checkBoxMag.setChecked(False)
                if 'eeg' in rejection.keys():
                    self.ui.checkBoxEeg.setChecked(True)
                    self.ui.doubleSpinBoxEEGReject_3.setValue(rejection['eeg'])
                else:
                    self.ui.checkBoxEeg.setChecked(False)
                if 'eog' in rejection.keys():
                    self.ui.checkBoxEog.setChecked(True)
                    self.ui.doubleSpinBoxEOGReject_3.setValue(rejection['eog'])
                else:
                    self.ui.checkBoxEog.setChecked(False)
        
                if 'event_name' in dic.keys():
                    self.ui.lineEditName.setText(dic['event_name'])
                else:
                    self.ui.lineEditName.setText('joo')
                if subject.subject_name != self.caller.experiment.active_subject.subject_name:   
                        raw_path = self.caller.experiment._working_file_names[subject.subject_name]
                        raw = fileManager.open_raw(raw_path, pre_load=False)
                        ch_names = raw.ch_names
                else:
                    ch_names = subject.working_file.ch_names
                if len(ch_names) == 0:
                    pass
                stim_channels = [x for x in ch_names if x.startswith('STI')]

                active = 0
                for idx, channel in enumerate(stim_channels):
                    self.ui.comboBoxStimChannel.addItem(channel)
                    if channel == dic['stim']:
                        active = idx
                self.ui.comboBoxStimChannel.setCurrentIndex(active)
                
                if 'event_id' in dic.keys():
                    self.ui.spinBoxEventID.setValue(dic['event_id'])
                else:
                    self.ui.spinBoxEventID.setValue(1)
                
                self.ui.lineEditCollectionName.setText(dic['collection_name'])
                self.ui.doubleSpinBoxTmin.setValue(dic['tmin'])
                self.ui.doubleSpinBoxTmax.setValue(dic['tmax'])
                self.update_events(subject)
    
    def get_selected_subject(self):
        item = None
        if self.batching_widget.ui.checkBoxBatch.checkState():
            item = self.batching_widget.ui.listWidgetSubjects.currentItem()
        if item is None:
            subject_name = self.caller.experiment.active_subject.subject_name
        else:
            subject_name = str(item.text())
        for subject in self.caller.experiment.get_subjects():
            if subject.subject_name == subject_name:
                return subject
        return None
    
    def get_default_values(self, subject):
        stim_channel = subject.stim_channel
        rejections = {
            'grad': 3000.00,
            'mag': 4000.00
        }
        return {
            'collection_name': 'Epochs',
            'tmin': -0.200,
            'tmax': 0.500,
            'include_stim': True,
            'event_id': 1,
            'stim': stim_channel,
            'mask': 0,
            'event_name': 'Event',
            'reject': rejections
        }

    def collect_parameter_values(self):
        """Collect the parameter values for epoch creation from the ui.

        Collect the parameter values for epoch creation from the ui and return
        them in a dictionary.
        """
        tmin = float(self.ui.doubleSpinBoxTmin.value())
        tmax = float(self.ui.doubleSpinBoxTmax.value())
        mag = self.ui.checkBoxMag.checkState() == QtCore.Qt.Checked
        grad = self.ui.checkBoxGrad.checkState() == QtCore.Qt.Checked
        eeg = self.ui.checkBoxEeg.checkState() == QtCore.Qt.Checked
        stim = self.ui.checkBoxStim.checkState() == QtCore.Qt.Checked
        eog = self.ui.checkBoxEog.checkState() == QtCore.Qt.Checked
        #stim_channel = self.caller.experiment.active_subject._stim_channel

        collection_name = str(self.ui.lineEditCollectionName.text())
        if len(self.parent.epochList.ui.listWidgetEpochs.\
            findItems(collection_name, QtCore.Qt.MatchExactly)) > 0:
            msg = ('Collection name %s exists. Overwrite existing epochs?' %
                   collection_name)
            reply = QtGui.QMessageBox.question(self, 'Collection exists', msg,
                                               QtGui.QMessageBox.Yes |
                                               QtGui.QMessageBox.No,
                                               QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return None

        reject = dict()
        if mag:
            value = self.ui.doubleSpinBoxMagReject_3.value()
            if value != -1:
                reject['mag'] = 1e-15 * value
        if grad:
            value = self.ui.doubleSpinBoxGradReject_3.value()
            if value != -1:
                reject['grad'] = 1e-13 * value
        if eeg:
            value = self.ui.doubleSpinBoxEEGReject_3.value()
            if value != -1:
                reject['eeg'] = 1e-6 * value
        if eog:
            value = self.ui.doubleSpinBoxEOGReject_3.value()
            if value != -1:
                reject['eog'] = 1e-6 * value

        #Check if any picks are found with current parameter values.

        if mag and grad:
            meg = True
        elif mag:
            meg = 'mag'
        elif grad:
            meg = 'grad'
        else: meg = False
        
        
        subject = self.get_selected_subject()
        if subject is self.caller.experiment.active_subject:
            print 'selected subject is active subject'
        if subject == self.caller.experiment.active_subject:
            print 'selected subject == active subject'
        if subject.subject_name is not self.caller.experiment.active_subject.subject_name:
            raw_path = self.caller.experiment._working_file_names[subject.subject_name]
            raw = fileManager.open_raw(raw_path, pre_load=False)
            info = raw.info
        else:
            info = self.caller.experiment.active_subject.working_file.info
        picks = mne.pick_types(info, meg=meg, eeg=eeg, stim=stim, eog=eog)
        if len(picks) == 0:
            message = 'No picks found with current parameter values' 
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return

        #Create a dictionary containing all the parameters
        #Note: Raw is not collected here.
        #events = []
        #fle = []
        events = self.batching_widget.data[subject.subject_name]['events']
        fle = self.batching_widget.data[subject.subject_name]['fixed_length_events']  # noqa
        param_dict = {'mag' : mag, 'grad' : grad,
                      'eeg' : eeg, 'stim' : stim, 'eog' : eog,
                      'reject' : reject, 'tmin' : float(tmin),
                      'tmax' : float(tmax), 'collection_name' : collection_name,
                      'events' : events, 'fixed_length_events' : fle}
        return param_dict

    def create_eventlist(self, subject, event_params):
        """
        Pick desired events from the raw data.
        """
        #TODO: log MNE call: you don't get the stim_channel or mask arguments here, because 
        #the MNE Events' __init__ function uses mne.find_events :  -  D
        #this needs some manual logging or logging from the Events' __ini__
        #e = wrap_mne_call(self.caller.experiment, Events, self.caller.experiment.active_subject.working_file,
        #                  stim_channel, mask)
        if subject.subject_name != self.caller.experiment.active_subject.subject_name:
            raw_path = self.caller.experiment._working_file_names[subject.subject_name]
            raw = fileManager.open_raw(raw_path, pre_load=False)
        else:
            raw = subject.working_file
        
        e = Events(raw, event_params['stim'], event_params['mask'])
        
        mask = np.bitwise_not(event_params['mask'])
        
        #TODO: Log events?
        #events = wrap_mne_call(self.caller.experiment, e.pick, np.bitwise_and(event_id, mask))
        events = e.pick(np.bitwise_and(event_params['event_id'], mask))
        print str(events)
        return events

    def fill_parameters(self, params):
        """Fill the fields in the dialog with parameters values from a dict.

        Keyword arguments:

        params -- A dict containing the parameter values to be used.
        """
        params_str = dict((str(key), value) for
                          key, value in params.iteritems())
        for item in params_str['events']:
            events = []
            events.append(item[0])
            event_name = item[1]
            self.add_events(events, event_name)

        if params_str['mag'] is True:
            self.ui.checkBoxMag.setChecked(True)
        else:
            self.ui.checkBoxMag.setChecked(False)

        if params_str['grad'] is True:
            self.ui.checkBoxGrad.setChecked(True)
        else:
            self.ui.checkBoxGrad.setChecked(False)

        if params_str['eeg'] is True:
            self.ui.checkBoxEeg.setChecked(True)
        else:
            self.ui.checkBoxEeg.setChecked(False)

        if params_str['stim'] is True:
            self.ui.checkBoxStim.setChecked(True)
        else:
            self.ui.checkBoxStim.setChecked(False)

        if params_str['eog'] is True:
            self.ui.checkBoxEog.setChecked(True)
        else:
            self.ui.checkBoxEog.setChecked(False)

        reject = params_str['reject']
        if reject.has_key('mag'):
            self.ui.doubleSpinBoxMagReject_3.setValue(reject['mag'])

        if reject.has_key('grad'):
            self.ui.doubleSpinBoxGradReject_3.setValue(reject['grad'])

        if reject.has_key('eeg'):
            self.ui.doubleSpinBoxEegReject_3.setValue(reject['eeg'])

        if reject.has_key('eog'):
            self.ui.doubleSpinBoxEogReject_3.setValue(reject['eog'])

        self.ui.doubleSpinBoxTmin.setValue(params_str['tmin'])
        self.ui.doubleSpinBoxTmax.setValue(params_str['tmax'])
        self.ui.lineEditCollectionName.setText(params_str['collectionName'])

    def on_pushButtonAdd_clicked(self, checked=None):
        """
        Method for adding events to the event list.
        """
        if checked is None:
            return
        event_params = {
            'stim': str(self.ui.comboBoxStimChannel.currentText()),
            'mask': self.ui.spinBoxMask.value(),
            'event_id': self.ui.spinBoxEventID.value(),
            'event_name': str(self.ui.lineEditName.text())
        }
        #Either active or non-active subject
        subject = self.get_selected_subject()
        events = self.create_eventlist(subject, event_params)
        if len(events) != 0:
            self.batching_widget.data[subject.subject_name]['events'].append(event_params)
            self.update_events(subject)
        

    def accept(self):
        """Save the parameters in a dictionary and send it forward.

        Collect all the parameters provided for epoch creations in a
        dictionary and send it forward using a QSignal. Show the user an error
        message if no events are selected for epoching.

        Emit an epoch_params_ready signal.
        """
        if self.ui.listWidgetEvents.count() == 0:
            message = 'Cannot create epochs from empty list.'
            self.errorMessage = messageBoxes.shortMessageBox(message)
            self.errorMessage.show()
            return
        QtGui.QApplication.setOverrideCursor(QtGui.
                                             QCursor(QtCore.Qt.WaitCursor))
        param_dict = self.collect_parameter_values()
        if param_dict is None:
            QtGui.QApplication.restoreOverrideCursor()
            return

        if all([not self.ui.checkBoxEeg.isChecked(), 
                not self.ui.checkBoxGrad.isChecked(),
                not self.ui.checkBoxMag.isChecked()]):
            QtGui.QApplication.restoreOverrideCursor()
            message = 'Picks cannot be empty. Select picks by checking the ' +\
                      ' checkboxes.'
            self.errorMessage = messageBoxes.shortMessageBox(message)
            self.errorMessage.show()
            return

        self.parent.update_epochs()
        QtGui.QApplication.restoreOverrideCursor()
        self.close()

    def on_pushButtonSaveEvents_clicked(self, checked=None):
        """
        Called when save events button is clicked. Saves all the events in the
        list to an excel-file.
        """
        if checked is None: return # Standard workaround
        events = np.ndarray((self.ui.listWidgetEvents.count(),4), dtype=object)
        for index in xrange(self.ui.listWidgetEvents.count()):
            category = (self.ui.listWidgetEvents.item(index).
                        data(33))
            events[index,0] = str(category)
            event = self.ui.listWidgetEvents.item(index).data(32)
            events[index,1:] = event
        #events = self.create_eventlist()'
        if len(events) > 0:
            try:
                activeSubject = self.caller._experiment._active_subject
                fileManager.write_events(events, activeSubject)
            except UnicodeDecodeError, err:
                message = 'Cannot save events: ' + str(err)
                self.messageBox = messageBoxes.shortMessageBox(message)
                self.messageBox.show()
                print 'Aborting...'
                return

    def on_pushButtonReadEvents_clicked(self, checked=None):
        """
        Called when read events button is clicked. Reads events from an 
        excel-file.
        """
        if checked is None: return # Standard workaround
        title = 'Read events from xls. Format: name|sample|old id|new id.'
        filename = str(QtGui.QFileDialog.getOpenFileName(self, title,
                                                         self.caller.\
                                                         experiment.\
                                                         active_subject.\
                                                         subject_path))
        if filename == '':
            return
        self.ui.listWidgetEvents.clear()
        try:
            sheet = fileManager.read_events(filename)
        except XLRDError, err:
            self.messageBox = messageBoxes.shortMessageBox(str(err))
            self.messageBox.show()
            return

        for row_index in range(sheet.nrows):
            #Check that there are no empty cells in a row
            if not (any([x == '' for x in sheet.row_values(row_index)])):
                item = CustomListItem(str(sheet.cell(row_index,0).value) +
                                      ' ' + str(int(sheet.cell(row_index, 1).
                                                    value)) + ', ' +
                                      str(int(sheet.cell(row_index, 3).value)))
                event = map(int, sheet.row_values(row_index)[1:4])
                print event
                item.setData(32, event)
                item.setData(33, str(sheet.cell(row_index,0).value))
                self.ui.listWidgetEvents.addItem(item)

        self.ui.listWidgetEvents.setCurrentItem(item)

    def on_pushButtonBatching_clicked(self, checked=None):
        """
        Opens a dialog for batch processing epochs.
        """
        if checked is None: 
            return

        batchDialog = GroupEpochingDialog(self)
        batchDialog.exec_()

        self.close()

    def on_pushButtonFixedLength_clicked(self, checked=None):
        """Opens a dialog for creating fixed length events."""
        if checked is None:
            return
        if self.fixedLengthDialog is None:
            self.fixedLengthDialog = FixedLengthEpochDialog(self)
        self.fixedLengthDialog.show()

    def on_pushButtonClear_clicked(self, checked=None):
        """
        Method for clearing the event list.
        """
        self.batching_widget.data.pop('events', None)
        #for row in range(self.ui.listWidgetEvents.count()):
        #    item = self.ui.listWidgetEvents.item(row)
        #    if item.data(33) in self.used_names:
        #        self.used_names.remove(item.data(33))
        self.ui.listWidgetEvents.clear()

    def set_event_name(self, name, suffix = 1):
        """Set the event name to name. If name exists, add suffix to it

        Keyword arguments:

        name   -- The name to be set.
        Suffix -- The suffix that is added to the name when greater than 1.

        Return the name that was set.
        """
        if suffix == 1 and self.used_names.count(name) == 0:
            return name

        elif suffix == 1 and self.used_names.count(name) > 0:
            suffix += 1
            name = self.set_event_name(name, suffix)
            return name

        elif suffix > 1 and self.used_names.count(name + str(suffix)) == 0:
            name = name + str(suffix)
            return name

        elif suffix > 1 and self.used_names.count(name + str(suffix)) > 0:
            suffix += 1
            name = self.set_event_name(name, suffix)
            return name

    def calculate_epochs(self):
        pass
