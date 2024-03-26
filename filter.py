import numpy as np
import pandas as pd


def smooth(data, window=100, start_index=0):
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
    pad_width = window // 2  # Number of values to pad on each side
    padded_data = np.pad(data, (pad_width, pad_width), mode='edge')  # Pad using edge values
    a = np.convolve(padded_data, np.ones(window)/window, mode='same')  # Use 'same' mode for convolution
    return np.pad(a, (start_index, 0), 'constant', constant_values=(0, 0))



def add_smoothed_cols(ddict, window=100, verbose=False, inPlace=True):
    """
    Create a new column for each accelerometer column in the data dictionary with the smoothed data.

    Parameters
    ----------
    ddict : dict
        The data dictionary to be modified.
    window : int
        The window size for the smoothing algorithm.
    verbose : bool
        Whether or not to print out the columns that are being added.
    inPlace : bool
        Whether or not to modify the dictionary in place.

    Returns
    -------
    dict
        The modified data dictionary.
    """
    if not inPlace:
        ddict = ddict.copy()
    for t_type in ddict:
        for csvf in ddict[t_type]:
            try:
                for dir in ddict[t_type][csvf]:
                    for col in ddict[t_type][csvf][dir].columns:
                        if "acc_" in col:
                            d = ddict[t_type][csvf][dir][col]
                            ddict[t_type][csvf][dir][col + "_smooth"] = smooth(d, window=window)[:len(d)]
                            if verbose:
                                print("Added", col + "_smooth")
            except TypeError:
                continue
    return ddict



def add_diff_cols(ddict, verbose=False, inPlace=True):
    """
    Create a new column for each lat/long/elevation column in the data dictionary with the difference data.

    Parameters
    ----------
    ddict : dict
        The data dictionary to be modified.
    verbose : bool
        Whether or not to print out the columns that are being added.
    inPlace : bool
        Whether or not to modify the dictionary in place.

    Returns
    -------
    dict
        The modified data dictionary.
    """
    if not inPlace:
        ddict = ddict.copy()
    names = ["latitude", "longitude", "elevation"]
    for t_type in ddict:
        for csvf in ddict[t_type]:
            try:
                for dir in ddict[t_type][csvf]:
                    for col in ddict[t_type][csvf][dir].columns:
                        if any(element in col for element in names):
                            d = ddict[t_type][csvf][dir]

                            # this is the only thing going on in this function
                            # print(d.shape)
                            # prepend a zero
                            d["d_" + col] = np.insert((np.diff(d[col])), 0, 0)
                            d["meters_" + col] = np.cumsum(d["d_" + col])

                            if verbose:
                                print("Added", "d_" + col)
                                print("Added", "meters_" + col)
            except TypeError:
                continue
    return ddict


def toMeters(data, col):
    """
    Convert the data from degrees to meters using the haversine metric.

    Parameters
    ----------
    data : 1D array
        The input data.
    
    Returns
    -------
    1D array
        The data in meters.
    """
    R = 6371000  # Radius of the Earth in meters
    if col == "elevation":
        return data
    return np.deg2rad(data) * R

def total_distance(data):
    """
    Compute the total distance traveled so far using the difference column (in meters)

    If the first two values are 1, 2, then the total distance so far col is 1, 3.
    """
    return np.cumsum(data)