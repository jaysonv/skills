import logging
from functools import partial
from selenium.common.exceptions import NoSuchElementException
from utility import log_result


@log_result
def by_tag_a(selenium_driver):
    logger = logging.getLogger(name=by_tag_a.__name__)
    links = []
    try:
        elements = [element.get_attribute('href') for element in selenium_driver.find_elements_by_tag_name('a')]
        links.extend(filter(None, elements))
    except NoSuchElementException:
        logger.warning('NoSuchElementException finding job description links')
    return links


@log_result
def by_xpath(selenium_driver, title_selector):
    logger = logging.getLogger(name=by_tag_a.__name__)
    links = []
    for index in range(1001):
        formatted_selector = title_selector.format(index)
        try:
            elements = selenium_driver.find_elements_by_xpath(formatted_selector)
            links += [element.get_attribute('href') for element in elements]
        except NoSuchElementException as exc:
            logger.exception(msg='{exc}: {selector}'.format(exc=exc, selector=formatted_selector))
    return links


@log_result
def by_class():
    raise NotImplementedError("Job title selection by class not yet implemented")
    # try:
    #     links = []
    #     print('Finding link elements')
    #     elements = driver.find_elements_by_class_name(class_name)
    #     print('Extracting links')
    #     for element in elements:
    #         links += element.get_attribute('href')
    #     logging.info('Returning links: ' + [link + ', ' for link in links])
    #     return links
    # except NoSuchElementException:
    #     print('NoSuchElementException')


def get_link_func(selector_tag_type, selenium_driver, job_link_selector):
    if selector_tag_type == 'tag':
        return partial(by_tag_a, selenium_driver)
    elif selector_tag_type == 'xpath':
        return partial(by_xpath, selenium_driver, job_link_selector)
    elif selector_tag_type == 'class':
        raise NotImplementedError("Job title selection by class not yet implemented")