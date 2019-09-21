from inv_baseClass import Transact, calc_pref, inv_base
import datetime
from dateutil.relativedelta import relativedelta # pip install python-dateutil
import matplotlib.pyplot as plt
import pandas as pd

class Inv_inv_03q_OpenDoor_Brandon_1908_xxxx_200k(inv_base):
    """Simulate an investment.

    Args:
        TBD

    Returns:
        TBD
    """

    @property
    def description(self):
        #ToDo: remove leading spaces on additional lines.  Add more content?
        a = '''Info for 03q_BrandonTurner_OpenDoorMobileHomeFund_1908-xxxx_tmpltV06
        References:
            Google Drive folder:
                https://drive.google.com/drive/folders/1ygKviY50MFk2G0cq0sryJXcANfOSBnCm?usp=sharing
        '''
        return a

    def __init__(self):
        #composition
        self.base = inv_base(
            short_name='Brand_200'
            , description=self.description
        )

        # 190920_ConfirmationLetter_Open Door Capital Fund - Welcome Letter - Eric Lee.pdf
        self.start_date = datetime.date(2019, 9, 20)
        self.inv_initial = 200000
        self.capital_account = self.inv_initial  # Start at initial investment amount.

        # From: 190902_ODC+Investment+Executive+Summary+V2.0.pdf, p05
        # 17%+ IRR projections on 5-10 year hold.
        # The goal: purchase the 500 total occupied units that we currently have
        # under contract, grow cash flow, hold for 5-10 years and sell at a
        # significantly higher valuation.

        # (Quarterly disbursements, and hold until ideal time in the market to maximize returns.)

        self.duration_expected = datetime.timedelta \
            ( 10 *365)  # estimate 10 years

        # From: 190902_ODC+Investment+Executive+Summary+V2.0.pdf, p26
        # yearly: 7.1, 10.0, 12.6, 13.4, 15.5, 17.5, 19.3, 21.1. 22.9

        # From the PPM:
        # 190902_#PPM+Open+Door+Capital+Fund w highlights copy.pdf
        #
        # Distributable Cash, if any, derived from operation of the Properties will be evaluated on a quarterly basis starting one (1) year after operations commence, and disbursed as provided below until expended.
        # First, the Class A Members will receive an annualized, non-cumulative, non- compounding Preferred Return of eight percent (8%) on their unreturned Capital Contributions.
        # Second, the Class A Members will receive, together with their Preferred Return, seventy percent (70%) of the Distributable Cash, pro rata, in accordance with their Percentage Interests and the Class B Members shall receive thirty percent (30%) of the Distributable Cash, pro rata in accordance with their Percentage Interests until the Class A Members have reached a fifteen percent (15%) IRR.
        # Thereafter, the Class A Members will receive fifty percent (50%) of the Distributable Cash, pro rata, in accordance with their Percentage Interests and the Class B Members shall receive fifty percent (50%) of the Distributable Cash, pro rata, in accordance with their Percentage Interests.
        # For the purposes of Cash Distribution calculations only, Cash Distributions to Class A and Class B Members from operations will be treated as a return on investment.

        # So, assume nothing until the end of the first year.  Then 7.1% (catchup?)  Then keep earning at that rate, until a refi, then pref will drop...(mgr percent goes up)
        # Assume about 1.5 month after end of quarter?

        self.pref_table = []

        # Wait 1 year for initial payment... 3rd qtr 2020?  Pay about 11-15? (qtr end is 9/30)
        self.pref_table.append(
            Transact('2020-11-15', 0.071 * self.capital_account),  # Full year
        )

        for (year_offset, annual_pref) in enumerate([10.0, 12.6, 13.4, 15.5, 17.5, 19.3, 21.1, 22.9]):
            # paid quarterly.
            for qtr_offset in range (4): # Remaining quarters
                self.pref_table.append(
                    Transact(datetime.date(2021, 2, 15) + relativedelta(years=year_offset) + relativedelta(months=qtr_offset*3),
                             annual_pref/100.0 * self.capital_account) )


        # Final cashout.
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

        print('DONE!!!!!')

if __name__ == '__main__':

    print('START')
    a = Inv_inv_03q_OpenDoor_Brandon_1908_xxxx_200k()

    # https://stackoverflow.com/questions/48439005/pycharm-jupyter-interactive-matplotlib/48695728
    x = [i.date for i in a.pref_table]
    y = [float(i.amount) for i in a.pref_table]
    plt.plot(x, y, '.-r')
    plt.ylim([0, 4000])
    plt.show()

    print(a.description)

