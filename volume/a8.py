# Assignment 8: Time Series
# Advanced Python for Streaming Analytics
# Julian McClellan
import pandas as pd

# Task 1: Load data
vpy_df = pd.read_csv("volume_per_year.csv")
vpy_df["Month"] = pd.to_datetime(vpy_df["Month"])
vpy_df.index = vpy_df["Month"]


# Task 2: Stationarity
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
ma = vpy_df["volume"].rolling(12).mean()
msd = vpy_df["volume"].rolling(12).std()

fig, ax = plt.subplots()
ax.plot(vpy_df.index, ma, color="green", label="Moving average: 1 year",
        linewidth=.7)
ax.plot(vpy_df.index, msd, color="red", label="Moving stddev: 1 year",
        linewidth=.7)
ax.plot(vpy_df.index, vpy_df["volume"], color="blue",
        label="Volume", linewidth=.7)
ax.set_xlabel("Time (Months)")
ax.set_ylabel("Volume")
ax.legend()
plt.show()

# Looking at the figure, it does look like the mean, variance, and
# autocorrelation structure change overtime.

# The null hypothesis of the Dickey-Fuller test is that in the equation
# delta(x_t) = pi * x_{t-1} + E_t (Where E_t ~ Normal), pi = 0
print(adfuller(vpy_df["volume"]))

# Looking at the results, I would fail to reject the null hypothesis that pi =
# 0, thus the data looks to be non-stationary and possess a unit root


# Task 3: Make a Time Series stationary
import numpy as np
vpy_df["logvolume"] = np.log(vpy_df["volume"])
vpy_df["mavolume"] = vpy_df["logvolume"].rolling(12).mean()
fig, ax = plt.subplots()
ax.plot(vpy_df.index, vpy_df["mavolume"], color="red", label="Log Volume Moving Average: 1 Year",
        linewidth=.7)
ax.plot(vpy_df.index, vpy_df["logvolume"], color="blue",
        label="Log Volume", linewidth=.7)
ax.set_xlabel("Time (Months)")
ax.set_ylabel("Log Volume")
ax.legend()
plt.show()

vpy_df["volume_without_trend"] = vpy_df["logvolume"] - vpy_df["mavolume"]
vol_wo_trend = vpy_df["volume_without_trend"][np.logical_not(np.isnan(vpy_df["volume_without_trend"]))]

# adfuller on volume without trend, but only the parts that are not NaNs
print(adfuller(vol_wo_trend))
# Looks like we can now reject (at the 5% level, the null hypothesis that there is a unit root)

ewma = vpy_df["logvolume"].ewm(12).mean()
print(adfuller(ewma))
# Now we can fail to reject the null that a unit root exists at a 5% confidence level


# Task 4 Removing trend and seasonality with differencing
vpy_df["logvol_dif1"] = vpy_df["logvolume"] - vpy_df["logvolume"].shift(1)
fig, ax = plt.subplots()
ax.plot(vpy_df.index, vpy_df["logvol_dif1"], color="blue", label="Log Volume Differenced (1)", linewidth=.7)
ax.set_xlabel("Time (Months)")
ax.set_ylabel("Log Volume Difference")
ax.legend()
plt.show()


# Task 5: Forecast Time Series
from statsmodels.tsa.stattools import acf, pacf
logvol_dif1 = vpy_df["logvol_dif1"][np.logical_not(np.isnan(vpy_df["logvol_dif1"]))]

lv_acf = acf(logvol_dif1)
lv_pacf = pacf(logvol_dif1)

fig, ax = plt.subplots()
plt.plot(lv_acf)
plt.axhline(y=0, linestyle='--', color='gray')
plt.axhline(y=-1.96/np.sqrt(len(logvol_dif1)), linestyle='--', color='gray')
plt.axhline(y=1.96/np.sqrt(len(logvol_dif1)), linestyle='--', color='gray')
plt.title('Autocorrelation Function')

from statsmodels.tsa.arima_model import ARIMA
model = ARIMA(vpy_df["logvolume"], (2, 1, 2))
results_ARIMA = model.fit(disp=-1)
predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)

# TODO(jcm) Ask why exponential scaling doesn't work in this case...
scaled_predictions = np.exp(predictions_ARIMA_diff.cumsum())

fig, ax = plt.subplots()
plt.plot(lv_acf)
plt.title('Autocorrelation Function')
