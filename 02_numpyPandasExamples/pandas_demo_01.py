
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

a = pd.Series([1,2,3,np.nan,9,8,7,np.inf])

print a
print "Hi"

dates = pd.date_range('20181001', periods=6)
dates

df = pd.DataFrame(data=np.random.randn(6,4), index=dates, columns=list('ABCD'))
df
print dates
print df


df2 = pd.DataFrame({"A": 1.,
                    "B": pd.Timestamp("20181001"),
                    "C": pd.Series(1, index=list(range(4)), dtype='float32'),
                    "D": np.array([3] * 4, dtype='int32'),
                    "E": pd.Categorical(["test","train","test","train"]),
                    "F": 'foo'
                    })

# df2 = pd.DataFrame({ 'A' : 1.,
#    ....:                      'B' : pd.Timestamp('20130102'),
#    ....:                      'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
#    ....:                      'D' : np.array([3] * 4,dtype='int32'),
#    ....:                      'E' : pd.Categorical(["test","train","test","train"]),
#    ....:                      'F' : 'foo' })

print df2
print df2.dtypes

df3 = pd.DataFrame({"A": 1.,
                    "B": [2] # MUST have at least one be an array/list (for some reason)!
                    })
print df3


# Plotting:
print "try plotting"
ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
ts.plot()


print "bye"
