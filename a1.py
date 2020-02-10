# Advanced Python for Streaming Analytics
# Workshop 1

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import pylab

# Simple Linear Regression
import statsmodels.formula.api as sm
from pandas_datareader import data

all_data = {}
for ticker in ['AAL', 'ALK', 'WTI']:
    all_data[ticker] = data.DataReader(ticker, 'yahoo', '2014-06-01', '2016-06-13')

all_data['WTI'].head()
all_data['AAL'].head()
all_data['ALK'].head()

price = pd.DataFrame({tic: data['Adj Close'] for tic, data in all_data.items()})

price.head(5)

price_pct_change = price.pct_change()

fig, ax = plt.subplots()
wti_color = np.repeat('black', 513)
aal_color = np.repeat('blue', 513)

ax.scatter(range(1, len(price_pct_change.index)),
        price_pct_change['AAL'][1:], c=aal_color, label='AAL',
        alpha=.5)
ax.scatter(range(1, len(price_pct_change.index)), price_pct_change['WTI'][1:],
        c=wti_color, label='WTI', alpha=.5)

ax.set_xlabel(r'Days', fontsize=15)
ax.set_ylabel(r'% Change', fontsize=15)
ax.legend()

plt.show()

result = sm.ols(formula="WTI ~ AAL", data=price_pct_change).fit()
print(result.params)
result = sm.ols(formula="WTI ~ ALK", data=price_pct_change).fit()
print(result.params)
