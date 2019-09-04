import datetime
#from dateutil.relativedelta import relativedelta  # To increment dates by a month, etc.
import decimal

import numpy as np
import pandas as pd
import simpy

# Try to simulate a mortgage!!!

DOLLAR_QUANTIZE = decimal.Decimal('.01')


def dollar(f, round=decimal.ROUND_CEILING):
    """
    This function rounds the passed float to 2 decimal places.
    """
    if not isinstance(f, decimal.Decimal):
        f = decimal.Decimal(str(f))
    return f.quantize(DOLLAR_QUANTIZE, rounding=round)

def timestamp(date):
    """ Convert a datetime.date to a UTC timestamp.  This is tz 'naive', everything is in GMT time"""
    return (date - datetime.date(1970, 1, 1)).total_seconds()

# https://docs.scipy.org/doc/numpy-1.13.0/reference/routines.financial.html
"""
fv(rate, nper, pmt, pv[, when])	Compute the future value.
pv(rate, nper, pmt[, fv, when])	Compute the present value.
npv(rate, values)	Returns the NPV (Net Present Value) of a cash flow series.
pmt(rate, nper, pv[, fv, when])	Compute the payment against loan principal plus interest.
ppmt(rate, per, nper, pv[, fv, when])	Compute the payment against loan principal.
ipmt(rate, per, nper, pv[, fv, when])	Compute the interest portion of a payment.
irr(values)	Return the Internal Rate of Return (IRR).
mirr(values, finance_rate, reinvest_rate)	Modified internal rate of return.
nper(rate, pmt, pv[, fv, when])	Compute the number of periodic payments.
rate(nper, pmt, pv, fv[, when, guess, tol, ...])	Compute the rate of interest per period.
"""


# OK, there IS AND IRR in numpy, no need to recreate it manually!!!!
# /Users/elee/01_git/test01/virtualenv/lib/python2.7/site-packages/numpy/lib/tests/test_financial.py


class mortgage_simple(object):
    """simpy process to simulate a mortgage

    Notes:
        Private mortgage insurance (PMI): https://www.bankrate.com/finance/mortgages/the-basics-of-private-mortgage-insurance-pmi.aspx
            If paying less than 20% down payment, it maybe required.
            PMI fees vary from around 0.3 percent to about 1.5 percent of the original loan amount per year.
            TBD: Possibly add logic to deal with reducing/removing when equity is >20%, etc.

    Args:
        interest_rate (float): The annual interest rate.  0.04 = 4.0%
        length_years (int): The length of the mortgate.  Is converted to months internally.
        private_mortgage_insur (float):

    Yields:
        simpy event that defines when this should be triggered and executed again.

    Returns:
        TBD
    """

    def __init__(self, env, start_date=datetime.date.today(),
                 loan_amount=100000, length_years=15, interest_rate=0.04,
                 private_mortgage_insur=0.0, ):
        self._interest_monthly = float(interest_rate)/12
        self._length_months = int(length_years * 12)
        self._initial_loan_amount = dollar(loan_amount) # ToDo: remove _???
        self.start_date = start_date
        self.principal = loan_amount # dollar(loan_amount)
        self.payment_number = 0
        print("{} {} {}".format(self._interest_monthly, self._length_months, float(dollar(loan_amount))))
        self.monthly_payment_amt = np.pmt(self._interest_monthly, length_years * 12,
                                          float(dollar(loan_amount)))
        self.amort_table_interest = np.ipmt(self._interest_monthly,
                                            range(1, self._length_months+1),
                                            length_years * 12,
                                            float(dollar(loan_amount)))
        self.amort_table_principal = np.ppmt(self._interest_monthly,
                                            range(1, self._length_months+1),
                                             self._length_months,
                                            float(dollar(loan_amount)))
        print("Monthly payment is: {}".format(self.monthly_payment_amt))
        print("Interest and Principal: {} {}".format(self.amort_table_interest, self.amort_table_principal))

        #Setup simpy
        self.env = env
        self.period_days = 30

        # Create a "process" that knows how to calculate the next monthly payment.
        self.mortgage_process = env.process(self.monthly_payment())

        # Create dataframe to store the history of this particular account.
        # NOTE: should have some "standard" columns (date, comment, amt) so can easily combine with OTHER
        # accounts.
        # Note: put in a date column, just use an integer index to start...
        # columns = ["date","princ_pay","int_pay","extra_fee_pay","balance"]
        # init_data = [pd.Timestamp(start_date), dollar(0), dollar(0), dollar(0), dollar(loan_amount)]
        # TODO: maybe initialize from something besides a dict, to control the column order better?
        self.mort_account = pd.DataFrame({
            "date": [pd.Timestamp(start_date)], # Make a list, so at least one element is non-scalar! Pandas error otherwise.
            "princ_pay": dollar(0),
            "int_pay": dollar(0),
            "extra_fee_pay": dollar(0),
            "balance": dollar(loan_amount)
        })

        print(self.mort_account)
        #raise("testing")

    #ToDo: HOW to handle float * Decimal calculations?
        # Convert back to decimal ONLY when displaying results (trim to 2 digits).
        # OR, is it better to do the calculations in Decimal, and convert floats to Decimal BEFORE doing calcs?
        # I guess readup on decimal some more later (just get it prototyped for now).

    def monthly_payment(self):
        while True:
            #Ok, I need to add the loop here, is NOT done externally by environment!
            # i.e. the timeout is a "sleep until", it still depends on the PROCESS to decide when to stop looping!!!

            # Add a timeout for the next monthly payment!!!
            # WAIT for the end of the month, THEN do the calculations!!!
            next_month_timestamp = timestamp(datetime.date.fromtimestamp(self.env.now) + relativedelta(months=+1) )
            print("Now is: {}, {}".format(self.env.now, datetime.date.fromtimestamp(self.env.now)))
            self.payment_number += 1
            print("Iteration is: {}".format(self.payment_number))
            #print("Next timestamp: {}".format(next_month_timestamp))
            # Calculate the DELTA here, first get a valid date, move forward one month, then see what the delta was.
            # The timeout usually wants the DELTA.
            new_ts = timestamp(datetime.date.fromtimestamp(self.env.now) + relativedelta(months=+1))
            delta = new_ts - timestamp(datetime.date.fromtimestamp(self.env.now))
            yield self.env.timeout( delta )


            # WAKE UP AND DO CALCULATIONS FOR THIS DATE/PAYMENT!
            # pre_amt = float(self.amount()) * self.rate() / (float(MONTHS_IN_YEAR) * (1.-(1./self.month_growth()) ** self.loan_months()))
            # return dollar(pre_amt, round=decimal.ROUND_CEILING)
            print("Woke up at: {}, {}".format(self.env.now, datetime.date.fromtimestamp(self.env.now)))
            # ToDo: If made an extra payment partially thru the month maybe calculate interest daily?
            # Calculate values from last month payment, instead of using amortizaion
            # table, to account for any "extra payments".
            interest_pay = -1 * float(self.principal) * self._interest_monthly
            principal_pay = (self.monthly_payment_amt - interest_pay)
            print("Payment: {}, Principal payment: {}".format(self.monthly_payment_amt, principal_pay))
            self.principal += dollar(principal_pay)
            if self.principal <= 0.01:
                print("Negative principal, loan is paid off! Final principal is: {}".format(self.principal))
                print(self.mort_account)

                self.env.exit(0) # End the process by returning!
            #self.payment_number += 1
            print("Interest: {}".format(interest_pay))
            print("Remaining Principal: {}".format(self.principal))
            print("____")

            #ADD A NEW ROW TO THE DATAFRAME!
            #Todo: add a class for a row in the mortgage? Or just make a dict as needed?
            # Class might be NICE, if put all the dollar conversion in there!!!
            new_row= {
                "date": datetime.date.fromtimestamp(self.env.now),
                "princ_pay": dollar(principal_pay),
                "int_pay": dollar(interest_pay),
                "extra_fee_pay": dollar(0),
                "balance": self.principal
                }
            #TODO: This creates a new object, then REPLACES the old one.
            # Maybe pandas.concat() is more efficient (does an "in-place" update?
            # Or, maybe should generate a list, and only occasionally update the dataframe?
            # i.e. I guess due to fixed size it is not optimized for growing, need to realloc memory often?  Or
            # does it allocate some extra space for growth??
            self.mort_account = self.mort_account.append(new_row, ignore_index=True)

            print("Mortgage update DONE")
            #print(self.mort_account)


####################
# 190901, Start Schneider simulation...
class Inv_03l_SchneidersSaddlery(object):
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
        #, start_date=datetime.date.today(),
    #              loan_amount=100000, length_years=15, interest_rate=0.04,
    #              private_mortgage_insur=0.0, ):
        """Info for Schneider Saddlery NNN investment

        Setup variables and info for investment.  Ideally put most of the setup
        info here, and make the "periodic update" code simpler.

        References:
            Confidential Investment Summary - Schneiders Saddlery.pdf
                https://drive.google.com/file/d/1RPueall8x_dQ9mFmjTJOgKy6cgu1c6xv/view?usp=sharing

        Returns:
            NA
        """


        self.start_date = datetime.date(2019, 5, 23)
        self.inv_initial = 150000
        self.capital_account = self.inv_initial #Start at initial investment amount.
        self.duration_expected = datetime.timedelta(5*365)  # "Target Hold Period: 5 to 7 years from closing"

        #Distributions:
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

        def calc_pref(pref_rate, full_quarter=True, date_start_str='', date_end_str='', days_year=364):
            """Calculate the amount of pref, based on a 364 day year

            Args:
                full_quarter: Boolean, True if is a full quarter.  If False, dates for start/end must be entered.
                date_start_str: String, starting day of period.  '2019-01-01' format.
                date_end_str: String, ending day of period
                pref_rate: Annual interest rate.  i.e. 0.08 = 8%
                days_year: Number of days per year (for interest calculations)

            Note: The calculations are from "midnight to midnight".  They
            include the full start day and none of the "final day".
            So, you can re-use the same date for the end of one period and the
            start of the next.

            ToDo: Add Decimal support.  IIUC, add quantization just before returning user-visible values.
            """
            if full_quarter:
                # Days per quarter is 90, 91, 92, 92 (91.25 avg).  Leap years (2020) have 91 days in 1st quarter.
                # I assume they will do a simple "equal amt per quarter".
                pref_amt = 0.25 * pref_rate * self.capital_account
            else:
                date_start = datetime.datetime.strptime(date_start_str, '%Y-%m-%d').date()
                date_end = datetime.datetime.strptime(date_end_str, '%Y-%m-%d').date()
                days = (date_end - date_start).days
                pref_amt = (float(days)/days_year) * pref_rate * self.capital_account
            return dollar(pref_amt) #Quantize to 0.01

        class trans(object):

            def __init__(self, date, amount):
                """Transaction

                Args:
                    date: String, will be converted to a datetime.date, in '2019-01-01' format.
                    amount: Decimal.
                """
                self.date = date
                self.amount = amount

            def __repr__(self):
                return '{}, {}'.format(self.date, self.amount)

        pref_table_raw = [
            #Year 1, 8% pref
            # 7/30/2019	Saddle Investmen Ach Pmt x x6780 Q2 2019 Distribution		$923.08	PREFERRED CHECKING	xxxx1428	Wells Fargo
            # This appears to be a 364 day year?  923.08 / (150000*0.08 / 364) = 28.0000933333 days.  If I use 365 it is 28.077.
            # Not sure why 364 days (can't divide by 12).  But, that appears to
            # be one of the accepted "conventions":  https://en.wikipedia.org/wiki/Day_count_convention

            # Try to calculate the "exact" amounts (dates don't quite line up on quarters, etc.)
            # This tests the ability to easily do "exact" calculations later on.

            # list of {trans_date, pref_amount, },
            # ToDo: Make this a class?  i.e. defined fields for transactions?
            trans('2019-07-30', calc_pref(0.080, False, '2019-06-03', '2019-07-01', 364)), # June 3-June 30.  First year is later (on 7-30)
            trans('2019-10-15', calc_pref(0.080, True)), # 07-01 thru 10-01
            trans('2020-01-15', calc_pref(0.080, True)), # 10-01 thru 01-01
            trans('2020-04-15', calc_pref(0.080, True)), # 01-01 thru 04-01
            trans('2020-07-15', calc_pref(0.080, False, '2020-04-01', '2020-06-03', 364)), # 04-01 thru 06-03

            # 2nd year.
            trans('2020-07-15', calc_pref(0.085, False, '2020-06-03', '2020-07-01', 364)), # New pref rate.
            trans('2020-10-15', calc_pref(0.085, True)),  # 07-01 thru 10-01
            trans('2021-01-15', calc_pref(0.085, True)),  # 10-01 thru 01-01
            trans('2021-04-15', calc_pref(0.085, True)),  # 01-01 thru 04-01
            trans('2021-07-15', calc_pref(0.085, False, '2021-04-01', '2021-06-03', 364)), # 04-01 thru 06-03

            # 3rd year
            trans('2021-07-15', calc_pref(0.090, False, '2021-06-03', '2021-07-01', 364)), # New pref rate.
            trans('2021-10-15', calc_pref(0.090, True)),  # 07-01 thru 10-01
            trans('2022-01-15', calc_pref(0.090, True)),  # 10-01 thru 01-01
            trans('2022-04-15', calc_pref(0.090, True)),  # 01-01 thru 04-01
            trans('2022-07-15', calc_pref(0.090, False, '2022-04-01', '2022-06-03', 364)), # 04-01 thru 06-03

            # 4th year
            trans('2022-07-15', calc_pref(0.095, False, '2022-06-03', '2022-07-01', 364)), # New pref rate.
            trans('2022-10-15', calc_pref(0.095, True)),  # 07-01 thru 10-01
            trans('2023-01-15', calc_pref(0.095, True)),  # 10-01 thru 01-01
            trans('2023-04-15', calc_pref(0.095, True)),  # 01-01 thru 04-01
            trans('2023-07-15', calc_pref(0.095, False, '2023-04-01', '2023-06-03', 364)), # 04-01 thru 06-03

            # 5th year and later, always 10% pref.
            trans('2023-07-15', calc_pref(0.100, False, '2022-06-03', '2022-07-01', 364)), # New pref rate.
            trans('2023-10-15', calc_pref(0.100, True)),  # 07-01 thru 10-01
            trans('2024-01-15', calc_pref(0.100, True)),  # 10-01 thru 01-01
            trans('2024-04-15', calc_pref(0.100, True)),  # 01-01 thru 04-01
            trans('2024-07-15', calc_pref(0.100, True)),  # 04-01 thru 07-01

            # 6th year
            trans('2024-10-15', calc_pref(0.100, True)),  # 07-01 thru 10-01
            trans('2025-01-15', calc_pref(0.100, True)),  # 10-01 thru 01-01
            trans('2025-04-15', calc_pref(0.100, True)),  # 01-01 thru 04-01
            trans('2025-07-15', calc_pref(0.100, True)),  # 04-01 thru 07-01

            # 7th year
            trans('2025-10-15', calc_pref(0.100, True)),  # 07-01 thru 10-01
            trans('2026-01-15', calc_pref(0.100, True)),  # 10-01 thru 01-01
            trans('2026-04-15', calc_pref(0.100, True)),  # 01-01 thru 04-01
            trans('2026-07-15', calc_pref(0.100, True)),  # 04-01 thru 07-01
            ]

        print(pref_table_raw)
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

        print(self.pref_table)

        #TEMPORARY
        import datetime as dt
        import matplotlib.pyplot as plt
        # https://stackoverflow.com/questions/48439005/pycharm-jupyter-interactive-matplotlib/48695728
        #import matplotlib
        #matplotlib.use('Qt5Agg')
        #import Matplotlib.pyplot as plt

        x = [ dt.datetime.strptime(i.date, '%Y-%m-%d') for i in self.pref_table ]
        y = [float(i.amount) for i in self.pref_table]
        plt.plot(x,y, '.-r')
        plt.ylim([0, 4000])
        plt.show()



        #OLD BELOW HERE!!!

        #Setup simpy
        self.env = env
        self.period_days = 30

        # Create a "process" that knows how to calculate the next monthly payment.
        #self.mortgage_process = env.process(self.monthly_payment())

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


env = simpy.Environment(initial_time=timestamp(datetime.date.today()))

# mortgage_simple(
#     env,
#     start_date=datetime.date.today(),
#     loan_amount=100000, length_years=15, interest_rate=0.04,
#     private_mortgage_insur=0.0, )
env.run()
a = Inv_03l_SchneidersSaddlery()
print("Done!!!")
