import logging
from selenium.common.exceptions import NoSuchElementException


def by_tag_a(selenium_driver, logging_context=logging.getLogger('GetLinkLogger')):
    logging_context.info('Getting links by tag')
    links = []
    try:
        logging_context.info('Finding link elements')
        print('Finding link elements')
        elements = selenium_driver.find_elements_by_tag_name('a')
        print('Extracting links')
        links += ([element.get_attribute('href') for element in elements if element.get_attribute('href') != None])
        logging_context.debug('Links found : ' + str(links))
        return links
    except NoSuchElementException:
        logging_context.warning('NoSuchElementException finding job description links')
        print('NoSuchElementException')


def by_xpath(selenium_driver, selector, logging_context=logging.getLogger('GetLinkLogger')):
    logging_context.info('Getting links by xpath')
    links = []
    for index in range(1001):
        try:
            elements = selenium_driver.find_elements_by_xpath(selector.format(index))
            logging_context.info('Found elements by xpath: ' + selector.format(str(index)))
            links += [element.get_attribute('href') for element in elements]
        except NoSuchElementException:
            logging_context.warning(
                'NoSuchElementException getting element by xpath: ' + selector.format(str(index)))
    if links:
        logging_context.info('Returning links: ' + str(links))
    else:
        logging_context.info('No links found')
    return links


def by_class():
    return []
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