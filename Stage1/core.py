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

def load_fee_records_from_file(filepath:str) -> list[FeeRecord]:
    """
    >>> import tempfile
    >>> import os
    >>> data ="late_payment,exempt,amount\\nTrue,False,500.00\\nFalse,False,200.00\\nTrue,True,300.00"
    >>> tmp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.csv')
    >>> _ = tmp_file.write(data)
    >>> tmp_file.close()
    >>> fee_records = load_fee_records_from_file(tmp_file.name)
    >>> fee_records[0].late_payment
    True
    >>> fee_records[0].exempt
    False
    >>> fee_records[0].amount
    500.0
    >>> load_fee_records_from_file("non_existent_file.csv")
    Traceback (most recent call last):
    ...
    FileNotFoundError: File not found: non_existent_file.csv

    """

    path = Path(filepath)

    if not path.exists():
        logger.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"File not found: {filepath}")
    
    fee_records: list[FeeRecord] = []
    with path.open("r") as f:
        next(f,None)

        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                late_payment, exempt, amount = line.split(",")
                late_payment_value = late_payment.strip().lower() == "true"
                exempt_value = exempt.strip().lower() == "true"
                amount_value = float(amount.strip())

                fee_records.append(FeeRecord(
                    late_payment=late_payment_value,
                    exempt=exempt_value,
                    amount=amount_value
                ))
                logger.info(f"Successfully loaded record: {fee_records[-1]}")
            except ValueError:
                logger.error(f"Invalid line format: {line}")
                continue
    

    return fee_records

def analyze_fee_records(fee_records: list[FeeRecord]) -> dict:
    """
    >>> records = [
    ...     FeeRecord(late_payment=True, exempt=False, amount=5),
    ...     FeeRecord(late_payment=False, exempt=False, amount=3),
    ...     FeeRecord(late_payment=True, exempt=True, amount=110),]
    >>> result = analyze_fee_records(records)
    >>> result["is_active"]
    True
    >>> result["payment_status"]
    'active'
    >>> result["discount_applicable"]
    False
    >>> result["late_payments_count"]
    2
    >>> result["exempt_count"]
    1
    >>> result["total_amount"]
    118
    >>> result["total_records"]
    3

    """

    is_active, status = payment_status(fee_records)
    discount_applicable = is_discount_applicable(fee_records)

    late_payment_counter = Counter(record.late_payment for record in fee_records)
    exemp_counter = Counter(record.exempt for record in fee_records)
    total_records = len(fee_records)
    total_amount = sum(record.amount for record in fee_records)

    analysis_result = {
        "is_active" : is_active,
        "payment_status": status,
        "discount_applicable": discount_applicable,
        "late_payments_count": late_payment_counter[True],
        "exempt_count": exemp_counter[True],
        "total_amount": total_amount,
        "total_records": total_records
    }
   
    logger.info(f"Analysis result: {analysis_result}")

    return analysis_result


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)