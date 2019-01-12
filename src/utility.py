from functools import wraps
import logging
from datetime import datetime


def log_result(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__name__)
        result = func(*args, **kwargs)
        logger.info('Result is: {}'.format(result))
        return result
    return wrapper


def get_element_from_selector(selenium_get_func, selector):
    @log_result
    @wraps(selenium_get_func)
    def wrapper(formatters=None):
        formatters = formatters or []
        return selenium_get_func(selector.format(*formatters))
    return wrapper


def get_href_from_selector(selenium_get_func, selector):
    @log_result
    @wraps(selenium_get_func)
    def wrapper(formatters=None):
        formatters = formatters or []
        element = selenium_get_func(selector.format(*formatters))
        return element.get_attribute('href')
    return wrapper


def get_hrefs_from_selector(selenium_get_func, selector):
    @log_result
    @wraps(selenium_get_func)
    def wrapper(formatters=None):
        formatters = formatters or []
        elements = selenium_get_func(selector.format(*formatters))
        return [element.get_attribute('href') for element in elements]
    return wrapper


def get_link_finder_func(selector_tag_type, selenium_driver, selector, single_link=False):
    if selector_tag_type == 'tag':
        if single_link:
            return get_href_from_selector(selenium_driver.find_element_by_tag_name, selector)
        return get_hrefs_from_selector(selenium_driver.find_elements_by_tag_name, selector)
    elif selector_tag_type == 'xpath':
        if single_link:
            return get_href_from_selector(selenium_driver.find_element_by_xpath, selector)
        return get_hrefs_from_selector(selenium_driver.find_elements_by_xpath, selector)
    elif selector_tag_type == 'css':
        if single_link:
            return get_href_from_selector(selenium_driver.find_element_by_css_selector, selector)
        return get_hrefs_from_selector(selenium_driver.find_elements_by_css_selector, selector)


def get_element_finder_func(selector_tag_type, selenium_driver, selector):
    if selector_tag_type == 'tag':
        return get_element_from_selector(selenium_driver.find_element_by_tag, selector)
    if selector_tag_type == 'xpath':
        return get_element_from_selector(selenium_driver.find_element_by_xpath, selector)
    if selector_tag_type == 'css':
        return get_element_from_selector(selenium_driver.find_elements_by_css_selector, selector)


def make_date_string():
    stamp = datetime.now()
    date_string = stamp.strftime('%Y-%d-%m-%H-%M-%S')
    return date_string