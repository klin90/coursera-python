import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv', \
                usecols = ['Date', 'Element', 'Data_Value'])
df['Date'] = pd.to_datetime(df['Date'])
df = df[~((df['Date'].dt.month == 2) & (df['Date'].dt.day == 29))]

df = df.assign(Year = df['Date'].dt.year)

# switch to a non-leap year, then take dates only
df['Date'] = df['Date'].apply(lambda x: x.replace(year = 2005))
df = df.assign(Day = df['Date'].dt.dayofyear)
df = df.drop('Date', axis = 1)

# numpy arrays for max/min temperatures 2009-2014, and 2015 temperatures
tmax = (df[(df['Year'] >= 2005) & (df['Year'] <= 2014) & \
           (df['Element'] == 'TMAX')].groupby(['Day'])['Data_Value'].max() / 10).values
tmin = (df[(df['Year'] >= 2005) & (df['Year'] <= 2014) & \
           (df['Element'] == 'TMIN')].groupby(['Day'])['Data_Value'].min() / 10).values
t15x = (df[(df['Year'] == 2015) & (df['Element'] == 'TMAX')].groupby(['Day'])['Data_Value'].max() / 10).values
t15n = (df[(df['Year'] == 2015) & (df['Element'] == 'TMIN')].groupby(['Day'])['Data_Value'].min() / 10).values

# null all 2015 data that doesn't set a new record
t15x[~np.greater(t15x, tmax)] = np.nan
t15n[~np.less(t15n, tmin)] = np.nan

# plot temperature data
dates = np.arange(1, 366)
fig, ax = plt.subplots(figsize = (12, 8), facecolor = 'white')
fig.set_alpha(1)
ax.plot(dates, tmax, color = 'black', alpha = 0.5)
ax.plot(dates, tmin, color = 'black', alpha = 0.5)
ax.scatter(dates, t15x, color = 'red', label = 'New Record High in 2015')
ax.scatter(dates, t15n, color = 'blue', label = 'New Record Low in 2005')
ax.fill_between(dates, tmin, tmax, facecolor = 'black', alpha = 0.25, label = 'Temperature Range for 2005-2014')

# set up the x axis - minor ticks for months
xticks = np.array([1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 365])
xticksm = 0.5 * (xticks[1:] + xticks[:-1])
months = pd.date_range(start = '2005-1-1', end = '2006-12-31', freq = 'M')
xticklabels = months.strftime('%b')
ax.set_xlim(1, 365)
ax.set_xticks(xticks)
ax.set_xticks(xticksm, minor = True)
ax.set_xticklabels(xticklabels, minor = True)
ax.tick_params(which = 'major', labelbottom = False)
ax.tick_params(which = 'minor', bottom = False)

# set up the y axes - left celsius, right fahrenheit
degC = u'\N{DEGREE SIGN}C'
degF = u'\N{DEGREE SIGN}F'
yticks = [-40, -20, 0, 20, 40]
yticklabels = ['-40' + degC, '-20' + degC, '0' + degC, '20' + degC, '40' + degC]
yticks2 = [-40, -4, 32, 68, 104]
yticklabels2 = ['-40' + degF, '-4' + degF, '32' + degF, '68' + degF, '104' + degF]
ax.set_ylim(-40, 45)
ax2 = ax.twinx()
ax2.set_ylim(-40, 113)
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)
ax2.set_yticks(yticks2)
ax2.set_yticklabels(yticklabels2)

# hide top bar, show legend and title
ax.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.legend(loc = 4)
ax.set_title('2005-2015 Weather Patterns in Ann Arbor, MI')

plt.show()