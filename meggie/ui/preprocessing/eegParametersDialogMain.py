'''
Created on 6.10.2016

@author: jaolpeso
'''
from PyQt4 import QtCore,QtGui
from meggie.ui.preprocessing.eegParametersDialogUi import Ui_Dialog

import mne
import numpy as np

from meggie.code_meggie.general.caller import Caller
from meggie.ui.utils.messaging import exc_messagebox

class EegParametersDialog(QtGui.QDialog):
    
    caller = Caller.Instance()
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        raw = self.caller.experiment.active_subject.get_working_file()
        self.ui.comboBoxChannelSelect.addItems(raw.info.get('ch_names'))
        
        self.event_id = None
        self.ui.tableWidgetEvents.currentItemChanged.connect(
            self.on_currentChanged
        )
        self.ui.tableWidgetEvents.setSortingEnabled(False)
        self.ui.tableWidgetEvents.setSelectionBehavior(1)        
        self.ui.tableWidgetEvents.setColumnCount(4)
        self.ui.tableWidgetEvents.setHorizontalHeaderLabels([
            "Time (s)",
            "Sample",
            "Prev. id",
            "Current id"
        ])
        
    def on_pushButtonAdd_clicked(self, checked=None):
        """
        Finds EOG-events from the raw data.
        Called when find eog events -button is clicked.
        """
        raw = self.caller.experiment.active_subject.get_working_file()
        if checked is None or not raw: return
        
        params = dict()
        self.event_id = int(self.ui.labelBlinkId.text())
        params['event_id'] = self.event_id
        params['ch_name'] = str(self.ui.comboBoxChannelSelect.currentText())
        params['l_freq'] = float(self.ui.doubleSpinBoxLowPass.value())
        params['h_freq'] = float(self.ui.doubleSpinBoxHighPass.value())
        params['filter_length'] = str(self.ui.spinBoxFilterLength.value())+'s'
        params['tstart'] = float(self.ui.doubleSpinBoxStart.value())
        
        try:
            eog_events = self.caller.find_eog_events(params)
            self.ui.tableWidgetEvents.clear()
            self.ui.tableWidgetEvents.setRowCount(0)
            for i in range(0, len(eog_events)):
                self.ui.tableWidgetEvents.insertRow(i)
                self.ui.tableWidgetEvents.setItem(
                    i,0,QtGui.QTableWidgetItem(
                        str(raw.index_as_time(eog_events[i][0])[0])
                    )
                )
                self.ui.tableWidgetEvents.setItem(i,1,QtGui.
                    QTableWidgetItem(str(int(eog_events[i][0])))
                )
                self.ui.tableWidgetEvents.setItem(
                    i,2,QtGui.QTableWidgetItem(str(eog_events[i][1]))
                )
                self.ui.tableWidgetEvents.setItem(
                    i,3,QtGui.QTableWidgetItem(str(eog_events[i][2]))
                )
        except Exception as e:
            exc_messagebox(self, e)
        self.ui.tableWidgetEvents.setHorizontalHeaderLabels([
            "Time (s)",
            "Sample",
            "Prev. id",
            "Current id"
        ])
            
    def get_events(self):
        """
        A convenience function for fetching all the events from
        the tableWidgetEvents as a numpy array.
        returns:
        eog_events as numpy array
        """
        events = list()
        rowCount = self.ui.tableWidgetEvents.rowCount()
        
        for i in xrange(0, rowCount):
            #time = float(self.ui.tableWidgetEvents.item(i, 1).text())
            time = int(self.ui.tableWidgetEvents.item(i, 1).text())
            prev = int(self.ui.tableWidgetEvents.item(i, 2).text())
            curr = int(self.ui.tableWidgetEvents.item(i, 3).text())
            events.append([time, prev, curr])

        return np.array(events)

    def on_pushButtonRemove_clicked(self, checked=None):
        if checked is None: return
        index = self.ui.tableWidgetEvents.currentRow()
        self.ui.tableWidgetEvents.removeRow(index)

    @QtCore.pyqtSlot()
    def on_currentChanged(self):
        """
        Called when tableWidgetEvent row selection is changed.
        """
        index = self.ui.tableWidgetEvents.currentIndex().row()
        if index < 0:
            self.ui.pushButtonRemove.setEnabled(False)
        else:
            self.ui.pushButtonRemove.setEnabled(True)

    def on_pushButtonPlotEpochs_clicked(self, checked=None):
        """
        Plots the averaged epochs.
        """
        if checked is None: return
        events = self.get_events()
        tmin = self.ui.doubleSpinBoxTmin.value()
        tmax = self.ui.doubleSpinBoxTmax.value()
        self.caller.plot_average_epochs(events, tmin, tmax, self.event_id)
        
    def on_pushButtonShowEvents_clicked(self, checked=None):
        """
        Plots the events on mne_browse_raw.
        """
        if checked is None: return
        events = self.get_events()
        self.caller.plot_events(events)

    def on_pushButtonCompute_clicked(self):
        params = dict()
        params['events'] = self.get_events()
        params['event_id'] = 998
        params['tmin'] = self.ui.doubleSpinBoxTmin.value()
        params['tmax'] = self.ui.doubleSpinBoxTmax.value()
        params['n_eeg'] = self.ui.spinBoxVectors.value()
        self.caller.call_eeg_ssp(params, self.caller.experiment.active_subject)
        self.close()
        self.parent.initialize_ui()
        
        