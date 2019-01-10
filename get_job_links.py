import logging
from functools import partial
from selenium.common.exceptions import NoSuchElementException


def by_tag_a(selenium_driver, logging_context):
    logging_context.info('Getting links by tag...')
    links = []
    try:
        logging_context.info('Extracting links...')
        elements = [element.get_attribute('href') for element in selenium_driver.find_elements_by_tag_name('a')]
        links.extend(filter(None, elements))
    except NoSuchElementException:
        logging_context.warning('NoSuchElementException finding job description links')
    logging_context.debug('Links found : ' + str(links))
    return links


def by_xpath(selenium_driver, title_selector, logging_context):
    logging_context.info('Getting links by xpath...')
    links = []
    for index in range(1001):
        formatted_selector = title_selector.format(index)
        try:
            logging_context.info('Extracting links...')
            elements = selenium_driver.find_elements_by_xpath(formatted_selector)
            links += [element.get_attribute('href') for element in elements]
        except NoSuchElementException as exc:
            logging_context.exception(msg='{exc}: {selector}'.format(exc=exc, selector=formatted_selector))
    logging_context.debug('Links found : ' + str(links))
    return links


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


def get_link_func(selector_tag_type, selenium_driver,
                  *, job_title_selector, logging_context=logging.getLogger('GetLinkLogger')):
    if selector_tag_type == 'tag':
        return partial(by_tag_a, selenium_driver, logging_context)
    elif selector_tag_type == 'xpath':
        partial(by_xpath, selenium_driver, job_title_selector, logging_context)
    elif selector_tag_type == 'class':
        raise NotImplementedError("Job title selection by class not yet implemented")