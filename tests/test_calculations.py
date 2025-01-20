import pytest
from app.calculations import add, BankAccount
#pytest -v --> to run the test in verbose mode
#pytest -v -k "test_add" --> to run the test in verbose mode and only the test that has the name test_add
#pytest -v -s --> to run the test in verbose mode and show the print statements
# fixtures --> minimize the code duplication

@pytest.fixture
def bank_account_zero():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(100)

@pytest.mark.parametrize("num1, num2, expected", [(1, 2, 3), (99, 100, 199), (99, 1, 100)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 100

def test_bank_defauult_amount(bank_account_zero):
    assert bank_account_zero.balance == 0

def test_bank_deposit(bank_account):
    bank_account.deposit(10)
    assert bank_account.balance == 110

def test_bank_withdraw(bank_account):
    bank_account.withdraw(51)
    assert bank_account.balance == 49

def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance,5) == 110


@pytest.mark.parametrize("deposit, withdraw, expected", [(100, 50, 50), (100, 100, 0), (200, 100, 100)])
def test_bank_transaction(bank_account_zero, deposit, withdraw, expected):
    bank_account_zero.deposit(deposit)
    bank_account_zero.withdraw(withdraw)
    assert bank_account_zero.balance == expected