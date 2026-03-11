import logging
from pathlib import Path
from collections import Counter

from validators.payment_status import FeeRecord, payment_status, is_discount_applicable

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bank_core.log"),
        logging.StreamHandler()
    ],
)

logger = logging.getLogger(__name__)

def get_last_n_records(fee_records: list[FeeRecord], n:int) -> list[FeeRecord]:
    """
    >>> records = [FeeRecord(True, False, 5), FeeRecord(True, False, 10), FeeRecord(False, False, 0)]
    >>> result = get_last_n_records(records, 2)
    >>> result[0].amount
    10
    >>> result[1].amount
    0
    >>> get_last_n_records(records, 0)
    Traceback (most recent call last):
    ...
    ValueError: n must be greater than 0
    >>> get_last_n_records(records, 5)
    Traceback (most recent call last):
    ...
    ValueError: Requested fee records not available
    >>> get_last_n_records([], 1)
    Traceback (most recent call last):  
    ...
    ValueError: Requested fee records not available
    >>> get_last_n_records(records, 1)
    [FeeRecord(late_payment=False, exempt=False, amount=0)]
    """
    logger.info(f"get_last_n_records called with n={n} and fee_records with length {len(fee_records)}")
    if n <= 0:
        logger.error("n must be greater than 0")
        raise ValueError("n must be greater than 0")
    
    if n > len(fee_records):
        logger.error("Requested fee records not available")
        raise ValueError("Requested fee records not available")
    
    result = fee_records[-n:]

    logger.info(f"Successfully returning {result}")

    return result

def get_middle_n_records(fee_records: list[FeeRecord], n:int) -> list[FeeRecord]:
    """
    >>> records = [
    ...     FeeRecord(late_payment=True, exempt=False, amount=100),
    ...     FeeRecord(late_payment=False, exempt=False, amount=200),
    ...     FeeRecord(late_payment=True, exempt=True, amount=300),
    ...     FeeRecord(late_payment=False, exempt=False, amount=400),
    ...     FeeRecord(late_payment=True, exempt=False, amount=500),
    ... ]
    >>> result = get_middle_n_records(records, 2)
    >>> result[0].amount
    200
    >>> result[1].amount
    300
    >>> get_middle_n_records(records, 0)
    Traceback (most recent call last):
    ...
    ValueError: n must be greater than 0
    >>> get_middle_n_records([], 1)
    Traceback (most recent call last):  
    ...
    ValueError: Requested fee records not available
    >>> get_middle_n_records(records, 1)
    [FeeRecord(late_payment=True, exempt=True, amount=300)]
    """
    logger.info(f"get_middle_n_records called with n={n} and fee_records with length {len(fee_records)}")
    
    if n <= 0:
        logger.error("n must be greater than 0")
        raise ValueError("n must be greater than 0")
    
    if n > len(fee_records):
        logger.error("Requested fee records not available")
        raise ValueError("Requested fee records not available")
    
    start_index = (len(fee_records) - n) // 2
    result = fee_records[start_index:start_index + n]

    logger.info(f"Successfully returning {result}")

    return result

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)