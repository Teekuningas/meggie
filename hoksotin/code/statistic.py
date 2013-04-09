# coding: latin1

"""
Created on Mar 14, 2013

@author: Jaakko Leppäkangas
"""
import numpy as np
import sys

from IntegralImage import IntegralImage

class Statistic(object):
    """
    A class for statistical operations.
    """


    def __init__(self):
        pass
        
    def find_minimum(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns the last minimum and its time for a
        one dimensional numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency in Hz
        arr           -- 1d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """        
        twindow, start = self.timewindow_to_samplewindow(sfreq, arr,
                                                         tmin, tmax)
        time = (np.argmin(twindow)+ start) * 1000 / sfreq
        return np.min(twindow), time
        
    def find_minimum2d(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns an array of last minimums for a 2d array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency in Hz
        arr           -- 2d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        return [self.find_minimum(sfreq, row, tmin, tmax) for row in arr]
        
    def find_maximum(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns the last maximum and its time for a 1d numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency in Hz
        arr           -- 1d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        twindow, start = self.timewindow_to_samplewindow(sfreq, arr,
                                                         tmin, tmax)
        time = (np.argmax(twindow) + start) * 1000 / sfreq 
        return np.max(twindow), time
    
    def find_maximum2d(self, sfreq, arr, tmin=0.0, tmax=sys.float_info.max):
        """
        Returns an array of maximums for a 2d array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency in Hz
        arr           -- 2d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        return [self.find_maximum(sfreq, row, tmin, tmax) for row in arr]
    
    def find_half_maximum(self, sfreq, arr, tmin=0.0,
                          tmax=sys.float_info.max):
        """
        Returns half maximum for a 1d numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency in Hz
        arr           -- 1d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        (max, time) = self.find_maximum(sfreq, arr, tmin, tmax)
        return (max/2, time)
    
    def find_half_maximum2d(self, sfreq, arr, tmin=0.0,
                            tmax=sys.float_info.max):
        """
        Returns half maximums for a 2d numpy array.
        
        Keyword arguments:
        sfreq         -- Sampling frequency in Hz
        arr           -- 2d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        """
        return [self.find_maximum(sfreq, row, tmin, tmax)/2 for row in arr]
    
    def find_maximum_intensity(self, mat, w, h):
        """
        Takes a matrix and finds the coordinates of a 
        window for maximum intensity. In case of many
        equal maximums, the first one is returned.
        
        Keyword arguments:
        mat           -- A matrix
        w             -- Width of the window
        h             -- Height of the window
        """
        if w > len(mat[0]) or h > len(mat):
            raise Exception('Out of bounds.')
        max = 0
        xcoord = 0
        ycoord = 0
        i = IntegralImage()
        """
        Goes through the original matrix and finds the window with highest
        intensity.
        """
        for y in range(len(mat) - h+1):
            for x in range((len(mat[0]) - w)+1):
                #create a new matrix with the size of the window
                newmat = mat[y:h+y,x:w+x]
                #temporary variable to help finding the maximum
                a = i.sum_over_rectangular_area((0,0), (w-1,h-1), newmat)
                """ Save coordinates if a new maximum is found """
                if a > max:
                    xcoord = x
                    ycoord = y
                    max = a
        print max
        return max, xcoord, ycoord
    
    def timewindow_to_samplewindow(self, sfreq, arr, tmin, tmax):
        """
        Converts time window in milliseconds to samples.
        Returns the time window in samples and the starting sample.
        
        Keyword arguments:
        sfreq         -- Sampling frequency
        arr           -- 1d numpy array
        tmin          -- Start of the time window in milliseconds
        tmax          -- End of the time window in milliseconds
        Raises an exception if the sampling frequency is zero.
        Raises an exception if the array is empty.
        """
        if sfreq <= 0:
            raise Exception('Sampling frequency cannot be zero.')
        if arr == []:
            raise Exception('No data found.')
        start = int(round((tmin/1000)*sfreq))
        stop = int(round((tmax/1000)*sfreq))+1
        return arr[start:stop], start
        
    
def main():
    s = Statistic()
    m = np.array([[1,1,1,1,1],
                  [2,2,2,2,2],
                  [3,3,3,3,3],
                  [4,5,9,7,8]])
    max = s.find_maximum_intensity(m, 2, 3)
    print max
     
if __name__ == "__main__":
    main()