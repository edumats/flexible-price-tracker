import argparse
import locale
import re
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
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

    print('[SCRAPPER]: ', title)
    print('[SCRAPPER]: ', message)

    # Send message to user's desktop notifications
    plyer.notification.notify(
        title=title,
        message=message
    )


def create_scrapper() -> webdriver.Chrome:
    """ Returns a Chrome webdriver object """

    # Set to eager to wait for DOM, but images may be still loading
    options = selenium.webdriver.chrome.options.Options()
    # Headless option disabled due to automation detection in some pages
    # options.headless = True
    user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit'
                  '/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36')
    # Avoids Chrome automation being detected
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Defines settings to avoid automation detection
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--lang=en-US,en')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # For avoiding the need for Chrome driver to be downloaded beforehand
    service = ChromeService(
        executable_path=ChromeDriverManager().install()
    )

    # Create and configure webdriver object
    driver = webdriver.Chrome(service=service, options=options)
    """
    As in: https://intoli.com/blog/making-chrome-headless-undetectable/
    WebGLRenderingContext should not return values that
    imply use of headless browser
    """
    driver.execute_script(
        (
         "const getParameter = WebGLRenderingContext.getParameter;"
         "WebGLRenderingContext.prototype.getParameter = function(param){"
         "if(param === 37445){return 'Intel Open Source Technology Center'}"
         "if(param === 37446){return 'Mesa DRI Intel(R) Ivybridge Mobile'"
         "}return getParameter(param);};"
        )
    )
    # navigator.plugins length set to 5 to escape automation detection
    driver.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {
            "source": ("Object.defineProperty(navigator,'plugins',"
                       "{get: () => [1, 2, 3, 4, 5]});")
        }
    )

    return driver


def scrap_page(url: str,
               xpath: str,
               driver: webdriver.Chrome) -> tuple[str, str]:
    """ Returns tuple of contents of xpath element and page's title """

    # Go to url
    driver.get(url)
    # Get page title
    page_title = driver.title

    try:
        # Wait for target element to load its contents and get when available
        wait_time = 3  # waits 3 seconds
        contents = WebDriverWait(driver, wait_time).until(
            element_has_text((By.XPATH, xpath))
        ).text
        # contents = driver.find_element(By.XPATH, xpath).text
    except NoSuchElementException:
        sys.exit("Error: Couldn't find an element using provided X-Path")
    except TimeoutException:
        sys.exit(
            'Error: Waited for target element text to appear,'
            ' but it remained empty'
        )

    # Raise error if element is empty
    if not contents:
        sys.exit(
            'Error: Found element with provided XPath,'
            ' but it does not contain a value'
        )

    # Exit browser
    driver.close()

    return (contents, page_title)


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


def extract_time(time_str: str) -> tuple[str, int]:
    """ Given a letter and number string, validate and return it as tuple """

    if time_str[0] in {'m', 'h', 'd'} and time_str[1:].isdigit():
        return (time_str[0], int(time_str[1:]))
    else:
        raise ValueError(
            'Time value does not start with s, m, h or d, followed by digit'
        )


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


class element_has_text(object):
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if element.text:
            return element
        else:
            return False


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
