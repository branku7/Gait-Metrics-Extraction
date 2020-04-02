from scipy import signal
from scipy import integrate
from scipy import constants
import numpy as np
import pandas as pd

def H_V_orth_sys(data,flip=False):
    """
    Considers 3 axis from an accelerometer tilted. This function fixes the values of all axis by assuming that the normal value of acceleration is +1g in the vertical axis.
    In case the device is flipped upside down, flip should be turned to True
    """
    # In case the AX3 is used upside down

    if flip:
        data.loc[:,1:3] = -data[1:3]

    # Get the tilted angles

    a2 = np.mean(data[2])
    a3 = np.mean(data[3])
    theta1 = np.arcsin(a2)
    theta2 = np.arcsin(a3)  

    # Do the changes for each axis

    dg = np.asarray(data)
    new_time_series = list()
    
    for row in dg:
        aA = row[3]*np.cos(theta2) - row[1]*np.sin(theta2)
        aV_ = row[3]*np.sin(theta2) + row[1]*np.cos(theta2)
        aM = row[2]*np.cos(theta1) - aV_*np.sin(theta1)
        aV = row[2]*np.sin(theta1) + aV_*np.cos(theta1) - 1
        new_time_series.append([row[0],aV,aM,aA])

    # Transform into dataframe

    timeseries_df = pd.DataFrame(new_time_series)
    return timeseries_df

def detrend_data(*args):
    """
    This function uses the signal scipy function to detrend the various 1-dim arrays contained in our dataset. It applies to the x,y,z axis of the accelerometer
    """
    for array in args:
        array = signal.detrend(array)
    return None

def butter_bandpass(cut, fs, order, btype):
    """
    A function which created a filter. It can be a bandpass, lowpass or highpass filter to apply for signal. It makes use of the signal class of the scipy package.
        *cut: frequency value which will serve to cut the signal
        *fs: frequency of the signal
        *order: from 1 to N it changes the way the signal is filtered
        *btype: 'bandpass', 'low' or 'high'
    """
    nyq = 0.5 * fs
    high_low = cut / nyq
    b, a = signal.butter(order, high_low, btype)
    return b, a

def butter_bandpass_filter(data, cut, fs, order = 4, btype = 'low'):
    """
    This function employs the butter_bandpass to a dataset. It has some default values which are mainly used in this project.
    """
    b, a = butter_bandpass(cut, fs, order, btype)
    y = signal.filtfilt(b, a, data)
    return y

def butter_bp_data(*args,lower_than,fs,order,btype):
    """
    This function applies the bandpass to a dataset with 4 dimensions, supposing that the 1st is the time dimension.
    """
    for array in args:
        array = butter_bandpass_filter(array, lower_than, fs, order, btype)
    return None

def integrate_Hz(data,Hz = 100, change_unit = False):
    """
    This function uses integrate package to integrate through cummulative trapezoids over the dataset period.
    Hz is the unit of time that we want to integrate over, change_unit is in case we want to change from g to m/s**2
    """
    if change_unit:
        data = np.multiply(data,constants.g)
    return integrate.cumtrapz(data,np.array(range(len(data)))/Hz, initial=0)