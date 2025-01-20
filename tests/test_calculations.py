import pytest
from app.calculations import add, BankAccount
#pytest -v --> to run the test in verbose mode
#pytest -v -k "test_add" --> to run the test in verbose mode and only the test that has the name test_add
#pytest -v -s --> to run the test in verbose mode and show the print statements

@pytest.mark.parametrize("num1, num2, expected", [(1, 2, 3), (99, 100, 199), (99, 1, 100)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

def test_bank_set_initial_amount():
    bank_account = BankAccount(100)
    assert bank_account.balance == 100

def test_bank_defauult_amount():
    bank_account = BankAccount()
    assert bank_account.balance == 0

def test_bank_deposit():
    bank_account = BankAccount(10)
    bank_account.deposit(100)
    assert bank_account.balance == 110

def test_bank_withdraw():
    bank_account = BankAccount(100)
    bank_account.withdraw(51)
    assert bank_account.balance == 49

def test_bank_collect_interest():
    bank_account = BankAccount(100)
    bank_account.collect_interest()
    assert round(bank_account.balance,5) == 110