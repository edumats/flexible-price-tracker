import argparse
import locale
import re
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import selenium.webdriver.chrome.options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import plyer
import schedule

# Configuration for parser
parser = argparse.ArgumentParser(
    description='Check prices on e-commerce websites'
)
parser.add_argument(
    'url',
    type=str,
    help='URL to be scrapped'
)
parser.add_argument(
    'xpath',
    type=str,
    help="X-Path of the element that contains the product's price"
)
parser.add_argument(
    'target_price',
    type=str,
    help='Target price to activate a notification'
)
parser.add_argument(
    'locale',
    type=str,
    help='Specify a locale for correctly formatting price'
)
parser.add_argument(
    '-t',
    '--time',
    type=str,
    help='Time between each price check'
)


def main():
    # Create Chrome driver instance
    driver = create_scrapper()

    # Get string for actual price and page's title
    actual_price_string, page_title = scrap_page(args.url, args.xpath, driver)

    # Sets the locale
    locale.setlocale(locale.LC_ALL, args.locale)

    # Convert prices from string to float, considering locale
    target_price = convert_string_to_float(args.target_price)
    actual_price_float = convert_string_to_float(actual_price_string)

    # Creates a message comparing actual price and target price
    title, message = create_message(
        actual_price_float,
        target_price,
        page_title
    )

    print(message)

    # Send message to user's desktop notifications
    plyer.notification.notify(
        title=title,
        message=message
    )


def extract_time(time_str: str) -> tuple[str, int]:
    """ Given a letter and number string, validate and return it as tuple """

    if time_str[0] in {'m', 'h', 'd'} and time_str[1:].isdigit():
        return (time_str[0], int(time_str[1:]))
    else:
        raise ValueError(
            'Time value does not start with s, m, h or d, followed by digit'
        )


def scrap_page(url: str,
               xpath: str,
               driver: webdriver.Chrome) -> tuple[str, str]:
    """ Returns tuple of contents of xpath element and page's title """

    # Go to url
    driver.get(url)

    # Get page title
    page_title = driver.title

    try:
        # Get target element contents
        contents = driver.find_element(By.XPATH, xpath).text
    except NoSuchElementException:
        sys.exit("Error: Couldn't find an element using provided X-Path")

    # Exit browser
    driver.close()

    return (contents, page_title)


def create_message(
        current_price: float,
        target_price: float,
        item_name: str) -> tuple[str, str]:
    """ Returns a title and message according to price difference """

    symbol = locale.localeconv()['currency_symbol']
    target_value = locale.currency(target_price, symbol=False)
    current_price_value = locale.currency(current_price, symbol=False)

    if current_price <= target_price:
        """
        Monetary value and currency symbol are separated to avoid inconsistent
        currency symbol placement, such as 100 R$ (MacOS) or R$ 100 (Ubuntu)
        """

        return (
            f'Price down to {symbol}{current_price_value}',
            f'Low price alert of {item_name}'
        )
    else:
        return (
            'Price higher than target price',
            f'Current price of {symbol}{current_price_value} is higher '
            f'than target price of {symbol}{target_value}'
        )


def convert_string_to_float(str: str) -> float:
    """
    Given a price like string, convert to float considering provided locale
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

    # Converts string according to provided locale
    try:
        result_value = locale.atof(match.group(1))
    except ValueError:
        sys.exit('Invalid price format was used')

    return float(result_value)


def create_scrapper() -> webdriver.Chrome:
    """ Returns a Chrome webdriver object """

    # Set to eager to wait for DOM, but images may be still loading
    options = selenium.webdriver.chrome.options.Options()
    options.page_load_strategy = 'eager'

    # For avoiding the need for browser driver to be downloaded beforehand
    service = ChromeService(
        executable_path=ChromeDriverManager().install()
    )

    return webdriver.Chrome(service=service, options=options)


if __name__ == '__main__':
    # Get parser arguments
    args = parser.parse_args()

    # If time argument is present, schedule the job
    if args.time:
        # Validate and get time unit and interval from command argument
        time_unit, interval = extract_time(args.time)

        # Schedule according to time interval requested by user
        schedule_options = {
            'm': schedule.every(interval).minutes.do(main),
            'h': schedule.every(interval).hours.do(main),
            'd': schedule.every(interval).days.do(main)
        }

        # Run schedule function
        schedule_options[time_unit]

        while True:
            # Run pending schedules
            schedule.run_pending()
            time.sleep(1)
    else:
        # If no time argument in command arguments, just run once
        main()
