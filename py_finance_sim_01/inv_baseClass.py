import datetime
#from dateutil.relativedelta import relativedelta  # To increment dates by a month, etc.
import decimal
import pandas as pd
import numpy as np

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


def calc_pref(pref_rate, capital_account, full_period=None, date_start_str='', date_end_str='',
              days_year=364):
    """Calculate the amount of pref, based on a 364 day year.

    Started with Schneider Saddlery.

    Args:
        pref_rate: Annual interest rate.  i.e. 0.08 = 8%
        capital_account: Value to use for "simple" interest calculations.

        full_period: String/None/False.  None if date_start_str and date_end_str should be used.
            'q' if it should calculate a full quarter.  'm' if it should calculate a month.
        date_start_str: String, starting day of period.  '2019-01-01' format.
        date_end_str: String, ending day of period
        days_year: Number of days per year (for interest calculations)

    Note: The calculations are from "midnight to midnight".  They
    include the full start day and none of the "final day".
    So, you can re-use the same date for the end of one period and the
    start of the next.
    """
    if full_period == 'q':
        # Days per quarter is 90, 91, 92, 92 (91.25 avg).  Leap years (2020) have 91 days in 1st quarter.
        # I assume they will do a simple "equal amt per quarter".
        pref_amt = (pref_rate / 4.0) * capital_account
    elif full_period == 'm':
        pref_amt = (pref_rate / 12.0) * capital_account
    elif (full_period is None) or (full_period == False):
        date_start = datetime.datetime.strptime(date_start_str,
                                                '%Y-%m-%d').date()
        date_end = datetime.datetime.strptime(date_end_str, '%Y-%m-%d').date()
        days = (date_end - date_start).days
        pref_amt = (float(days) / days_year) * pref_rate * capital_account
    else:
        # full_period value is invalid.
        raise(ValueError)
    return dollar(pref_amt)  # Quantize to 0.01

def quarterly_to_monthly(dataframe):
    """Convert quarterly payments to equivalent ones

    This allows easier comparison of various investments, and simpler calculations of
    "equivalent" monthly income.
    This is a bit "conservative" as it will:
    * Resample to the END of the month (i.e. a payment on Jan 01 is moved to Jan 31)
    * Spread that quarterly payment over that month (and the next 2).

    For example, a payment on 01/01/2019 of $300 is recorded as
        2019-01-31, $100,
        2019-02-28, $100,
        2019-03-31, $100
    """
    # Resample to "month end" dates.
    # If have "simple" quarterly payments it will look like $100,0,0,$100,0,0,...$100
    b = dataframe.resample('m').sum()
    # Add 2 more months to the end (pad it) so the last element ALSO has trailing 0's.
    b[b.index[-1] + pd.offsets.MonthEnd(1)] = 0
    b[b.index[-1] + pd.offsets.MonthEnd(1)] = 0

    #Use a simple "boxcar" filter.  Typically there are 2 0's after each payment
    # So only 1 payment is IN the boxcar at any time, and it returns the same
    # value for 3 points.
    # Remove the "extra" points at the end.  They were added above (with the proper dates)
    b.values = np.convolve(b.values, [1.0/3, 1.0/3, 1.0/3], 'full')[0:-2]

    return pd.Series(data=b,index=b.index)

class Transact(object):
    # ToDo: Add other columns (tax, etc).
    # ToDo: add converters to csv, json, qif, etc.

    def __init__(self, date, amount):
        """Transaction

        Args:
            date: Datetime.date or String, will be converted to a datetime.date, in '2019-01-01' format.
            amount: Decimal.

        Returns:
            Class instance
        """
        if isinstance(date, datetime.date):
            self.date = date
        elif isinstance(date, str):
            self.date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        else:
            raise(ValueError)
        self.amount = amount

    def __repr__(self):
        return '\n{}, {}'.format(self.date, self.amount)

class inv_base(object):
    """ Base class for investments

    Define common variables, classes, etc.

    ToDo: Add a "description" field for an overview.  Make it a readonly parameter?
    """
    def __init__(self, short_name, description):
        self.short_name = short_name
        self.description = description
        self.df = None #ToDo: How to force this to be set?  And be a DataFrame?  DataClass? etc?

        # Do some calculations (smooth quarterly to monthly) for quarterly investments (which are common).
        # Only need to over-ride this for investments that are quarterly, leave it at None for others.
        self.is_quarterly = None

    #ToDo: Make this a dataclass? (python 3.7).  Can enforce elements, etc.
    #   Or, use composition?  Feed in defined values, then add more on?
    #ToDo: Have this raise an exception when an instance is created, not just accessed?
    #@property
    #def description(self):
        #raise NotImplementedError('Subclasses should implement this')

    def quarterly_to_month_end(self):
        """Convert quarterly payments to equivalent ones

        This allows easier comparison of various investments, and simpler calculations of
        "equivalent" monthly income.
        This is a bit "conservative" as it will:
        * Resample to the END of the month (i.e. a payment on Jan 01 is moved to Jan 31)
        * Spread that quarterly payment over that month (and the next 2).

        For example, a payment on 01/01/2019 of $300 is recorded as
            2019-01-31, $100,
            2019-02-28, $100,
            2019-03-31, $100
        """
        # Resample to "month end" dates.
        # If have "simple" quarterly payments it will look like $100,0,0,$100,0,0,...$100
        # https://stackoverflow.com/a/34270422 Resample drops non-numeric columns!
        b = self.df.resample('m').sum()

        if self.base.is_quarterly:
            # b is now a single column, non-numberical columns get DROPPED by the sum.  Add them back later.
            # Add 2 more months to the end (pad it) so the last element ALSO has trailing 0's.
            b.loc[b.index[-1] + pd.offsets.MonthEnd(1)] = {'amt':0.0}
            b.loc[b.index[-1] + pd.offsets.MonthEnd(1)] = {'amt':0.0}

            # Use a simple "boxcar" filter.  Typically there are 2 0's after each payment
            # So only 1 payment is IN the boxcar at any time, and it returns the same
            # value for 3 points.
            # Remove the "extra" points at the end.  They were were already added above (with the proper dates)
            new_list = np.convolve(b['amt'].tolist(), [1.0 / 3, 1.0 / 3, 1.0 / 3], 'full')[
                       0:-2]

            b['amt'] = new_list

            #print(self.df['amt'].sum())
            #print( sum(new_list) )
            #Check the old and new sum match (within 0.1 cent)
            assert( abs(self.df['amt'].sum() - sum(new_list)) <= 0.001 )

        b['inv_name'] = self.df.iloc[0]['inv_name']
        #Return a dataframe (not just a series, so the inv_name is also there...
        return b #pd.Series(data=new_list, index=b.index)

