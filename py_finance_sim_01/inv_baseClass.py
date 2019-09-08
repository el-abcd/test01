import datetime
#from dateutil.relativedelta import relativedelta  # To increment dates by a month, etc.
import decimal

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

