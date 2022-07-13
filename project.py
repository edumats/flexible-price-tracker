import argparse
from email import message
import locale
import re
import sys
from unittest.mock import DEFAULT

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import plyer

# Configuration for parser
parser = argparse.ArgumentParser(
    description='Watch prices on e-commerce websites'
)
parser.add_argument(
    'url',
    type=str, help='URL to be scrapped'
)
parser.add_argument(
    'xpath',
    type=str,
    help="X-Path of the element that contains the product's price"
)
parser.add_argument(
    'target_price',
    type=float,
    help='Target price to activate a notification'
)
parser.add_argument(
    '-l',
    '--locale',
    type=str,
    default='en_US',
    help='Specify a locale for correctly formatting price'
)

DEFAULT_LOCALE = 'en_US.UTF-8'


class Scrapper:
    def __init__(self):
        options = Options()
        # Set to eager to wait for DOM, but images may be still loading
        options.page_load_strategy = 'eager'

        # Does not require browser driver to be downloaded beforehand
        service = ChromeService(
            executable_path=ChromeDriverManager().install()
        )

        # Creates instance of Chrome webdriver
        self.driver = webdriver.Chrome(service=service, options=options)

    def get_url(self, url: str) -> None:
        """ Navigate to provided url """
        self.driver.get(url)

    def find_element_text(self, xpath: str) -> str:
        """ Given a X-Path to a element, return inner text of the element """
        try:
            element_text = self.driver.find_element(By.XPATH, xpath).text
        except NoSuchElementException:
            sys.exit("Error: Couldn't find element by provided X-Path")

        return element_text

    def close(self):
        """ Closes the webdriver """
        self.driver.close()


def main():
    args = parser.parse_args()
    page_title, actual_price = scrap_element(args.url, args.xpath)
    print(actual_price)
    if is_price_reduced(args.target_price, actual_price):
        print('Price lower than target price')
        msg = (
            f'The price of the item {page_title} '
            f'has gone down to {actual_price}'
        )
        plyer.notification.notify(
            title='A price has been reduced',
            message=msg,
        )
    else:
        print('Price higher than target price')


def convert_string_to_float(str: str, locale_setting: str = DEFAULT_LOCALE) -> float:
    """
    Given a price like string, convert to float


    Considers locale when converting price like string, defaults to en_US
    """

    # If all character are digits, just return as float
    if str.isdigit():
        return float(str)

    # Searches for digits, with or without dot and comma
    match = re.search(r'([\d,.]+)', str)
    # If not digits are found, raise exception
    if not match:
        raise ValueError(
            'Provided string has no digits to be converted to float'
        )

    # Sets the locale
    locale.setlocale(locale.LC_ALL, locale_setting)

    # Converts string according to provided locale or by the default en_US
    try:
        result_value = locale.atof(match.group(1))
    except ValueError:
        sys.exit('Invalid price format was used')

    return float(result_value)


def scrap_element(url: str, xpath: str) -> tuple[str, float]:
    """ Returns tuple (page's title, X-Path's target element's inner html) """

    # Initialize a Scrapper object
    scrapper = Scrapper()

    # Gets url
    scrapper.get_url(url)

    # Find element in url using X-Path
    price = scrapper.find_element_text(xpath)

    # Gets url's title
    title = scrapper.driver.title

    scrapper.close()

    return (title, convert_string_to_float(price))


def is_price_reduced(target_price: float, actual_price: float) -> bool:
    """Returns True if target price is less than target, False otherwise"""
    if actual_price < target_price:
        return True
    return False


if __name__ == '__main__':
    main()
