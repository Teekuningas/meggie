# coding: latin1

"""
Created on May 2, 2013

@author: Jaakko Leppakangas, Atte Rautio
Contains the EpochWidget-class used for listing epoch collections.
"""
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

from code_meggie.general.caller import Caller
from epochWidgetUi import Ui_Form

class EpochWidget(QtGui.QWidget):
    """
    Creates a widget that shows a list of epoch collections.
    """
    
    #Custom signals:
    on_selection_changed = pyqtSignal()
    item_added = pyqtSignal(QtGui.QListWidgetItem)
    #last_epoch_item_removed = pyqtSignal()

    def __init__(self, parent):
        """
        Constructor 
        """
        QtGui.QWidget.__init__(self, parent)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.parent = parent
        
        # Connect listWidgetEpochs.currentItemChanged method to change
        # parameters on epochParamsWidget
        self.ui.listWidgetEpochs.currentItemChanged.connect(self.selection_changed)
        
    def addItem(self, item, suffix = 1):
        """
        Add an item or items to the widget's list and sort the list.
        
        If item is a list, add all the items in it. Item text is converted to
        start with an uppercase letter and the list is also sorted in ascending
        order.
        Emit an item_added signal
        
        Keyword arguments:
        item   = a single QListWidgetItem or a list of QListWidgetItems
                 to be added.
        suffix = a suffix given to the item to make the item's text unique.
        
        """
        try:
            for i in item:
                #A recursive call for each individual item
                self.addItem(i)
        
        except TypeError:
            #If suffix is 1 there's no need to add it to the item's text. I.e.
            #Name "Epochs" doesn't have to become "Epochs1"
            if suffix is 1:
                if not self.ui.listWidgetEpochs.findItems(item.text(),\
                                                          QtCore.Qt.\
                                                          MatchFixedString):
                    self.ui.listWidgetEpochs.addItem(item)
                    self.ui.listWidgetEpochs.sortItems()
                    self.item_added.emit(item)
                else:
                    suffix += 1
                    self.addItem(item, suffix)
                
            else:
                if not self.ui.listWidgetEpochs.findItems(item.text() +\
                                                          suffix,\
                                                          QtCore.Qt.\
                                                          MatchFixedString):
                    item.setText(item.text() + suffix)
                    self.ui.listWidgetEpochs.addItem(item)
                    self.ui.listWidgetEpochs.sortItems()
                    self.item_added.emit(item) 
                else:
                    suffix += 1
                    self.addItem(item, suffix)
                    
    def clearItems(self):
        """Remove all the items from the widget's list.
        """
        while self.ui.listWidgetEpochs.count() > 0:
            self.ui.listWidgetEpochs.takeItem(0)
            
    def currentItem(self):
        """return The currently selected item from the widget's list."""
        if self.ui.listWidgetEpochs.count() == 0: return None
        else:
            return self.ui.listWidgetEpochs.currentItem() 
            
    def isEmpty(self):
        """Return True if the widget is empty, otherwise return False."""
        if self.ui.listWidgetEpochs.count() > 0:
            return False
        else:
            return True
        
    def remove_item(self, item):
        """Remove an item from the list.
        
        Keyword arguments:
        
        item -- The item to be removed
        """
        row = self.ui.listWidgetEpochs.row(item)
        self.ui.listWidgetEpochs.takeItem(row)
            
    def setCurrentItem(self, item):
        """
        sets the current item of the widget's list.
        
        Keyword arguments:
        item = item to be set as the current item.
        """
        self.ui.listWidgetEpochs.setCurrentItem(item)
        
    def selection_changed(self):
        item = self.ui.listWidgetEpochs.currentItem()
        if item is None: return
        caller = Caller.Instance()
        epochs = caller.experiment.active_subject._epochs[str(item.text())]
        if self.ui.listWidgetEpochs.currentItem() is None:
            self.parent.clear_epoch_collection_parameters()
        else:
            self.parent.show_epoch_collection_parameters(epochs)
 