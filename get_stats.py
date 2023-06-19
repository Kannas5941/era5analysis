# %% Defining the different packages
from windrose import WindroseAxes, WindAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os, sys

# %% Getting the statistics of the data


def get_stats(data, analysis):
    """
    This Function is used to get the statistical data of the inputs.

    Inputs
    -------
    data : the data that you want to analyze.
    analysis : (String)
               For either timeseries (dataframe) or spatial data (3d-dataset)

    Returns
    -------
    Mean
    Max
    Min
    Std. Deviation
    """
    file_path = os.path.realpath(__file__)  # script full name
    current_dir = os.path.dirname(file_path)  # script directory
    os.chdir(current_dir)
    # Get the stats based on inputs
    if analysis == 'time_series':
        statistics = data.describe()
        print(statistics)
        return statistics
    else:
        ds_max = data.max()
        ds_mean = data.mean()
        ds_min = data.min()
        ds_std = data.std()
        statistics = ['max', ds_max, 'mean',
                      ds_mean, 'min', ds_min, 'std', ds_std]
        print(statistics)
        return statistics

# %% Plotting the data

def plot_windrose(data, analysis, lat=None, lon=None):
    """   
    This function give the wind rose of the data.

    Inputs
    -------
    data : The data set that needs to be assessed.
    Lat : Lattitude value (int/float)
    Long: Longitude value (int/float)     

    Returns
    -------
    Wind Speed : at 10m and 100m.
    WInd Direction : at 10m and 100m.
    Wind Frequency : at 10m and 100m.
    Wind Rose graph: at 10m and 100m height.
    Wind Frequency : at 10m and 100m height.
    """
    file_path = os.path.realpath(__file__)  # script full name
    current_dir = os.path.dirname(file_path)  # script directory
    os.chdir(current_dir)
    # Extract the data
    if analysis == 'time_series':
        WS10m = data.WS10m
        WS100m = data.WS100m
        WD10m = data.WD10m
        WD100m = data.WD100m
        title10 = 'Wind Rose at the height of 10m'
        title100 = 'Wind Rose at the height of 100m'

    elif analysis == 'spatial':
        WS10m = data.WS10m.sel(latitude=lat, longitude=lon, method='nearest')
        WS100m = data.WS100m.sel(latitude=lat, longitude=lon, method='nearest')
        WD10m = data.WD10m.sel(latitude=lat, longitude=lon, method='nearest')
        WD100m = data.WD100m.sel(latitude=lat, longitude=lon, method='nearest')
        title10 = f'Wind Rose at the height of 10m in lat = {lat} and long = {lon}'
        title100 = f'Wind Rose at the height of 100m in lat = {lat} and long = {lon}'

    # Plotting wind Roses for 10m height.
    ax = WindroseAxes.from_ax()
    ax.bar(WD10m, WS10m, normed=True, opening=0.8, edgecolor='black')
    ax.set_legend()
    ax.set(title=title10)

    ax.set_legend()
    plt.savefig('../docs/windrose_10m.png', dpi=300)

    # Plotting wind Roses for 100m height.
    ax = WindroseAxes.from_ax()
    ax.bar(WD100m, WS100m, normed=True, opening=0.8, edgecolor='black')
    ax.set(title=title100)
    ax.set_legend()
    plt.savefig('../docs/windrose_100m.png', dpi=300)


def plot_timeseries(df):
    """
    This function is to plot the timeseries of the data.

    Inputs
    -------
    The dataframe.    

    Returns
    -------
    Timeseries at 10m and 100m height.    
    """
    file_path = os.path.realpath(__file__)  # script full name
    current_dir = os.path.dirname(file_path)  # script directory
    os.chdir(current_dir)
    
    fig, axs = plt.subplots(1, 1, num=1, clear=True, figsize=(10, 5))
    ax = axs
    ax.plot(df.index, df.WS10m, label='10m')
    ax.plot(df.index, df.WS100m, label='100m')
    ax.set(title='Wind Speed at 10 and 100 meters',
           xlabel='Date', ylabel='Wind Speed [m/s]')
    ax.legend()
    ax.grid()
    plt.xticks(rotation=60)
    plt.show()
    fig.savefig('../docs/time_series.png', dpi=300)


def plot_spatial_map(ds):
    """
    This function is used to plot the map of the 100 m wind speed data.

    Inputs
    ----------
    data   : The dataframe.
    WSdata : either WS10m or WS100m data.

    Returns
    -------
    Maps of wind speed at 10 and 100 meters over the area of interest.
    """
    file_path = os.path.realpath(__file__)  # script full name
    current_dir = os.path.dirname(file_path)  # script directory
    os.chdir(current_dir)
    
    fig, axs = plt.subplots(1, 2, clear=True, figsize=(10, 6))
    ds.WS10m.mean('time').plot(cmap='jet', ax=axs[0])
    ds.WS100m.mean('time').plot(cmap='jet', ax=axs[1])
    fig.tight_layout()
    plt.show()
    fig.savefig('../docs/spatial_map.png', dpi=300)


def plot_spatial_timeseries(ds, lat, lon):
    """
    This function is used to get the timeseries of a place (lat,lon) from the spatial data.

    Inputs
    ----------
    lat : int/float
        This is the lattidue of the desired location.
    lon :int/float
        This is the longitude of the desired location.

    Returns
    -------
    Timeseries of the particular location.
    """
    file_path = os.path.realpath(__file__)  # script full name
    current_dir = os.path.dirname(file_path)  # script directory
    os.chdir(current_dir)

    ds_ts_10 = ds.WS10m.sel(latitude=lat, longitude=lon, method='nearest')
    ds_ts_100 = ds.WS100m.sel(latitude=lat, longitude=lon, method='nearest')

    fig, ax = plt.subplots(1, 1, clear=True, figsize=(10, 5))
    ds_ts_10.plot(ax=ax, label='WS10m')
    ds_ts_100.plot(ax=ax, label='WS100')
    ax.set(xlabel="Time", ylabel="Wind Speed [m/s]")
    ax.legend()
    ax.grid(True)
    plt.show()
    fig.savefig('../docs/spatial_time_series.png', dpi=300)


def plot_pdf_ts(df):
    """
    This function gives the plot of the probability density 
    of a time series.

    Inputs
    ----------
    df (object) : Time series Dataframe.

    Returns
    -------
    Plot of the pdf
    Parameters of the pdf function.

    """
    file_path = os.path.realpath(__file__)  # script full name
    current_dir = os.path.dirname(file_path)  # script directory
    os.chdir(current_dir)
    
    height = 10
    ax = WindAxes.from_ax()  
    
    bins = np.arange(0, df['WS{}m'.format(height)].max() + 1, 0.5)
    bins = bins[1:]
    ax, params = ax.pdf(df['WS{}m'.format(height)], bins=bins)
    plt.title('PDF for 10m')
    plt.xlabel('Wind Speed [m/s]')
    plt.ylabel('Probability [%]')
    plt.savefig('../docs/pdf_{}.png'.format(height), dpi=300)

    height = 100
    ax = WindAxes.from_ax()
    bins = np.arange(0, df['WS{}m'.format(height)].max() + 1, 0.5)
    bins = bins[1:]
    ax, params = ax.pdf(df['WS{}m'.format(height)], bins=bins)
    plt.title('PDF for 100m')
    plt.xlabel('Wind Speed [m/s]')
    plt.ylabel('Probability [%]')
    plt.savefig('../docs/pdf_{}.png'.format(height), dpi=300)
