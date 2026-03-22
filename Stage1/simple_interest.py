from __future__ import annotations
import doctest
from decimal import Decimal, ROUND_HALF_UP

def simple_interest(principal: Decimal, rate: Decimal, days: int) -> Decimal:
   
    """
    Calculate simple interest using the formula: Interest = (Principal * Rate * Time) / 365
    >>> simple_interest(Decimal('1000'), Decimal('0.05'), 1095)
    Decimal('150.00')

    >>> simple_interest(Decimal('500'), Decimal('0.1'), 182)
    Decimal('24.93')

    >>> simple_interest(Decimal('0'), Decimal('0.05'), 3650)
    Decimal('0.00')

    """

    if not isinstance(principal, Decimal):
        raise TypeError("Principal must be of type Decimal")
    
    if not isinstance(rate, Decimal):
        raise TypeError("Rate must be of type Decimal")
    
    if not isinstance(days, int):
        raise TypeError("Days must be of type int")

    if principal < 0 or rate < 0 or days < 0:
        raise ValueError("Principal, rate, and days cannot be negative.")

    interest = (principal * rate * days) / 365

    return interest.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

if __name__ == "__main__":
    doctest.testmod(verbose=True)