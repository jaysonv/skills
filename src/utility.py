from datetime import datetime
from functools import wraps
import logging
import yaml


def log_result(func):
    """
    :return: A function that logs it's name and resulting return.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        result = func(*args, **kwargs)
        logger.info('Result with these arguments {}, {} is: {}'.format(args, kwargs, result))
        return result
    return wrapper


def get_element_from_selector(selenium_find_by_func, selector):
    @wraps(selenium_find_by_func)
    def wrapper(formatters=None):
        formatters = formatters or []
        return selenium_find_by_func(selector.format(*formatters))
    return wrapper


def get_href_from_selector(selenium_find_by_func, selector):
    @wraps(selenium_find_by_func)
    def wrapper(formatters=None):
        formatters = formatters or []
        element = selenium_find_by_func(selector.format(*formatters))
        return element.get_attribute('href')
    return wrapper


def get_hrefs_from_selector(selenium_find_by_func, selector):
    @log_result
    @wraps(selenium_find_by_func)
    def wrapper(formatters=None):
        formatters = formatters or []
        elements = selenium_find_by_func(selector.format(*formatters))
        return [element.get_attribute('href') for element in elements]
    return wrapper


def get_href_finder_func(selenium_driver, selector, selector_type, single_link=False):
    """
    Return a function that is bound to a selenium_driver to a selector and selector_type,
    and returns either a list of hrefs, or a single href.
    :param selenium_driver: The driver to bind to.
    :param selector: The selector to bind the function with(a css, xpath, etc selector).
    :param selector_type: The type of selector that is used (css, xpath, etc)
    :param single_link: If True, return a function that returns a single href.
    """
    if selector_type == 'xpath':
        if single_link:
            return get_href_from_selector(selenium_driver.find_element_by_xpath, selector)
        return get_hrefs_from_selector(selenium_driver.find_elements_by_xpath, selector)
    if selector_type == 'css':
        if single_link:
            return get_href_from_selector(selenium_driver.find_element_by_css_selector, selector)
        return get_hrefs_from_selector(selenium_driver.find_elements_by_css_selector, selector)


def get_element_finder_func(selenium_driver, selector, selector_type):
    """
    Return a function that is bound to a selenium_driver to a selector and selector_type,
    and returns a single element.
    :param selenium_driver: The driver to bind to.
    :param selector: The selector to bind the function with(a css, xpath, etc selector).
    :param selector_type: The type of selector that is used (css, xpath, etc)
    """
    if selector_type == 'xpath':
        return get_element_from_selector(selenium_driver.find_element_by_xpath, selector)
    if selector_type == 'css':
        return get_element_from_selector(selenium_driver.find_element_by_css_selector, selector)


@log_result
def load_all_site_configurations(path):
    configs = {}
    file_names = path.glob('*.yaml')
    for file_path in file_names:
        with open(file_path, 'r') as f:
            configs.update(yaml.load(f))
    return configs


def get_logger_date_string():
    stamp = datetime.now()
    date_string = stamp.strftime('%Y-%d-%m-%H-%M-%S')
    return date_string