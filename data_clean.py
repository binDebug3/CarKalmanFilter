from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os

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

    for col in bad_cols + useless_cols:
        if col in df.columns:
            df = df.drop(columns=[col])
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

# Function to convert OHE to label
def ohe_to_label(df_in, classes, df_out, class_name):
    conditions = []
    for r in classes:
        conditions.append(df_in[r] == 1)
    df_out[class_name] = np.select(conditions, classes)
    return df_out

