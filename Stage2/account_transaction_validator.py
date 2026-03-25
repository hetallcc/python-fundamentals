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


class TransactionValidator:
    def __init__(self, transaction_fee: Decimal = Decimal("0.00"), overdraft_fee: Decimal = Decimal("0.00")) -> None:
        self.transaction_fee = transaction_fee
        self.overdraft_fee = overdraft_fee

    def validate_deposit(self,account_id, amount: Decimal) -> bool:
        is_valid_deposit = False
        
        if amount >= 0:
            is_valid_deposit = True

        return {
            "valid": is_valid_deposit,
            "account_id": account_id,
            "type": "deposit",
            **({"amount": amount} if is_valid_deposit else {}),
            **({"reason": "Invalid amount"} if not is_valid_deposit else {}) 
        }

    def validate_withdrawal(self,account_id, amount: Decimal, balance: Decimal, overdraft: Decimal) -> dict[str, any]:

        if amount <= 0:
            return {
                "valid": False,
                "account_id": account_id,
                "type": "withdrawal",
                "reason": "Amount must be positive"
            }

        available_funds = balance + overdraft
        if amount > available_funds:
                return {
                    "valid": False,
                    "account_id": account_id,
                    "type": "withdrawal",
                    "reason": "Withdrawal exceeds available funds"
                }
              

        new_balance = balance - amount
        fee=self.transaction_fee
        if new_balance < 0:
            fees += self.overdraft_fee
        
        new_balance -= fee
        
        return{
            "valid": True,
            "account_id": account_id,
            "type": "withdrawal",
            "amount": amount,
            "remaining_balance": new_balance,
            **({"fees": fee} if fee > 0 else {})
        }
    
    def validate_transfer(self, from_account, too_account, amount: Decimal, balance: Decimal):
        is_valid = validate_amount(amount)
        if not is_valid:
            return {
                "valid": False,
                "from_account": from_account,
                "to_account": too_account,
                "reason": "Invalid amount"
            }
        
        total_debit = amount + self.transaction_fee
        if total_debit > balance:
            return {
                "valid": False,
                "from_account": from_account,
                "to_account": too_account,
                "reason": f"Insufficient funds (need {total_debit} including fee)"
            }

        return{
            "valid": True,
            "from_account": from_account,
            "to_account": too_account,
            "amount": amount,
            "fees": self.transaction_fee,
            "from_new_balance": balance - total_debit
        }        

       

    

   