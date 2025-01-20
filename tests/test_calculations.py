import pytest
from app.calculations import add

@pytest.mark.parametrize("num1, num2, expected", [(1, 2, 3), (99, 100, 199), (99, 1, 100)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected
