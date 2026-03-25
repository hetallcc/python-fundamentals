#Create a transaction validation system for savings and checking accounts with comprehensive unit tests.

#The functions and methods are intentionally naive to simplify unittest creation.


from decimal import Decimal


def validate_amount(amount: Decimal) -> bool:
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")
    return True

def validate_balance(*,balance: Decimal, withdrawal: Decimal, overdraft: Decimal) -> Decimal:
     available_funds = balance + overdraft
     if withdrawal > available_funds:
        raise ValueError("Withdrawal exceeds available funds")
     return available_funds - withdrawal

def calculate_fees(*fee_components: Decimal) -> Decimal:
    total_fee = sum(fee_components, Decimal("0.00"))
    return total_fee

def process_transaction(**kwargs) -> dict[str, any]:
    """
    >>> result = process_transaction(account_id="A001", amount=Decimal("100"), type="deposit")
    >>> result["status"]
    'success'
    >>> result["account_id"]
    'A001'
    >>> result = process_transaction(account_id="A002", amount=Decimal("-50"), type="withdrawal")
    >>> result["status"]
    'failed'
    >>> result["reason"]
    'Invalid amount'

    """
    if "account_id" not in kwargs:
        return {"error": "Missing account_id"}

    account_id = kwargs.get("account_id")
    amount = kwargs.get("amount", Decimal("0.00"))

    if(amount <= 0):
        return {
            "status": "failed",
            "account_id": account_id,
            "reason": "Invalid amount",
        }
    
    balance = kwargs.get("balance", Decimal("0.00"))
    new_balance = balance + amount

    return {
        "account_id":account_id,
        "amount": amount,
        "transaction_type": kwargs.get("transaction_type", "unknown"),
        "new_balance" : new_balance,
        **({"fees":kwargs.get("fees")} if "fees" in kwargs else {}),
        "fees": kwargs.get("fees"),
        "status": "success"
    }



   