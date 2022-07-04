import pytest
from project import Scrapper, scrap_element, convert_string_to_float, is_price_reduced

def test_scrapper_class():
    pass

def test_convert_string_to_float():
    assert convert_string_to_float('45') == float(45)
    assert convert_string_to_float('R$ 45,35', 'pt_BR') == float('45.35')
    assert convert_string_to_float('U$ 45.35') == float('45.35')
    assert convert_string_to_float('$ 1000.35') == float('1000.35')
    assert convert_string_to_float('Por: R$ 10.999,00', 'pt_BR') == float('10999.00')
    assert convert_string_to_float('For: $ 10,999.00') == float('10999.00')
    assert convert_string_to_float('Yen: 10,900', 'ja_JP') == float('10900')
    assert convert_string_to_float('$ 45.35 - $ 75.46') == float('45.35')
    with pytest.raises(ValueError):
        convert_string_to_float('abc')
    with pytest.raises(SystemExit):
        convert_string_to_float('...,,,')

def test_is_reduced():
    with pytest.raises(ValueError):
        is_price_reduced(1200, 1200)
    with pytest.raises(ValueError):
        is_price_reduced(1300, 1200)
    assert is_price_reduced(1199, 1200)
