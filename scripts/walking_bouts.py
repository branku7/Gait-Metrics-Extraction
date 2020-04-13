import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os
from scripts.signal_processing import butter_bp_data
from scripts.visualization import showCharts


def applyOffsetRemove(df):
    df[1] = np.subtract(df[1], np.average(df[1]))
    df[2] = np.subtract(df[2], np.average(df[2]))
    df[3] = np.subtract(df[3], np.average(df[3]))


def applyFilter(df):
    fs = 100 # Hz
    lower_than = 17 # Hz
    order = 2
    df = butter_bp_data(df, lower_than, fs, order, 'low')


def runWalkingBoutDetection(
    data,
    mean_threshold = 0.05,
    ssd_threshold = 0.1,
    windowSize = 10
    ):

    print ("started window")
    df1, df2 = comb_std_rolling(data, windowSize) #ssd and mean av
    ranges_ww = calcSegments(df1, df2, mean_threshold,ssd_threshold)
    showCharts(ranges_ww, df1, df2, mean_threshold, ssd_threshold)
    return ranges_ww


def calcSegments(
    data_std,
    data_mean,
    mean_threshold,
    ssd_threshold
    ):

    """
    This function provides the ranges that satisfy the
    threshold conditions.
    """
    Ln = len(data_std)
    walking_window = np.zeros(Ln)
    ranges = list()
    start = 0
    end = 0
    contiguous = False

    # Mark the ranges that satisfy a certain condition
    for i in range(0,Ln):
        if (data_std[i] >= ssd_threshold and \
        (data_mean[i] >= mean_threshold or data_mean[i] <= -mean_threshold )):
            walking_window[i] = 1


    for i in range(0,Ln):
        if (i == Ln - 1) and contiguous:
            end = i - 1
            ranges.append((start,end))
        if walking_window[i] == 1:
            if not contiguous:
                contiguous = True
                start = i
        elif (walking_window[i] == 0 ) and contiguous:
            contiguous = False
            end = i - 1
            ranges.append((start,end))

    # Here we are filtering all the ranges that have
    # less than 50 centiseconds

    for i in range(0,len(ranges)):
        start = ranges[i][0]
        end = ranges[i][1]
        len_wb = end - start
        if (len_wb < 50):
            walking_window[start:end] = [0]*len_wb

    ranges = list()
    start = 0
    end = 0
    contiguous = False
    for i in range(0,Ln):
        if (i == Ln - 1) and contiguous:
            end = i
            ranges.append((start,end))
        if walking_window[i] == 1:
            if not contiguous:
                contiguous = True
                start = i
        elif walking_window[i] == 0 and contiguous:
            contiguous = False
            end = i-1
            ranges.append((start,end))
    return ranges


def comb_std_rolling (data, window):
    """
    This function will perform a rolling window for combined std and mean value
    of several axis.
    """

    data_combined1 = data[1].rolling(window).std()
    data_combined2 = data[2].rolling(window).std()
    data_combined3 = data[3].rolling(window).std()
    arr = np.array([
        data_combined1.tolist(),
        data_combined2.tolist(),
        data_combined3.tolist()
        ])
    data_combined = arr.sum(axis = 0)
    data_combined = data_combined[window-1:len(data_combined)]

    # data[1] for vertical, data[3] for posterior, data[2] for mediolateral
    data_mean = data[3].rolling(window).mean()
    data_mean = data_mean[window-1:len(data_mean)].tolist()

    return data_combined, data_mean