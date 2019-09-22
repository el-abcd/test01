from inv_baseClass import Transact, calc_pref, inv_base
import datetime
from dateutil.relativedelta import relativedelta # pip install python-dateutil
import matplotlib.pyplot as plt
import pandas as pd

class Inv_02ac_PPR_Reliant(inv_base):
    """Simpy process to simulate investment.

    ToDo: Perhaps extract into text format, in a text input file?

    Args:
        TBD

    Yields:
        simpy event that defines when this should be triggered and executed again.

    Returns:
        TBD
    """

    @property
    def description(self):
        #ToDo: remove leading spaces on additional lines.  Add more content?
        a = '''Info for 02ac_PPR_Reliant-10%-3yr_1908-2208
        References:
            Google Drive folder:
                https://drive.google.com/drive/folders/1nia_IyhUybJYDjyzQrIvj4ZbhkpDyzwU?usp=sharing
        '''
        return a

    def __init__(self):
        #composition
        self.base = inv_base(
            short_name='PPR_350'
            , description='02ac_PPR_Reliant-10%-3yr_1908-2208_tmpltV06_350k'
        )
        self.base.is_quarterly = None

        # Bank transaction record:  WT SEQ160752 RELIANT INCOME FUND LLC /BNF=RELIANT INCOME FUND LLC SRF# 0000257242264277 TRN#190830160752 RFB#
        self.start_date = datetime.date(2019, 8, 30)
        self.inv_initial = 350000
        self.capital_account = self.inv_initial  # Start at initial investment amount.
        self.duration_expected = datetime.timedelta \
            ( 3 *365)  # 3 years, 10% returns

        # Distributions:
        # Monthly, 10% rate.

        # Email with confirmation / 1st month.
        # Sent: Tuesday, September 3, 2019, 11:27:45 AM PDT
        # Subject: Funding Confirmation - non-compounding
        # We received your funds 8/30/2019, and due to our processing period,
        # your investment start date will begin 9/6/2019.
        # Expect your 1st preferred return on October 1st, pro-rated back to
        # September 6th.  Also on the 6th, your investment information will be
        # uploaded and accepted, which will enable you to view this information
        # in your account in the investor portal.

        self.pref_table = []

        # Initial partial month.
        self.pref_table.append(
            Transact('2019-10-01', calc_pref(0.100, self.capital_account, False, '2019-09-06', '2019-10-01', 365)),  # Partial month
        )

        # Full months.
        start_month = 10
        for n in range (1, 36): # Remaining months
            self.pref_table.append(
                Transact(datetime.date(2019, start_month, 1) + relativedelta(months=n),
                         calc_pref(0.100, self.capital_account, 'm'))
            )

        # Final month.
        self.pref_table.append(
            Transact('2022-10-01', calc_pref(0.100, self.capital_account, False, '2022-09-01', '2022-09-06', 365)),  # Partial month
        )
        #print(self.pref_table)


        # Create a dataframe...
        x = [i.date for i in self.pref_table]
        # ToDo: https://beepscore.com/website/2018/10/12/using-pandas-with-python-decimal.html#targetText=in%20Pandas,be%20another%20type%20like%20Decimal.

        y = [float(i.amount) for i in self.pref_table]

        self.df = pd.DataFrame()
        self.df['dates'] = pd.to_datetime(x)
        self.df['amt'] = y
        # Add a column with the same value per row...
        self.df['inv_name'] = self.base.short_name

        self.df = self.df.set_index('dates')

if __name__ == '__main__':

    a = Inv_02ac_PPR_Reliant()

    # https://stackoverflow.com/questions/48439005/pycharm-jupyter-interactive-matplotlib/48695728
    x = [i.date for i in a.pref_table]
    y = [float(i.amount) for i in a.pref_table]
    plt.plot(x, y, '.-r')
    plt.ylim([0, 4000])
    plt.show()

    print(a.description)

