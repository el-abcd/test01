from inv_baseClass import Transact, calc_pref, inv_base
import datetime
from dateutil.relativedelta import relativedelta # pip install python-dateutil
import matplotlib.pyplot as plt
import pandas as pd

class Inv_03p_UrbanCatalystQOZ_1908_250k(inv_base):
    """Simulate an investment.

    Args:
        TBD

    Returns:
        TBD
    """
    #ToDo: Make notes about paying deferred capital gains in 2026!!!!  Need to save cash for that!
    # estimate:  250K * 0.238 = 59.5K FED tax.

    @property
    def description(self):
        #ToDo: remove leading spaces on additional lines.  Add more content?
        a = '''Info for 03p_UrbanCatalystQOZ_Yoram_1908-xxxx_tmpltV06
        References:
            Google Drive folder:
                https://drive.google.com/drive/u/0/folders/11C9Lvdg9XRczJugoHyYaFkybZfC6m_Jl
        '''
        return a

    def __init__(self):
        #composition
        self.base = inv_base(
            short_name='UrbCatal_250'
            , description=self.description
        )
        self.base.is_quarterly = TBD?

        # 190920_ConfirmationLetter_Open Door Capital Fund - Welcome Letter - Eric Lee.pdf
        self.start_date = datetime.date(2019, 8, 29)
        self.inv_initial = 79000
        self.capital_account = self.inv_initial  # Start at initial investment amount.

        # Note: deposited initial 70k.  Then 9k (5%) deposit on additional 180k!


        self.duration_expected = datetime.timedelta \
            ( 10 *365)  # estimate 10 years



if __name__ == '__main__':

    print('START')
    a = Inv_03p_UrbanCatalystQOZ_1908_250k()

    # https://stackoverflow.com/questions/48439005/pycharm-jupyter-interactive-matplotlib/48695728
    x = [i.date for i in a.pref_table]
    y = [float(i.amount) for i in a.pref_table]
    plt.plot(x, y, '.-r')
    plt.ylim([0, 20000])
    plt.show()

    print(a.description)

