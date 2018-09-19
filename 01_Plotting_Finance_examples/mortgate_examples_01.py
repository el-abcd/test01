
# pip install git+https://github.com/jbmohler/mortgage.git
import mortgage
m=mortgage.Mortgage(interest=0.0375, amount=350000, months=360)
mortgage.print_summary(m)


from itertools import islice
print list(month[0] for month in islice(m.monthly_payment_schedule(), 12))


# import pandas as pd
# import numpy as np

