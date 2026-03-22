from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import doctest


def next_payment_date(current_date:datetime, day_of_month: int)-> datetime:
    """
    >>> next_payment_date(datetime(2024, 1, 15), 20)
    datetime.datetime(2024, 1, 20, 0, 0)

    >>> next_payment_date(datetime(2024, 1, 20), 20)
    datetime.datetime(2024, 2, 20, 0, 0)
    >>> next_payment_date(datetime(2024, 2, 29), 31)
    datetime.datetime(2024, 3, 31, 0, 0)
    >>> next_payment_date(datetime(2024, 2, 1), 31)
    datetime.datetime(2024, 2, 29, 0, 0)
    >>> next_payment_date(datetime(2023, 2, 1), 31)
    datetime.datetime(2023, 2, 28, 0, 0)
    """

    if day_of_month < 1 or day_of_month > 31:
        raise ValueError("Day of month must be between 1 and 31")
    
    target_date = current_date if current_date.day < day_of_month else current_date + relativedelta(months=1)

    try:
        return target_date.replace(day=day_of_month)
    except ValueError:
        last_day_of_month = calendar.monthrange(target_date.year, target_date.month)[1]
        return target_date.replace(day=last_day_of_month)


    #easier to ask forgiveness than permission (EAFP)

   
if __name__ == "__main__":
    doctest.testmod(verbose=True)
