#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %%
from era5analysis import era5_funcs, get_stats, get_report
# BASIC PYTHON LIB
import numpy as np
import matplotlib.pylab as plt
import os
import numpy as np
# Imports Wind Turbine class from Pywake
from py_wake.wind_turbines import WindTurbines


# %% Generating Power and Thrust curves of a wind turbine
def PT(path, filename):
    '''
    This function generates power and thrust co efficient curves for the user
     desired Wind turbine. The input file needs to be WaSP file(.WTG)

    Parameters
    ----------
    path(str) : Path for the filename
        DESCRIPTION.
    filename(str) : .WTG Filename in the specified path
        DESCRIPTION.

    Returns
    -------
    Wind turbine generator object variable.

    '''
    file_path = os.path.realpath(__file__)  # script full name
    current_dir = os.path.dirname(file_path)  # script directory
    os.chdir(current_dir)
    wtg_file = os.path.join(path, filename)  # joins the path and filename
    wt_wtg = WindTurbines.from_WAsP_wtg(wtg_file)  # reads  .wtg file
    ws = np.arange(4, 25)  # windspeed
    ct = wt_wtg.ct(ws)  # Thrust coefficient values taken from wtg object
    power = wt_wtg.power(ws)  # Power values
    # Plot Power and Thrust curve in the same plot
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    plt.xlabel('Wind speed [m/s]')
    ax.plot(ws, power)
    ax2.plot(ws, ct)
    # giving labels to the axes
    ax.set_xlabel('Wind speed [m/s]', fontsize=15)
    ax.set_ylabel('Power [kW]', fontsize=15)
    # secondary y-axis label
    ax2.set_ylabel('Ct[-]', fontsize=15)
    # defining display layout
    ax.grid(True)
    plt.title('Power and Thrust Coefficient Curve', fontsize=15)
    plt.show()
    return wt_wtg


# %% Calculate AEP for specified wind turbine and wind speed data
def AEP(data, analysis, vref, PT, lat=None, lon=None):
    '''
    This function calculates Annual Energy production of user defined Turbine
    at an arbitary location for the given wind speed data.

    Parameters
    ----------
    data : User specified wind speed data
    analysis (str): Type of analysis to be carried out either
    time_series/spatial
    vref : Reference wind speed for wind class I,II,III- 50,42.5,37.5

    Returns
    -------
    None.

    '''
    file_path = os.path.realpath(__file__)  # script full name
    current_dir = os.path.dirname(file_path)  # script directory
    os.chdir(current_dir)
    wt_wtg = PT
    # Extract the data
    if analysis == 'time_series':
        WS10m = np.sort(data.WS10m)
        WS100m = np.sort(data.WS100m)
        power10m = wt_wtg.power(WS10m)  # Explicitly taken from the PT func
        power100m = wt_wtg.power(WS100m)
        # calculate the annual energy production
        v_ave = 0.2*vref  # v_ave=0.2*vref
        hrs_per_year = 365 * 24  # hours per year
        dvj10m = WS10m[1] - WS10m[0]  # assuming even bins!
        dvj100m = WS100m[1] - WS100m[0]  # assuming even bins!
        probs10m = (np.exp(-np.pi*((WS10m - dvj10m/2) / (2*v_ave))**2)
                  - np.exp(-np.pi*((WS10m + dvj10m/2) / (2*v_ave))**2))  # prob of wind
        probs100m = (np.exp(-np.pi*((WS100m - dvj100m/2) / (2*v_ave))**2)
                  - np.exp(-np.pi*((WS100m + dvj100m/2) / (2*v_ave))**2))  # prob of wind
        aep10m = hrs_per_year * sum(probs10m * power10m)  # sum weighted power and convert to AEP (Wh)
        aep100m = hrs_per_year * sum(probs100m * power100m)  # sum weighted power and convert to AEP (Wh)
        print(f'The AEP for wind speed at height of 10mts: {aep10m/(1e6):.1f} MWh')
        print(f'The AEP for wind speed at height of 100mts: {aep100m/(1e6):.1f} MWh')
        # make the plot
        fig, ax1 = plt.subplots(1, 1, num=1, figsize=(7, 3), clear=True)
        plt.plot(WS10m, power10m, 'or', mec='0.2', ms=7, alpha=0.7, zorder=11, label='Wind speed 10m')  # bin-average
        plt.plot(WS100m, power100m, 'ob', mec='0.2', ms=7, alpha=0.7, zorder=11, label='Wind speed 100m')  # bin-average
        plt.grid('on')
        plt.xlabel('Wind speed [m/s]')
        plt.ylabel('Electric Power [w]')
        plt.legend()
        plt.title('Power and AEP generated for each wind speed', fontsize=15)
        plt.tight_layout()
        plt.show()
    elif analysis == 'spatial':
        WS10m = data.WS10m.sel(latitude=lat, longitude=lon, method='nearest')
        WS10m = WS10m.values
        WS100m = data.WS100m.sel(latitude=lat, longitude=lon, method='nearest')
        WS100m = WS100m.values
        power10m = wt_wtg.power(WS10m)
        power10m = power10m
        power100m = wt_wtg.power(WS100m)
        power100m = power100m
        # calculate the annual energy production
        v_ave = 0.2*vref  # v_ave=0.2*vref
        hrs_per_year = 365 * 24  # hours per year
        dvj10m = WS10m[1] - WS10m[0]  # assuming even bins!
        dvj100m = WS100m[1] - WS100m[0]  # assuming even bins!
        probs10m = (np.exp(-np.pi*((WS10m - dvj10m/2) / (2*v_ave))**2)
                  - np.exp(-np.pi*((WS10m + dvj10m/2) / (2*v_ave))**2))  # prob of wind
        probs100m = (np.exp(-np.pi*((WS100m - dvj100m/2) / (2*v_ave))**2)
                  - np.exp(-np.pi*((WS100m + dvj100m/2) / (2*v_ave))**2))  # prob of wind
        aep10m = hrs_per_year * sum(probs10m * power10m)  # sum weighted power and convert to AEP (Wh)
        aep100m = hrs_per_year * sum(probs100m * power100m)  # sum weighted power and convert to AEP (Wh)
        print(f'The AEP for wind speed at height of 10mts: {abs(aep10m)/(1e6):.1f} MWh')
        print(f'The AEP for wind speed at height of 100mts: {abs(aep100m)/(1e6):.1f} MWh')
        # make the plot
        fig, ax1 = plt.subplots(1, 1, num=1, figsize=(7, 3), clear=True)
        plt.plot(WS10m, power10m, 'or', mec='0.2', ms=7, alpha=0.7, zorder=11, label='Wind speed 10m')  # bin-average
        plt.plot(WS100m, power100m, 'ob', mec='0.2', ms=7, alpha=0.7, zorder=11, label='Wind speed 100m')  # bin-average
        plt.grid('on')
        plt.xlabel('Wind speed [m/s]')
        plt.ylabel('Electric Power [w]')
        plt.legend()
        plt.title('Power and AEP generated for each wind speed', fontsize=15)
        plt.tight_layout()
        plt.show()
    return
