import pytest
import locale
from unittest.mock import Mock

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from project import (
    convert_string_to_float,
    create_message,
    create_scrapper,
    scrap_page,
    extract_time
)


def test_convert_string_to_float():
    # Using en_US.UTF-8 locale
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    assert convert_string_to_float('45') == float(45)
    assert convert_string_to_float('U$ 45.35') == float('45.35')
    # Testing currency with US formatting
    assert convert_string_to_float('$ 1000.35') == float('1000.35')
    assert convert_string_to_float(
        'For: $ 10,999.00') == float('10999.00')
    assert convert_string_to_float('$ 45.35 - $ 75.46') == float('45.35')
    assert convert_string_to_float('45.35') == float('45.35')

    # Testing currency with BR formatting
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    assert convert_string_to_float('R$ 45,35') == float('45.35')
    assert convert_string_to_float('Por: R$ 10.999,00') == float('10999.00')
    assert convert_string_to_float('3.490') == float('3490.00')

    # Testing currency with JP formatting
    locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')
    assert convert_string_to_float('Yen: 10,900') == float('10900')

    # Checking error checking
    with pytest.raises(ValueError):
        convert_string_to_float('abc')
    with pytest.raises(SystemExit):
        convert_string_to_float('...,,,')


def test_create_message():
    # Tests if returns instance of str
    item = 'book'
    assert isinstance(create_message(10.5, 15.5, item), tuple)

    # Test with US locale
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    assert create_message(
        10.5, 15.5, item) == (
            'Price down to $10.50',
            'Low price alert of book'
        )
    assert create_message(
        16,
        15,
        item
    ) == (
        'Price higher than target price',
        'Current price of $16.00 is higher than target price of $15.00'
    )

    # Test with BR locale
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    assert create_message(
        1001,
        1000,
        item
    ) == (
          'Price higher than target price',
          'Current price of R$1001,00 is '
          'higher than target price of R$1000,00'
        )


def test_create_scrapper():
    # Tests if return instance of Chrome webdriver
    assert isinstance(create_scrapper(), webdriver.Chrome)


def test_scrap_page():
    # Checks if returns tuple with defined values
    class MockResponse:
        text = '$100.00'

    url = 'https://www.google.com'
    xpath = '.'
    driver = Mock(title='Google')
    driver.find_element.return_value = MockResponse()
    assert scrap_page(url, xpath, driver) == ('$100.00', 'Google')

    # Check if exception triggers SystemExit
    with pytest.raises(SystemExit):
        driver.find_element.side_effect = NoSuchElementException
        scrap_page(url, xpath, driver)

    # Check if raises error if element is empty
    with pytest.raises(SystemExit):
        empty_mock = MockResponse()
        empty_mock.text = ''
        driver.find_element.return_value = empty_mock
        scrap_page(url, xpath, driver)


def test_extract_time():
    # Tests if returns expected values
    assert extract_time('m1') == ('m', 1)
    assert extract_time('h10') == ('h', 10)
    assert extract_time('d100') == ('d', 100)

    # Tests if raises ValueError if wrong inputs are provided
    with pytest.raises(ValueError):
        extract_time('mm')
    with pytest.raises(ValueError):
        extract_time('a5')
