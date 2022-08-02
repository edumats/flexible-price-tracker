import pytest
from project import (
    convert_string_to_float,
    is_price_reduced
)


def test_convert_string_to_float():
    assert convert_string_to_float('45', 'en_US.UTF-8') == float(45)
    assert convert_string_to_float('R$ 45,35', 'pt_BR.UTF-8') == float('45.35')
    assert convert_string_to_float('U$ 45.35', 'en_US.UTF-8') == float('45.35')
    assert convert_string_to_float(
        '$ 1000.35',
        'en_US.UTF-8') == float('1000.35')
    assert convert_string_to_float(
        'Por: R$ 10.999,00',
        'pt_BR.UTF-8') == float('10999.00')
    assert convert_string_to_float(
        'For: $ 10,999.00',
        'en_US.UTF-8') == float('10999.00')
    assert convert_string_to_float(
        'Yen: 10,900',
        'ja_JP.UTF-8') == float('10900')
    assert convert_string_to_float(
        '$ 45.35 - $ 75.46',
        'en_US.UTF-8') == float('45.35')
    assert convert_string_to_float(
        '3.490',
        'pt_BR.UTF-8') == float('3490.00')

    with pytest.raises(ValueError):
        convert_string_to_float('abc', 'en_US.UTF-8')
    with pytest.raises(SystemExit):
        convert_string_to_float('...,,,', 'en_US.UTF-8')


def test_is_price_reduced():
    assert is_price_reduced(1200, 1200) is False
    assert is_price_reduced(1300, 1200)
    assert is_price_reduced(1199, 1200) is False
