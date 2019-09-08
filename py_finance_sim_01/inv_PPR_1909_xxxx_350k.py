from inv_baseClass import Transact, calc_pref
import datetime
from dateutil.relativedelta import relativedelta # pip install python-dateutil

class Inv_PPR_todo_cleanup(object):
    """Simpy process to simulate investment.

    ToDo: Perhaps extract into text format, in a text input file?

    Args:
        TBD

    Yields:
        simpy event that defines when this should be triggered and executed again.

    Returns:
        TBD
    """

    def __init__(self):
        """Info for 02ac_PPR_Reliant-10%-3yr_1908-2208


        References:
            Google Drive folder:
                https://drive.google.com/drive/folders/1nia_IyhUybJYDjyzQrIvj4ZbhkpDyzwU?usp=sharing

        Returns:
            NA
        """

        # WT SEQ160752 RELIANT INCOME FUND LLC /BNF=RELIANT INCOME FUND LLC SRF# 0000257242264277 TRN#190830160752 RFB#
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


        import matplotlib.pyplot as plt
        # https://stackoverflow.com/questions/48439005/pycharm-jupyter-interactive-matplotlib/48695728

        x = [ i.date for i in self.pref_table ]
        y = [float(i.amount) for i in self.pref_table]
        plt.plot(x ,y, '.-r')
        plt.ylim([0, 4000])
        plt.show()


a = Inv_PPR_todo_cleanup()