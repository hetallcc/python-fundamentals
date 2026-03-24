# Create a loan account manager that tracks loan balances, payments, and interest with cached calculations and class-level utilities.

from functools import lru_cache
import csv
import json
from decimal import Decimal
from typing import Union

from Stage1.products import ProductName  


Transaction = dict[str, str | Decimal]
TransactionList = list[Transaction]

class LoanAccount:
    def __init__(self, opening_balance: Decimal,
                 account_id: str,
                 interest_rate: Decimal,
                 original_principal: Decimal,
                 product: ProductName) -> None:
        self._balance = opening_balance
        self.account_id = account_id
        self.interest_rate = interest_rate
        self.original_principal = original_principal
        self.product = product

    @property    
    def balance(self) -> Decimal:
        return self._balance
    
    @balance.setter
    def balance(self, value: Decimal) -> None:
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

    def make_payment(self, amount: Decimal):
        if amount <= 0:
            raise ValueError("Payment amount must be greater than 0")
        if amount > self._balance:
            raise ValueError("Payment amount cannot exceed current balance")
        self._balance -= amount

    def to_dict(self) -> dict[str, str | Decimal]:
        return {
            "balance": self._balance,
            "account_id": self.account_id,
            "interest_rate": self.interest_rate,
            "original_principal": self.original_principal,
            "product": self.product.value
        }
    
    @classmethod
    def from_json(cls, json_string: str) -> "LoanAccount":
        data = json.loads(json_string)
        return cls(
            opening_balance=Decimal(data["balance"]),
            account_id=data["account_id"],
            interest_rate=Decimal(data["interest_rate"]),
            original_principal=Decimal(data["original_principal"]),
            product=ProductName(data["product"]),
        )

    @staticmethod
    def calculate_late_fee(balance: Decimal, days_late: int) -> Decimal:
        if days_late <= 0:
            return Decimal("0.00")
        five_percent = balance * Decimal("0.05")
        late_fee = max(five_percent, Decimal("25.00"))
        if days_late > 10:
            late_fee += Decimal("50.00")
        return late_fee.quantize(Decimal("0.01"))
    
    
class LoanLedger:
        def __init__(self, ledger_name: str) -> None:
            self._loans: dict[str, LoanAccount] = {}
            self.ledger_name = ledger_name
        
        def add_loan(self, loan: LoanAccount) -> None:
            if loan.account_id in self._loans:
                raise ValueError("Loan with this account ID already exists")
            self._loans[loan.account_id] = loan

        @lru_cache(maxsize = 5)
        def calculate_total_balance(self,product: ProductName) -> Decimal:
            total_balance = Decimal('0.00')
            for loan in self._loans.values():
                if loan.product == product:
                    total_balance += loan.balance
            return total_balance
        
        def get_account_ids(self) -> str:
            return ", ".join(self._loans.keys())
        
        def parse_transaction_csv(self, csv_string:str) -> TransactionList:
            transactions: TransactionList = []
            lines = csv_string.strip().split("\n")
            for line in lines:
                balance, interest_rate, account_id, original_principal, product = line.split(",")
                transaction = {
                    "balance": Decimal(balance.strip()),
                    "interest_rate": Decimal(interest_rate.strip()),
                    "account_id": account_id.strip(),
                    "original_principal": Decimal(original_principal.strip()),
                    "product": product.strip()
                }

                transactions.append(transaction)
            return transactions
        def get_ledger_summary(self) -> dict[str, Decimal| str | int | dict[str, Decimal]]:
            """
            >>> ledger = LoanLedger("Summary Test")
            >>> ledger.add_loan(LoanAccount(Decimal("5000"), "L1", Decimal("0.05"), Decimal("5000"), ProductName.SAVINGS_ACCOUNT))
            >>> ledger.add_loan(LoanAccount(Decimal("3000"), "L2", Decimal("0.04"), Decimal("3000"), ProductName.CHECKING_ACCOUNT))
            >>> summary = ledger.get_ledger_summary()
            >>> summary['ledger_name']
            'Summary Test'
            >>> summary['total_loans']
            2
            >>> summary['balances_by_product'][ProductName.SAVINGS_ACCOUNT.value]
            Decimal('5000.00')
            >>> summary['balances_by_product'][ProductName.CHECKING_ACCOUNT.value]
            Decimal('3000.00')
            """
            balances_by_product: dict[str, Decimal] = {}

            for loan in self._loans.values():
                product_name = loan.product.value
                balances_by_product[product_name] = (
                    balances_by_product.get(product_name, Decimal('0.00')) + loan.balance
                )

            dict1: dict[str, str | Decimal] = {
                    "balances_by_product": balances_by_product,
                    "ledger_name": self.ledger_name
               }

            dict2: dict[str, Decimal] = {
                    "total_loans": len(self._loans),
             }

            return {**dict1, **dict2}

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)






    
    


    