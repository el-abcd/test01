"""
Overall master file that imports classes for various investments, and runs the overall plots, etc.
"""

import sys
#from pathlib import Path
#print(Path().absolute())
#sys.path.append(Path().absolute()) # set path to do imports below...
import inv_PPR_1909_xxxx_350k as ppr_350
import inv_03l_SchneidersSaddleryNNN_1905_xxxx_150k as schn_150
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


a = schn_150.Inv_03l_SchneidersSaddleryNNN()
print(a.df)
print(a.quarterly_to_month_end())
b = ppr_350.Inv_02ac_PPR_Reliant()
print(b.df)
print(b.quarterly_to_month_end())


