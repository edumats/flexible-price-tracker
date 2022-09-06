import pytest
import locale

from selenium import webdriver

from project import (
    convert_string_to_float,
    create_message,
    create_scrapper
)


def test_convert_string_to_float():
    assert convert_string_to_float('45', 'en_US.UTF-8') == float(45)
    assert convert_string_to_float('R$ 45,35', 'pt_BR.UTF-8') == float('45.35')
    assert convert_string_to_float('U$ 45.35', 'en_US.UTF-8') == float('45.35')
    # Testing currency with US formatting
    assert convert_string_to_float(
        '$ 1000.35',
        'en_US.UTF-8') == float('1000.35')
    assert convert_string_to_float(
        'For: $ 10,999.00',
        'en_US.UTF-8') == float('10999.00')
    assert convert_string_to_float(
        '$ 45.35 - $ 75.46',
        'en_US.UTF-8') == float('45.35')

    # Testing currency with BR formatting
    assert convert_string_to_float(
        'Por: R$ 10.999,00',
        'pt_BR.UTF-8') == float('10999.00')
    assert convert_string_to_float(
        '3.490',
        'pt_BR.UTF-8') == float('3490.00')

    # Testing currency with JP formatting
    assert convert_string_to_float(
        'Yen: 10,900',
        'ja_JP.UTF-8') == float('10900')

    # Checking error checking
    with pytest.raises(ValueError):
        convert_string_to_float('abc', 'en_US.UTF-8')
    with pytest.raises(SystemExit):
        convert_string_to_float('...,,,', 'en_US.UTF-8')


def test_create_message():
    item = 'book'
    assert isinstance(create_message(10.5, 15.5, item), str)

    # Test with US locale
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    assert create_message(
        10.5, 15.5, item
    ) == 'The price of book has gone down to $10.50'
    assert create_message(
        16,
        15,
        item
    ) == 'Current price of $16.00 is higher than target price of $15.00'

    # Test with BR locale
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    assert create_message(
        1001,
        1000,
        item
    ) == ('Current price of R$ 1001,00 is '
          'higher than target price of R$ 1000,00')


def test_create_scrapper():
    url = 'www.google.com'
    assert isinstance(create_scrapper(url), webdriver.Chrome)
