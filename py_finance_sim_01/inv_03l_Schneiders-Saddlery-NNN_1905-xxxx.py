from inv_baseClass import Transact, calc_pref
import datetime

class Inv_03l_SchneidersSaddleryNNN(object):
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
        # , start_date=datetime.date.today(),
        #              loan_amount=100000, length_years=15, interest_rate=0.04,
        #              private_mortgage_insur=0.0, ):
        """Info for Schneider Saddlery NNN investment

        Setup variables and info for investment.  Ideally put most of the setup
        info here, and make the "periodic update" code simpler.

        References:
            Confidential Investment Summary - Schneiders Saddlery.pdf
                https://drive.google.com/file/d/1RPueall8x_dQ9mFmjTJOgKy6cgu1c6xv/view?usp=sharing
            190621__Saddle - Class A Investor Memo_6.20.19.pdf
                https://drive.google.com/file/d/1UQW9OAMOkNDSojlMmbg1NsZkgMaTi94T/view?usp=sharing
        Returns:
            NA
        """

        self.start_date = datetime.date(2019, 5, 23)
        self.inv_initial = 150000
        self.capital_account = self.inv_initial  # Start at initial investment amount.
        self.duration_expected = datetime.timedelta(
            5 * 365)  # "Target Hold Period: 5 to 7 years from closing"

        # Distributions:
        # Preferred dividend on invested capital distributed quarterly
        # (8.0% in Year 1,
        # 8.5% Year 2,
        # 9.0% Year 3,
        # 9.5% Year 4, and
        # 10% Year 5 and thereafter)

        # 190621__Saddle - Class A Investor Memo_6.20.19.pdf
        # Distributions are made quarterly within 30 days of the end of the
        # previous closed quarter. The first distributions for the partnership
        # will be made for the investment period of June 3-June 30 2019 and will
        # be sent out on or before July 30th. We general target the 15th of
        # each month.

        """ Details of return calculations:
        i.e. how to read thru the pdf and understand the numbers...

        Loan of $4,140,000, 5%, 23 yr amortization = annual payment of 303,250.
        First year rent of 473,833.
        Mag Capital has 3% Mgmt fee on rent: 473,800 * 0.03 = 14,215
        473833 - 303250 - 14215 = 156,368
        Investor pref of 8% (on 1,800,000) is 144,000 (first year).
        MAG capital keeps the REST of the annual rent payments!  This is not 
        included in later calculations.  

        Upon selling, we get 80/20 split of proceeds upto a "18% ROI".  
        This is NOT IRR (compounded).  Instead, for each dollar at the time of 
        sale (after paying closing costs, bank loan, investor capital), we get 
        80%, until we have (overall) received 18% annual return 
        (1,800,000*0.18 = 324,000 annually).  MAG gets 20%.  
        Above that amt, we do 50/50 split.  
        Since we get paid at the end, our returns drift below an 18% IRR in 
        general.  
        """

        pref_table_raw = [
            # Year 1, 8% pref
            # 7/30/2019	Saddle Investmen Ach Pmt x x6780 Q2 2019 Distribution		$923.08	PREFERRED CHECKING	xxxx1428	Wells Fargo
            # This appears to be a 364 day year?  923.08 / (150000*0.08 / 364) = 28.0000933333 days.  If I use 365 it is 28.077.
            # Not sure why 364 days (can't divide by 12).  But, that appears to
            # be one of the accepted "conventions":  https://en.wikipedia.org/wiki/Day_count_convention

            # Try to calculate the "exact" amounts (dates don't quite line up on quarters, etc.)
            # This tests the ability to easily do "exact" calculations later on.

            # list of {trans_date, pref_amount, },
            # ToDo: Make this a class?  i.e. defined fields for transactions?
            Transact('2019-07-30',
                     calc_pref(0.080, self.capital_account, False, '2019-06-03',
                               '2019-07-01', 364)),
            # June 3-June 30.  First year is later (on 7-30)
            Transact('2019-10-15', calc_pref(0.080, self.capital_account, 'q')),
            # 07-01 thru 10-01
            Transact('2020-01-15', calc_pref(0.080, self.capital_account, 'q')),
            # 10-01 thru 01-01
            Transact('2020-04-15', calc_pref(0.080, self.capital_account, 'q')),
            # 01-01 thru 04-01
            Transact('2020-07-15',
                     calc_pref(0.080, self.capital_account, False, '2020-04-01',
                               '2020-06-03', 364)),  # 04-01 thru 06-03

            # 2nd year.
            Transact('2020-07-15',
                     calc_pref(0.085, self.capital_account, False, '2020-06-03',
                               '2020-07-01', 364)),  # New pref rate.
            Transact('2020-10-15', calc_pref(0.085, self.capital_account, 'q')),
            # 07-01 thru 10-01
            Transact('2021-01-15', calc_pref(0.085, self.capital_account, 'q')),
            # 10-01 thru 01-01
            Transact('2021-04-15', calc_pref(0.085, self.capital_account, 'q')),
            # 01-01 thru 04-01
            Transact('2021-07-15',
                     calc_pref(0.085, self.capital_account, False, '2021-04-01',
                               '2021-06-03', 364)),  # 04-01 thru 06-03

            # 3rd year
            Transact('2021-07-15',
                     calc_pref(0.090, self.capital_account, False, '2021-06-03',
                               '2021-07-01', 364)),  # New pref rate.
            Transact('2021-10-15', calc_pref(0.090, self.capital_account, 'q')),
            # 07-01 thru 10-01
            Transact('2022-01-15', calc_pref(0.090, self.capital_account, 'q')),
            # 10-01 thru 01-01
            Transact('2022-04-15', calc_pref(0.090, self.capital_account, 'q')),
            # 01-01 thru 04-01
            Transact('2022-07-15',
                     calc_pref(0.090, self.capital_account, False, '2022-04-01',
                               '2022-06-03', 364)),  # 04-01 thru 06-03

            # 4th year
            Transact('2022-07-15',
                     calc_pref(0.095, self.capital_account, False, '2022-06-03',
                               '2022-07-01', 364)),  # New pref rate.
            Transact('2022-10-15', calc_pref(0.095, self.capital_account, 'q')),
            # 07-01 thru 10-01
            Transact('2023-01-15', calc_pref(0.095, self.capital_account, 'q')),
            # 10-01 thru 01-01
            Transact('2023-04-15', calc_pref(0.095, self.capital_account, 'q')),
            # 01-01 thru 04-01
            Transact('2023-07-15',
                     calc_pref(0.095, self.capital_account, False, '2023-04-01',
                               '2023-06-03', 364)),  # 04-01 thru 06-03

            # 5th year and later, always 10% pref.
            Transact('2023-07-15',
                     calc_pref(0.100, self.capital_account, False, '2022-06-03',
                               '2022-07-01', 364)),  # New pref rate.
            Transact('2023-10-15', calc_pref(0.100, self.capital_account, 'q')),
            # 07-01 thru 10-01
            Transact('2024-01-15', calc_pref(0.100, self.capital_account, 'q')),
            # 10-01 thru 01-01
            Transact('2024-04-15', calc_pref(0.100, self.capital_account, 'q')),
            # 01-01 thru 04-01
            Transact('2024-07-15', calc_pref(0.100, self.capital_account, 'q')),
            # 04-01 thru 07-01

            # 6th year
            Transact('2024-10-15', calc_pref(0.100, self.capital_account, 'q')),
            # 07-01 thru 10-01
            Transact('2025-01-15', calc_pref(0.100, self.capital_account, 'q')),
            # 10-01 thru 01-01
            Transact('2025-04-15', calc_pref(0.100, self.capital_account, 'q')),
            # 01-01 thru 04-01
            Transact('2025-07-15', calc_pref(0.100, self.capital_account, 'q')),
            # 04-01 thru 07-01

            # 7th year
            Transact('2025-10-15', calc_pref(0.100, self.capital_account, 'q')),
            # 07-01 thru 10-01
            Transact('2026-01-15', calc_pref(0.100, self.capital_account, 'q')),
            # 10-01 thru 01-01
            Transact('2026-04-15', calc_pref(0.100, self.capital_account, 'q')),
            # 01-01 thru 04-01
            Transact('2026-07-15', calc_pref(0.100, self.capital_account, 'q')),
            # 04-01 thru 07-01
        ]

        # print(pref_table_raw)
        # Merge payments that happen on the SAME day, to clean up the data a bit.
        prev_date = 0
        prev_index = -1
        self.pref_table = []
        for row in pref_table_raw:
            if row.date == prev_date:
                self.pref_table[prev_index].amount += row.amount
            else:
                self.pref_table.append(row)
                prev_date = row.date
                prev_index += 1

        # print(self.pref_table)

        # TEMPORARY plotting.

        import matplotlib.pyplot as plt
        # https://stackoverflow.com/questions/48439005/pycharm-jupyter-interactive-matplotlib/48695728
        # import matplotlib
        # matplotlib.use('Qt5Agg')
        # import Matplotlib.pyplot as plt

        x = [i.date for i in self.pref_table]
        y = [float(i.amount) for i in self.pref_table]
        plt.plot(x, y, '.-r')
        plt.ylim([0, 4000])
        plt.show()

        print('Start plotting...')
        df = pd.DataFrame()
        df['dates'] = pd.to_datetime(x)
        df.index = df['dates']

        # ToDo: https://beepscore.com/website/2018/10/12/using-pandas-with-python-decimal.html#targetText=in%20Pandas,be%20another%20type%20like%20Decimal.
        df['03l_Schn'] = y
        y2 = df.resample('Q').sum()
        plt.plot(y2)
        plt.show()

        y3 = y2.cumsum()
        plt.plot(y3)
        plt.show()

        # OK, have resampled by quarter!
        # How to resample by month and show in a reasonable way?
        # How to do cumulative plots?

        # OLD BELOW HERE!!!

        # Setup simpy
        self.env = env
        self.period_days = 30

        # Create a "process" that knows how to calculate the next monthly payment.
        # self.mortgage_process = env.process(self.monthly_payment())

        # Create dataframe to store the history of this particular account.
        # NOTE: should have some "standard" columns (date, comment, amt) so can easily combine with OTHER
        # accounts.
        # Note: put in a date column, just use an integer index to start...
        # columns = ["date","princ_pay","int_pay","extra_fee_pay","balance"]
        # init_data = [pd.Timestamp(start_date), dollar(0), dollar(0), dollar(0), dollar(loan_amount)]
        # TODO: maybe initialize from something besides a dict, to control the column order better?
        # self.mort_account = pd.DataFrame({
        #     "date": [pd.Timestamp(start_date)], # Make a list, so at least one element is non-scalar! Pandas error otherwise.
        #     "princ_pay": dollar(0),
        #     "int_pay": dollar(0),
        #     "extra_fee_pay": dollar(0),
        #     "balance": dollar(loan_amount)
        # })

if __name__ == '__main__':
    a = Inv_03l_SchneidersSaddleryNNN()
