#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 17:57:10 2022

@author: vikranthkanna
"""
# %%

from era5analysis import era5_funcs, get_stats, get_report,get_AEP

# BASIC PYTHON LIB
import numpy as np
import matplotlib.pylab as plt
import os
import numpy as np
import pandas as pd
# %%
data=pd.read_csv('../docs/ERA5_timeseries.csv')
path='../docs'
filename='GE_WIND_ENERGY_GE_750i_750 50_WAsP.wtg'
wt_wtg=get_AEP.PT(path,filename)
vref=37.5
WS10m = np.sort(data.WS10m)
WS100m = WS10m+1
power10m=wt_wtg.power(WS10m) #Explicitly taken from the Power Thrust function
power100m=wt_wtg.power(WS100m)
# calculate the average power for Wind speeds at 10m,100m
# wsp_unique10m = np.unique(WS10m)
# wsp_unique100m=np.unique(WS100m)
# wsp_unique10m=np.sort(WS10m)
# wsp_unique100m=np.sort(WS100m)
# pows10m=wt_wtg.power(wsp_unique10m)
# pows100m=wt_wtg.power(wsp_unique100m)
# pows10m = np.empty(wsp_unique10m.size)  # mean power at each wind speed
# pows100m= np.empty(wsp_unique100m.size)
# for j,vj in enumerate(wsp_unique10m):
#     wsp_pw10m = power10m[np.isclose(WS10m, vj)]
#     p10m = 1/wsp_pw10m.size  # probability of each simulation in the wsp bin is equal 1/nsim
#     pows10m[j] = sum(p10m * wsp_pw10m)
# for i,vi in enumerate(wsp_unique100m):
#     wsp_pw100m = power100m[np.isclose(WS100m, vi)]
#     p100m= 1/wsp_pw100m.size
#     pows100m[i] = sum(p100m * wsp_pw100m)

# calculate the annual energy production
v_ave = 0.2*vref  # v_ave=0.2*vref
hrs_per_year = 365 * 24  # hours per year
dvj10m = WS10m[1] - WS10m[0]  # assuming even bins!
dvj100m = WS100m[1] - WS100m[0]  # assuming even bins!
probs10m = (np.exp(-np.pi*((WS10m - dvj10m/2) / (2*v_ave))**2)
          - np.exp(-np.pi*((WS10m + dvj10m/2) / (2*v_ave))**2))  # prob of wind in each bin
probs100m = (np.exp(-np.pi*((WS100m - dvj100m/2) / (2*v_ave))**2)
          - np.exp(-np.pi*((WS100m + dvj100m/2) / (2*v_ave))**2))  # prob of wind in each bin
aep10m = hrs_per_year * sum(probs10m * power10m)  # sum weighted power and convert to AEP (Wh)
aep100m = hrs_per_year * sum(probs100m * power100m)  # sum weighted power and convert to AEP (Wh)
print(f'The AEP for wind speed at height of 10mts: {aep10m/(1e6):.1f} MWh')
print(f'The AEP for wind speed at height of 100mts: {aep100m/(1e6):.1f} MWh')
# make the plot
fig, ax1 = plt.subplots(1, 1, num=1, figsize=(7, 3), clear=True)
#plt.plot(wind, power, 'o', zorder=10)  # 10-min means
plt.plot(WS10m, power10m, 'or', mec='0.2', ms=7, alpha=0.7, zorder=11,label='Wind speed 10m')  # bin-average
plt.plot(WS100m, power100m, 'ob', mec='0.2', ms=7, alpha=0.7, zorder=11,label='Wind speed 100m')  # bin-average
plt.grid('on')
plt.xlabel('Wind speed [m/s]')
plt.ylabel('Electric Power [w]')
plt.legend()
plt.title('Power and Thrust Coefficient Curve',fontsize = 15)
plt.tight_layout()
plt.show()

# # calculate the average power in a wind speed binfor Windspeed at 100m
# wsp_unique = np.unique(WS100m)
# pows = np.empty(wsp_unique.size)  # mean power at each wind speed
# for j, vj in enumerate(wsp_unique):
#     # isolate the dels from each simulation
#     wsp_pows = power10m[np.isclose(WS100m, vj)]  # powers for that wind speed
#     p = 1/wsp_pows.size  # probability of each simulation in the wsp bin is equal 1/nsim
#     pows[j] = sum(p * wsp_pows)  

# # calculate the annual energy production
# v_ave = 0.2*vref  # v_ave=0.2*vref
# hrs_per_year = 365 * 24  # hours per year
# dvj = wsp_unique[1] - wsp_unique[0]  # assuming even bins!
# probs = (np.exp(-np.pi*((wsp_unique - dvj/2) / (2*v_ave))**2)
#           - np.exp(-np.pi*((wsp_unique + dvj/2) / (2*v_ave))**2))  # prob of wind in each bin
# aep = hrs_per_year * sum(probs * pows)  # sum weighted power and convert to AEP (Wh)
# print(f'The AEP for wind speed at height of 100 mts: {aep/(1e6):.1f} MWh')
# # make the plot
# fig, ax1 = plt.subplots(1, 1, num=1, figsize=(7, 3), clear=True)
# #plt.plot(wind, power, 'o', zorder=10)  # 10-min means
# plt.plot(wsp_unique, pows, 'or', mec='0.2', ms=7, alpha=0.9, zorder=11)  # bin-average
# plt.grid('on')
# plt.xlabel('Wind speed [m/s]')
# plt.ylabel('Electric Power [w]')
# plt.tight_layout()
# plt.show()