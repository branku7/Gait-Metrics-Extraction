from matplotlib import pyplot as plt
import numpy as np

def normalize(dg):
    """
    Helper function to normalize data before plotting it. Uses (data-average)/std
    """
    return (dg-np.average(dg))/np.std(dg)

def visualize_signal(legend, title, *args, **kwargs):
    """
    Function to visualize the IC and FC detection both before and after optimization.
    * *args should be the different plots to visualize, normaly, both continuous wavelet tranformations and possibly the variations of the axis accelerations or velocities
    * **kwargs can have the plots of the cwt(s) and the respective index for IC and FC
    """
    plt.figure(figsize=(10,8))
    for arg in args:
        plt.plot(range(len(arg)), normalize(arg))
    for event, values in kwargs.items():
        if event == 'FC':
            plt.plot(values[0], values[1], 'bo', markersize = 7)
        elif event == 'IC':
            plt.plot(values[0], values[1], 'rx', markersize = 10)
    plt.legend(legend)
    plt.ylabel('m/s (normalized)')
    plt.xlabel('0.01 seconds')
    plt.title(title)