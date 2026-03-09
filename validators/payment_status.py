from collections import namedtuple
from decimal import Decimal

FeeRecord = namedtuple('FeeRecord', ['late_payment', 'exempt','amount'])

def payment_status(feeRecord: FeeRecord) -> tuple[bool,str]:
    """
    >>> payment_status([FeeRecord(True, False, Decimal("5"))])
    (True, 'active')
    >>> payment_status([FeeRecord(True, False, Decimal("11"))])
    (False, 'delinquent')
    >>> payment_status([FeeRecord(True, False, Decimal("6")), FeeRecord(True, False, Decimal("5"))])
    (False, 'delinquent')
    >>> payment_status([FeeRecord(True, True, Decimal("2000"))])
    (True, 'active')
    >>> payment_status([FeeRecord(False, False, Decimal("2000"))])
    (True, 'active')
    >>> payment_status([FeeRecord(True, False, Decimal("5")), FeeRecord(True, True, Decimal("1000"))])
    (True, 'active')
    >>> payment_status([FeeRecord(True, False, Decimal("10"))])
    (True, 'active')
    >>> payment_status([FeeRecord(True, False, Decimal("10.01"))])
    (False, 'delinquent')
    >>> payment_status([])
    (True, 'active')
    """
    total_late_payment = sum(
        Decimal(str(record.amount))
        for record in feeRecord
        if record.late_payment and not record.exempt
    )

    if total_late_payment > 10:
        return (False, "delinquent")
    else:
        return (True, "active")
    

def is_discount_applicable(feeRecord: FeeRecord) -> bool:
    """
    >>> is_discount_applicable([FeeRecord(late_payment=False, exempt=False, amount=Decimal("500"))])
    True
    >>> is_discount_applicable([FeeRecord(late_payment=True, exempt=True, amount=Decimal("500"))])
    True
    >>> is_discount_applicable([FeeRecord(late_payment=True, exempt=False, amount=Decimal("500"))])
    False
    >>> is_discount_applicable([FeeRecord(late_payment=False, exempt=False, amount=Decimal("500")), FeeRecord(late_payment=True, exempt=True, amount=Decimal("300"))])
    True
    >>> is_discount_applicable([FeeRecord(late_payment=False, exempt=False, amount=Decimal("500")), FeeRecord(late_payment=True, exempt=False, amount=Decimal("300"))])
    False
    >>> is_discount_applicable([])
    True
    """
    all_eligible_for_discount = all(
        not record.late_payment or record.exempt
        for record in feeRecord
        )

    if all_eligible_for_discount:
        return True
    return False

    if __name__ == "__main__":
        import doctest
    doctest.testmod(verbose=True)