import argparse
import locale
import re
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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

args = parser.parse_args()


def main():
    # Get parser args
    # args = parser.parse_args()
    target_as_float = convert_string_to_float(args.target_price, args.locale)
    # If time argument is present, schedule the job
    if args.time:
        time_unit, interval = extract_time(args.time)

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
    ''' Gets contents of xpath element '''

    # Initialize Scrapper object and get page's title and price
    scrapper = Scrapper(url)
    page_title = scrapper.driver.title
    price = scrapper.find_element_text(xpath)

    # Convert extracted price to a float
    actual_price = convert_string_to_float(price, locale_setting)

    # Compare extracted price with target price
    if actual_price <= target_price:
        msg = (
            f'The price of the item {page_title} '
            f'has gone down to {locale.currency(actual_price)}'
        )
        plyer.notification.notify(
            title=f'Price reduced to {locale.currency(actual_price)}',
            message=msg,
        )
    else:
        print(f'Current price of {locale.currency(actual_price)} is higher '
              f'than target price of {locale.currency(target_price)}')


def send_notification():
    pass


def convert_string_to_float(
        str: str,
        locale_setting: str) -> float:
    """
    Given a price like string, convert to float

    Considers locale when converting price like string
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


# Contains methods related to scrapping
class Scrapper:
    def __init__(self, url: str) -> None:
        options = Options()
        # Set to eager to wait for DOM, but images may be still loading
        options.page_load_strategy = 'eager'

        # Does not require browser driver to be downloaded beforehand
        service = ChromeService(
            executable_path=ChromeDriverManager().install()
        )

        # Creates instance of Chrome webdriver
        self.driver = webdriver.Chrome(service=service, options=options)
        # Navigate to provided url
        self.driver.get(url)

    def find_element_text(self, xpath: str) -> str:
        """ Given a X-Path to a element, return inner text of the element """
        try:
            element_text = self.driver.find_element(By.XPATH, xpath).text
        except NoSuchElementException:
            sys.exit("Error: Couldn't find an element using provided X-Path")

        return element_text

    def close(self):
        """ Closes the webdriver """
        self.driver.close()


if __name__ == '__main__':
    main()
