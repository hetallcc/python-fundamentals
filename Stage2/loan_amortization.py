# loan amortization calculator with advance date handling

from bisect import bisect
from calendar import calendar
from datetime import date, timedelta
from decimal import Decimal as decimal, ROUND_HALF_UP


class DayCountConvention:
    @staticmethod
    def actual_365(start_date: date, end_date: date) -> decimal:
        daysBetween = (end_date - start_date).days
        year_fraction = decimal(daysBetween) / decimal(365)
        return year_fraction
    
    @staticmethod
    def actual_360(start_date: date, end_date: date) -> decimal:
        daysBetween = (end_date - start_date).days
        year_fraction = decimal(daysBetween) / decimal(360)
        return year_fraction

    @staticmethod
    def thirty_360(start_date: date, end_date: date) -> decimal:
        year_fraction = ((end_date.year - start_date.year) * 360 +
                         (end_date.month - start_date.month) * 30 +
                         (end_date.day - start_date.day)) / decimal(360)
        return year_fraction.quantize(decimal('0.0001'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def get_days_in_month(year: int, month:int) -> int:
       return calendar.monthrange(year, month)[1]
    
    @staticmethod
    def adjust_for_business_day(payment_date: date) -> date:
        if payment_date.weekday() >= 5:  # Saturday or Sunday
            payment_date += timedelta(days=1)  # Move to next Monday
        return payment_date
    
    @staticmethod
    def calculate_monthly_payment(principal: decimal, annual_rate: decimal, months: int) -> decimal:
        if(months <=0):
            raise ValueError("Months must be greater than 0")
        
        if annual_rate == 0:
            return (principal / months).quantize(decimal('0.01'), rounding=ROUND_HALF_UP)

        monthly_interest_rate = annual_rate / decimal(12) 
        growth = (1 + monthly_interest_rate) ** months # to the power of months e.g. 2**3= 8
        monthly_payment = (principal * monthly_interest_rate * growth) / (growth -1)
        return monthly_payment.quantize(decimal('0.01'), rounding=ROUND_HALF_UP)
    
class RateSchedule:
    def __init__(self):
        self.dates = list[date] = []
        self.rates = list[decimal] = []

    def add_rate(self, effective_date: date, rate: decimal)-> None:
        #self.rates.append(decimal(str(rate)))
        #self.dates.append(effective_date)

        index = bisect.bisect_left(self.dates, effective_date)

        if index < len(self.dates) and self.dates[index] == effective_date:
            self.rates[index] = decimal(str(rate))
        else:
            self.dates.insert(index, effective_date)
            self.rates.insert(index, decimal(str(rate)))

    def get_rate(self, as_of_date: date) -> decimal:
        index = bisect.bisect_right(self.dates, as_of_date)
        if index < 0:
            raise ValueError("No rates available for the given date")
        return self.rates[index-1]

    def get_rate_schedule(self) -> list[tuple[date, decimal]]:
        return list(zip(self.dates, self.rates))