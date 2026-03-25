#Test suite structure
import json
from pathlib import Path
import unittest
from decimal import Decimal
from Stage2.account_transaction_validator import TransactionValidator, calculate_fees, process_transaction, validate_amount, validate_balance


class TestValidationFunctions(unittest.TestCase):
    def test_validate_amount(self):
        self.assertTrue(validate_amount(Decimal("10.00")))
        with self.assertRaises(ValueError):
            validate_amount(Decimal("0.00"))
        with self.assertRaises(ValueError):
            validate_amount(Decimal("-1.00"))

    def test_validate_balance(self):
        result = validate_balance(
            balance=Decimal("100.00"),
            withdrawal=Decimal("20.00"),
            overdraft=Decimal("50.00"),
        )
        self.assertEqual(result, Decimal("130.00"))

        with self.assertRaises(ValueError):
            validate_balance(
                balance=Decimal("100.00"),
                withdrawal=Decimal("200.00"),
                overdraft=Decimal("50.00"),
            )

    def test_calculate_fees(self):
        self.assertEqual(calculate_fees(Decimal("1.00"), Decimal("2.00")), Decimal("3.00"))
        self.assertEqual(calculate_fees(), Decimal("0.00"))
        
class TestProcessTransaction(unittest.TestCase):
    def test_process_transaction_success(self):
        result = process_transaction(account_id="A001", amount=Decimal("100.00"))
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["account_id"], "A001")

    def test_process_transaction_invalid_amount(self):
        result = process_transaction(account_id="A001", amount=Decimal("-10.00"))
        self.assertEqual(result["status"], "failed")
        self.assertIn("reason", result)

    def test_process_transaction_missing_account_id(self):
        result = process_transaction(amount=Decimal("10.00"))
        self.assertIn("error", result)

class TestEdgeCases(unittest.TestCase):
    def setUp(self): #run before each test
        self.validator = TransactionValidator(
            transaction_fee=Decimal("2.00"),
            overdraft_fee=Decimal("10.00"),
        )

    def tearDown(self): #run after each test
        pass

    def test_exact_balance_withdrawal(self):
        result = self.validator.validate_withdrawal(
            "A100", Decimal("100.00"), Decimal("100.00"), Decimal("0.00")
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["remaining_balance"], Decimal("-2.00"))  # if transaction fee applies

    def test_very_small_amount(self):
        result = process_transaction(account_id="A200", amount=Decimal("0.01"))
        self.assertEqual(result["status"], "success")
        self.assertGreater(result["amount"], Decimal("0.00"))

class TestTransactionValidator(unittest.TestCase):
    def setUp(self):
        self.validator = TransactionValidator()

        # load JSON test data
        self.file = open(
            Path(__file__).with_name("test_accounts_data.json"),
            "r",
            encoding="utf-8",
        )
        self.test_accounts = json.load(self.file)

    def tearDown(self):
        if hasattr(self, "file") and self.file and not self.file.closed:
            self.file.close()

    def test_valid_deposit(self):
        acc = self.test_accounts["savings"]
        result = self.validator.validate_deposit(acc["id"], Decimal("100.00"))
        self.assertTrue(result["valid"])

    def test_invalid_deposit(self):
        acc = self.test_accounts["savings"]
        result = self.validator.validate_deposit(acc["id"], Decimal("-1.00"))
        self.assertFalse(result["valid"])

    def test_valid_withdrawal(self):
        acc = self.test_accounts["checking"]
        result = self.validator.validate_withdrawal(
            acc["id"],
            Decimal("100.00"),
            Decimal(acc["balance"]),
            Decimal(acc["overdraft"]),
        )
        self.assertTrue(result["valid"])
        self.assertIn("remaining_balance", result)

    def test_insufficient_funds(self):
        acc = self.test_accounts["low_balance"]
        result = self.validator.validate_withdrawal(
            acc["id"],
            Decimal("100.00"),
            Decimal(acc["balance"]),
            Decimal(acc["overdraft"]),
        )
        self.assertFalse(result["valid"])

if __name__ == "__main__":
    unittest.main(verbosity=2)