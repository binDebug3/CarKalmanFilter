import numpy as np
import pandas as pd

def smooth(data, window=10):
    """
    Compute the moving average of a 1D array using a given window size.

    Parameters
    ----------
    data : 1D array
        The input data.
    window : int
        The size of the moving average window.
    
    Returns
    -------
    1D array
        The smoothed data.
    """
    return np.convolve(data, np.ones(window)/window, mode='valid')