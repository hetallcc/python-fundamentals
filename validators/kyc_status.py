from typing import Optional

AGE_RESTRICTED_COUNTRIES = {
    "China": 18,
    "Japan" : 20,
    "UAE": 21
}

BLACKLISTED_IDS = {
    "ID001",
    "ID002",
    "ID003",
    "FAKE123"
}

def check_kyc_status(age:int, id_number: Optional[str], country: str) -> tuple[bool, str]:
    """
    >>> check_kyc_status(25, "ID004", "USA")
    (True, 'KYC check passed')
    >>> check_kyc_status(17, "ID004", "USA")
    (False, 'Customer is underage')
    >>> check_kyc_status(17, "ID004", "China")
    (False, 'Customer is underage')
    >>> check_kyc_status(19, "ID004", "China")
    (True, 'KYC check passed')
    >>> check_kyc_status(19, "ID001", "USA")
    (False, 'Identification is blacklisted')
    >>> check_kyc_status(19, None, "USA")
    (False, 'Identification not provided')
    
    """
    if id_number is None:
        return (False, "Identification not provided")
    if id_number in BLACKLISTED_IDS:
        return (False, "Identification is blacklisted")
    if country in AGE_RESTRICTED_COUNTRIES and age < AGE_RESTRICTED_COUNTRIES[country]:
        return (False, "Customer is underage")
    if(country not in AGE_RESTRICTED_COUNTRIES and age < 18):
        return (False, "Customer is underage")
    return (True, "KYC check passed")
    