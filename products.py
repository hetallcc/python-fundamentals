from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Protocol
from enum import Enum

class ProductProtocol(Protocol):
    def get_config(self) -> dict[str, any]:
        """Return product configuration"""
        ...

class ProductName(Enum):
    SAVINGS_ACCOUNT = "savings_account"
    CHECKING_ACCOUNT = "checking_account"
    MONEY_MARKET = "money_market"


@dataclass
class savingsAccount:
    """
    >>> account = savingsAccount()
    >>> account.name
    'Savings Account'
    >>> account.interest_rate
    2.5
    >>> account.has_savings
    True
    >>> config = account.get_config()
    >>> config['name']
    'Savings Account'
    >>> config['interest_rate']
    2.5
    >>> config['has_savings']
    True
    """
    _id: str = "savings_account"
    name: str = "Savings Account"
    interest_rate: float = 2.5
    has_savings: bool = field(default=True, init=False)
    starting_balance: Decimal = field(default=Decimal('0.00'), init=False)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
        
    def get_config(product: ProductProtocol) -> dict[str, any]:
        return {
            "id": product._id,
            "name": product.name,
            "interest_rate": product.interest_rate,
            "has_savings": product.has_savings,
            "starting_balance": product.starting_balance,
            "created_at": product.created_at.isoformat()
        }

@dataclass
class CheckingAccount:
    """
    """
    _id: str = "checking_account"
    name: str = "Checking Account"
    interest_rate: float = 0.1
    has_savings: bool = field(default=False, init=False)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def get_config(product: ProductProtocol) -> dict[str, any]:
        return {
            "id": product._id,
            "name": product.name,
            "interest_rate": product.interest_rate,
            "has_savings": product.has_savings,
            "created_at": product.created_at.isoformat()
        }

@dataclass
class MoneyMarket:
    _id: str = "money_market"
    name: str = "Money Market"
    interest_rate: float = 4.0
    has_savings: bool = field(default=True, init=False)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def get_config(product: ProductProtocol) -> dict[str, any]:
        return {
            "id": product._id,
            "name": product.name,
            "interest_rate": product.interest_rate,
            "has_savings": product.has_savings,
            "created_at": product.created_at.isoformat()
        }
  
_PRODUCT_MAP = {
    ProductName.SAVINGS_ACCOUNT: savingsAccount,
    ProductName.CHECKING_ACCOUNT: CheckingAccount,
    ProductName.MONEY_MARKET: MoneyMarket
}

def create_product(product_name: ProductName) -> ProductProtocol:
    """
    >>> product = create_product(ProductName.SAVINGS_ACCOUNT)
    >>> product.name
    'Savings Account'
    >>> product.interest_rate
    2.5
    >>> product = create_product(ProductName.CHECKING_ACCOUNT)
    >>> product.name
    'Checking Account'
    >>> product.interest_rate
    0.1
    >>> product = create_product(ProductName.MONEY_MARKET)
    >>> product.name
    'Money Market'
    >>> product.interest_rate
    4.0
    >>> create_product("invalid_product")
    Traceback (most recent call last):
    ...
    ValueError: Unknown product name: invalid_product
    
    >>> savings = create_product(ProductName.SAVINGS_ACCOUNT)
    >>> savings.interest_rate
    2.5
    >>> savings.interest_rate = 3.5
    >>> savings.interest_rate
    3.5
    >>> savings.get_config()['interest_rate']
    3.5
    >>> checking = create_product(ProductName.CHECKING_ACCOUNT)
    >>> checking.interest_rate
    0.1
    >>> checking.interest_rate = 0.5
    >>> checking.interest_rate
    0.5
    >>> money_market = create_product(ProductName.MONEY_MARKET)
    >>> money_market.interest_rate
    4.0
    >>> money_market.interest_rate = 4.5
    >>> money_market.interest_rate
    4.5
     
    """
    product_class = _PRODUCT_MAP.get(product_name)
    if not product_class:
        raise ValueError(f"Unknown product name: {product_name}")
    return product_class()

def get_product_name(id: str) -> ProductName:
    try:
        return ProductName(id)
    except ValueError:
        return "Unknown Product"

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)