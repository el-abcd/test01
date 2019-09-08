import datetime
#from dateutil.relativedelta import relativedelta  # To increment dates by a month, etc.
import decimal

import numpy as np
import pandas as pd
import simpy

# Try to simulate a mortgage!!!

# ToDo: Fix up when there is time (timestamp moved out, etc. )

# ToDo: This is using simpy, can leave here for now.  Should refactor in the future though.
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


if __name__ == "__main__":
    env = simpy.Environment(initial_time=timestamp(datetime.date.today()))

    # mortgage_simple(
    #     env,
    #     start_date=datetime.date.today(),
    #     loan_amount=100000, length_years=15, interest_rate=0.04,
    #     private_mortgage_insur=0.0, )
    env.run()
    # a = Inv_03l_SchneidersSaddlery()
    print("Done!!!")
