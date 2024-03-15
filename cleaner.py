# imports
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os



def print_structure(csvs, level=0):
    """
    Recursively print the structure of the csvs dictionary

    Parameters:
    csvs (dict): The dictionary to print the structure of
    level (int): The current level of recursion

    Returns:
    None
    """
    for key in csvs.keys():
        print("\n", "\t"*level, key, end=": ")
        if isinstance(csvs[key], dict):
            print_structure(csvs[key], level+1)
        else:
            if type(csvs[key]) == list:
                print(len(csvs[key]), end="")
            elif type(csvs[key]) == pd.DataFrame:
                print(csvs[key].shape, end="")
            else:
                print(type(csvs[key]), end="")



def clean_dict(ddict, verbose=False):
    """
    Clean the data in the dictionary by dropping bad rows and columns

    Parameters
    ----------
    ddict : dict
        The dictionary of dataframes
    verbose : bool
        Whether or not to print out verbose information
    
    Returns
    -------
    dict
        The cleaned dictionary
    """
    # everything here is just navigating the dictionary
    for t_type in ddict:
        for csvf in ddict[t_type]:
            dff = ddict[t_type][csvf]
            if dff is not None:
                if "left" in csvf or "right" in csvf:
                    for folder in dff:
                        dff[folder] = clean_acc(dff[folder])        # this is the only interesting line
                        if verbose:
                            print("cleaned", t_type, csvf, folder)
                elif "t_gps" in csvf:
                    for folder in dff:
                        dff[folder] = clean_gps(dff[folder])        # this is the only other interesting line
                        if verbose:
                            print("cleaned", t_type, csvf, folder)

    return ddict



def clean_gps(df):
    """
    Clean the gps data by dropping bad rows and columns

    Parameters
    ----------
    df : pd.DataFrame
        The gps data
    
    Returns
    -------
    pd.DataFrame
        The cleaned gps data
    """
    bad_cols = ['ageofdgpsdata', "dgpsid", "activity", "annotation"]
    useless_cols = ['hdop', 'vdop', 'pdop', "satellites", "geoidheight"]

    # drop bad columns and rows
    for col in bad_cols + useless_cols:
        if col in df.columns:
            df = df.drop(columns=[col])
    
    # drop rows with bad data and return
    df = df.dropna()
    return df


def clean_acc(dirty_df):
    """
    Clean the accelerometer data by dropping bad rows and columns

    Parameters
    ----------
    left : pd.DataFrame
        The left accelerometer data
    right : pd.DataFrame
        The right accelerometer data

    Returns
    -------
    pd.DataFrame
        The cleaned accelerometer data
    """
    useless_cols = ["temp_dash", "temp_above", "temp_below"]
    for col in useless_cols:
        if col in dirty_df.columns:
            dirty_df = dirty_df.drop(columns=[col])
    
    for col in dirty_df.columns:
        if "mag" in col:
            dirty_df = dirty_df.drop(columns=[col])
    
    # remove the word "suspect" from the columns
    dirty_df.columns = dirty_df.columns.str.replace("_suspension", "")
    dirty_df.columns = dirty_df.columns.str.replace("dashboard", "dash")

    dirty_df = dirty_df.dropna()
    
    return dirty_df


def combine_data(dfs):
    """
    Combine the data into one dataframe by merging on the timestamp column

    Parameters
    ----------
    dfs : list
        A list of dataframes to combine
    
    Returns
    -------
    pd.DataFrame
        The combined dataframe
    """
    df = dfs[0]
    for i in range(1, len(dfs)):
        # merge the dataframes on timestamp
        df = pd.merge(df, dfs[i], on="timestamp")
    return df



def ohe_to_label(df_in, classes, df_out, class_name):
    """
    Convert one hot encoded data to label data

    Parameters
    ----------
    df_in : pd.DataFrame - The input dataframe
    classes : list - The list of classes
    df_out : pd.DataFrame - The output dataframe
    class_name : str - The name of the class column

    Returns
    -------
    pd.DataFrame - The output dataframe
    """
    conditions = []
    for r in classes:
        # create a condition for each class
        conditions.append(df_in[r] == 1)

    # create a list of the classes
    df_out[class_name] = np.select(conditions, classes)
    return df_out



def load_data(parent=".data", exclude_test=[], exclude_val=[], verbose=False):
    """
    Load all data from the given parent directory. The data is expected to be in the following format:
    parent
    ├── folder1
    │   ├── t_gps.csv
    │   ├── gps_mpu_left.csv
    │   ├── gps_mpu_right.csv
    │   └── labels.csv
    ├── folder2
    etc.

    The function will load all csv files into a dictionary of dataframes. The dictionary will be in the following format:
    {
        "train": {
            "t_gps": {folder1: df, folder2: df, ...},
            "gps_mpu_left": {folder1: df, folder2: df, ...},
            "gps_mpu_right": {folder1: df, folder2: df, ...},
            "labels": {folder1: df, folder2: df, ...},
            "folders": [folder1, folder2, ...]
        },
        "val": {
            "t_gps": {folder1: df, folder2: df, ...},
            ...
        },
        "test": {
            "t_gps": {folder1: df, folder2: df, ...},
            ...
        }
        "folders": [folder1, folder2, ...]
    }

    The function will also exclude any folders that are in the exclude_test or exclude_val lists. 
    If verbose is set to True, the function will print out which files are being loaded into which data set.

    Parameters:
    parent (str): The parent directory of the data
    exclude_test (list): A list of folders to exclude from the test data
    exclude_val (list): A list of folders to exclude from the validation data
    verbose (bool): Whether or not to print out verbose information

    Returns:
    dict: A dictionary of dataframes in the format described above
    """
    # initialize data dictionary variables
    csvs = {"t_gps": None,
            "gps_mpu_left": None,
            "gps_mpu_right": None,
            "labels": None,
            "folders": None}
    folders = os.listdir(parent)
    data_dict = {"train": csvs.copy(), "val": csvs.copy(), "test": csvs.copy()}

    # set folders value
    data_dict["val"]["folders"] = exclude_val
    data_dict["test"]["folders"] = exclude_test
    data_dict["train"]["folders"] = [f for f in folders if f not in exclude_test and f not in exclude_val]

    # iterate through all folders
    for dir in folders:
        path = os.path.join(parent, dir)
        curr_csv = os.listdir(path)

        # decide which chain and which type of information
        for name in curr_csv:
            for file_type in csvs.keys():
                if file_type in name:

                    # load data
                    data = pd.read_csv(os.path.join(path, name))

                    # decide which train grouping
                    t_type = "train"
                    if dir in exclude_test:
                        t_type = "test"
                    elif dir in exclude_val:
                        t_type = "val"                        

                    # add to data in appropriate location
                    if data_dict[t_type][file_type] == None:
                        data_dict[t_type][file_type] = {dir: data}
                    elif dir in data_dict[t_type][file_type].keys():
                        continue
                    else:
                        data_dict[t_type][file_type][dir] = data
                    
                    # print out verbose information
                    if verbose:
                        print(f"Loaded {name} from {dir} into {t_type} data")

    return data_dict