
# Try resampling data.
# https://chrisalbon.com/python/data_wrangling/pandas_group_data_by_time/

import pandas as pd
import datetime
import numpy as np

# Create data
base = datetime.datetime.today()
# List of days
date_list = [base - datetime.timedelta(days=x) for x in range(0,365)]
score_list = list(np.random.randint(low=1, high=1000, size=365))

#Create a dataframe
df = pd.DataFrame()

df['datetime'] = date_list
#Convert to a pandas datetime.
df['datetime'] = pd.to_datetime(df['datetime'])
df.index = df['datetime']

df['score'] = score_list

df.head()

#Resample is a two stage process.
print(df.resample('M').mean())
print(df.resample('MS').mean())