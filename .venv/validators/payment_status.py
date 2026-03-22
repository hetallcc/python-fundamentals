from collections import namedtuple
import decimal

FeeRecord = namedtuple('FeeRecord', ['late_payment', 'exempt','amount'])
def payment_status(feeRecord: FeeRecord) -> tuple[bool,str]:
    if not feeRecord:
        return (True, "active")
    


    