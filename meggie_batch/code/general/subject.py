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


"""
Created on Oct 22, 2013

@author: jaolpeso
"""

from PyQt4.QtCore import QObject

import os, sys

import mne

class Subject(QObject):
    
    def __init__(self, experiment, subject_name):
        """
        Constructor for the subject class.
        
        Keyword arguments:
        raw_data        -- the raw data file of the subject
        subject_name    -- the name of the subject
        """
        self._raw_data = None
        
        # Either user defined or the name of the data file.
        self._subject_name = subject_name
        
        self._event_set = None
        self._stim_channel = None
        self._working_file = ''
        self._working_file_path = 'no path defined'
        
        #TODO: save raw here or somewhere else
        self._experiment = experiment
        
        # experiment_name is saved as QString and it has to be converted to
        # string to be able to do basic string operations for subject_path.
        self._subject_path = self._experiment.workspace + '/' + \
        str(self._experiment.experiment_name) + '/' + self._subject_name
        self._epochs_directory = self._subject_path + '/epochs/'
        #self.save_raw(raw_data, self.subject_path)
        
    @property
    def raw_data(self):
        """
        Returns the raw data file of the subject.
        """
        return self._raw_data
    
    @raw_data.setter
    def raw_data(self, raw_data):
        """
        Sets the raw data file for the subject.
        Raises an exception if the given data type is wrong. 
        Keyword arguments:
        raw_data        -- the raw data file of the measured data
        """
        if (isinstance(raw_data, mne.fiff.Raw)):
            self._raw_data = raw_data
        else:
            raise Exception('Wrong data type')
        
    @property
    def subject_name(self):
        """
        Returns the subject_name of the subject.
        """
        return self._subject_name
    
    @subject_name.setter
    def subject_name(self, subject_name):
        """
        Sets the subject_name for the subject.
        """
        self._subject_name = subject_name
        
    @property
    def subject_path(self):
        """
        Returns the subject_path of the subject.
        """
        return self._subject_path
    
    @subject_path.setter
    def subject_path(self, subject_path):
        """
        Sets the subject_path for the subject.
        """
        self._subject_path = subject_path
                
    @property
    def working_file(self):
        """
        Returns the current working file.
        """
        return self._working_file
    
    @working_file.setter
    def working_file(self, fname):
        """
        Sets the current working file and notifies the main window to show it.
        Keyword arguments:
        fname         -- Name of the new working file.
        """
        self._working_file = mne.fiff.Raw(fname, preload=True)
        self.working_file_path = fname

    def save_raw(self, file_name, path):
        """
        Saves the raw data file into the subject directory.
        Keyword arguments:
        file_name      -- the full path and name of the chosen raw data file
        path           -- path to the experiment directory
        """
        # See old version in save_raw method of original experiment.
        try:
            os.mkdir(path)
        except OSError:
            raise Exception('No rights to save to the chosen path or' + 
                            ' subject/experiment name already exists')
            return
        
        
        if os.path.exists(path):
            mne.fiff.Raw.save(self._raw_data, path + '/' + \
                              str(os.path.basename(file_name)))
            self.create_epochs_directory()
        else:
            raise Exception('No rights to save the raw file to the chosen ' + 
                            'path or bad raw file name.')
        
    def create_epochs_directory(self):
        """Create a directory for saving epochs under the subject directory.
        """
        try:
            #self.epochs_directory = self.subject_path + 'epochs/'
            os.mkdir(self._epochs_directory)
        except OSError:
            raise OSError('no rights to save to the chosen path')                
    
    def create_event_set(self):
        """
        Creates an event set where the first element is the id
        and the second element is the number of the events.
        Raises type error if the raw_data attribute is not set or
        if the data is not of type mne.fiff.Raw.
        """
        if not isinstance(self._raw_data, mne.fiff.Raw):
            raise TypeError('Nt a raw object')
        if self.stim_channel == None:
            return
        events = mne.find_events(self._raw_data,
                                 stim_channel=self._stim_channel)
        bins = np.bincount(events[:,2]) #number of events stored in an array
        d = dict()
        for i in set(events[:,2]):
            d[i] = bins[i]
        self._event_set = d