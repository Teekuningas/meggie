'''
Created on Mar 16, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui
from UIehd7 import Ui_MainWindow
import mne
import pylab as pl
from matplotlib.figure import Figure
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from infoDialog_main import InfoDialog
from parameterDialog_main import ParameterDialog
from maxFilterDialog_main import MaxFilterDialog

from epochs import Epochs
from eventList import Events
from createEpochs import CreateEpochs

class MainWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''


    def __init__(self, project):
        '''
        Constructor
        '''
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tabEvoked = None
        self.project = project
        #self.item = QtGui.QTreeWidgetItem(self.ui.treeWidget)
        self.raw = project.get_raw_data() # Onko fiksua olla oma attribuutti???
        #self.ui.treeWidget.topLevelItem(0).setText(0, QtGui.QApplication.translate("MainWindow", str(self.raw), None, QtGui.QApplication.UnicodeUTF8))
        #self.ui.treeWidget.editItem
        info = InfoDialog(self.raw, self.ui, False)
        self.ui.pushButtonAverage.setEnabled(False)
        self.ui.pushButtonVisualize.setEnabled(False)
        
        """ Draws a graph to the window"""
        
        """
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.ui.centralwidget)
        self.axes = self.fig.add_subplot(111)
        
        picks = mne.fiff.pick_types(self.raw.info, meg='mag')
        start, stop = self.raw.time_as_index([0, 15])  # read the first 15s of data
        data, times = self.raw[picks[:5], start:(stop + 1)]  # take 5 first channels
        self.axes.plot(times, data.T)
        self.canvas.draw()
        #pl.xlabel('time (s)')
        #pl.ylabel('MEG data (T)')
        """
        
        
    def on_pushButtonEpoch_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.epochParameterDialog = ParameterDialog(self)
        self.epochParameterDialog.show()
        #eveFile = self.raw.info.get('filename')[:-4] + '-eve.fif'
        #self.epochParameterDialog.fileEdit.setText(eveFile)
        
    def on_pushButtonAverage_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        epoch = self.ui.listWidgetEpochs.currentItem().data(1).toPyObject()
        evoked = epoch.average()
        
        #Check if the tab has already been created
        if self.ui.tabEvoked == None:
            self.ui.tabEvoked = QtGui.QWidget()
            self.ui.listWidgetAverage = self.__create_tab(self.ui.tabEvoked, 'Evoked')
        item = QtGui.QListWidgetItem()
        item.setText('TestElement')
        item.setData(1,evoked)
        self.ui.listWidgetAverage.addItem(item)
        evoked.plot()
        
    def on_pushButtonMaxFilter_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.maxFilterDialog = MaxFilterDialog(self, self.raw)
        self.maxFilterDialog.show()
        
    
      
    def create_epochs(self):
        stim_channel = str(self.epochParameterDialog.ui.comboBoxStimulus.currentText())
        event_id = self.epochParameterDialog.ui.lineEditEventID.text()
        tmin = self.epochParameterDialog.ui.lineEditTmin.text()
        tmax = self.epochParameterDialog.ui.lineEditTmax.text()
        reject = self.epochParameterDialog.ui.lineEditReject.text()
        meg = self.epochParameterDialog.ui.checkBoxMeg.checkState() == QtCore.Qt.Checked
        eeg = self.epochParameterDialog.ui.checkBoxEeg.checkState() == QtCore.Qt.Checked
        stim = self.epochParameterDialog.ui.checkBoxStim.checkState() == QtCore.Qt.Checked
        eog = self.epochParameterDialog.ui.checkBoxEog.checkState() == QtCore.Qt.Checked
        epochs = Epochs(self.raw, stim_channel, meg, eeg, stim, eog, reject, float(tmin),
                        float(tmax), int(event_id))
        self.ui.tabEpoch = QtGui.QWidget()
        self.__create_tab(self.ui.tabEpoch, 'Epoch')
        
        """
        
        print eveFile
        events = Events(eveFile)
        self.epochs = Epochs(self.raw, events.events)
        evoked = self.epochs.average()
        evoked.plot()
        """
    
    def __create_tab(self, tab, title):
        """
        Creates a new tab with a listWidget to tabWidget.
        
        Keyword arguments:
        tab           -- A QWidget
        title         -- Title for the tab
        list          -- A QListWidget
        returns a reference to the newly created listWidget
        """
        self.ui.horizontalLayoutWidget = QtGui.QWidget(tab)
        self.ui.tabWidget.addTab(tab, title)
        self.ui.horizontalLayoutWidget = QtGui.QWidget(tab)
        self.ui.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10,
                                                                341, 511))
        #self.ui.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))

        #self.listWidget.setObjectName(("listWidgetEpochs"))
        