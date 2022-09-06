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
    '-l',
    '--locale',
    type=str,
    default='en_US.UTF-8',
    help='Specify a locale for correctly formatting price'
)
parser.add_argument(
    '-t',
    '--time',
    type=str,
    help='Time between each price check'
)


def main():
    # Convert price from string to float formatted according to locale setting
    target_as_float = convert_string_to_float(args.target_price, args.locale)
    # If time argument is present, schedule the job
    if args.time:
        time_unit, interval = extract_time(args.time)

        # Schedule according to time interval requested by user
        # Incomplete
        schedule_options = {
            'm': schedule.every(interval).minutes.do(scrap_page, url=args.url),
            'h': schedule.every(interval).hours.do(scrap_page),
            'd': schedule.every(interval).days.do(scrap_page)
        }

        # Run schedule function
        schedule_options[time_unit]()

        while True:
            # Run pending schedules
            schedule.run_pending()
            time.sleep(1)
    else:
        # If no time argument, just run once
        scrap_page(args.url, args.xpath, args.locale, target_as_float)


def extract_time(time_str: str) -> tuple[str, str]:
    """ Given a letter and number string, validate and return as tuple """

    if time_str[0] in {'m', 'h', 'd'} and time_str[1].isdigit():
        return (time_str[0], time_str[1])
    else:
        raise ValueError(
            'Time value does not start with s, m, h or d, followed by digit'
        )


def scrap_page(url, xpath, locale_setting, target_price):
    """ Gets contents of xpath element """

    driver = create_scrapper(url)

    # Go to url
    driver.get(url)
    page_title = driver.title

    try:
        price = driver.find_element(By.XPATH, xpath).text
    except NoSuchElementException:
        sys.exit("Error: Couldn't find an element using provided X-Path")

    # Convert extracted price to a float
    actual_price = convert_string_to_float(price, locale_setting)

    message = create_message(actual_price, target_price, page_title)

    print(message)

    plyer.notification.notify(
        message
    )


def create_message(
        current_price: float,
        target_price: float,
        item_name: str) -> str:
    """ Returns a message related to changes in price """

    if current_price <= target_price:
        return (
            f'The price of {item_name} '
            f'has gone down to {locale.currency(current_price)}'
        )
    else:
        return (
            f'Current price of {locale.currency(current_price)} is higher '
            f'than target price of {locale.currency(target_price)}'
        )


def convert_string_to_float(
        str: str,
        locale_setting: str) -> float:
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

    # Sets the locale
    locale.setlocale(locale.LC_ALL, locale_setting)

    # Converts string according to provided locale or by the default en_US
    try:
        result_value = locale.atof(match.group(1))
    except ValueError:
        sys.exit('Invalid price format was used')

    return float(result_value)


def create_scrapper(url: str) -> webdriver.Chrome:
    """ Returns a webdriver object """

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
    main()
