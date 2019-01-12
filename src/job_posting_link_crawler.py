import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import signal
from utility import get_link_finder_func, log_result


class JobPostingLinkCrawler(object):
    def __init__(self, **site_config):
        """
        :param site_config:
            * search_start_url: str
            * next_page_selector: str
            * next_page_selector_type: str
            * job_link_selector: str
            * job_link_selector_type: str
            * use_solitary_paging: bool
        """
        self.found_links = []
        self._selenium_driver = webdriver.Firefox(service_log_path='../logs/geckodriver.log')
        self._selenium_driver.set_window_position(-2000, -2000)
        self._selenium_driver.get(site_config['search_start_url'])
        self._current_page = 1
        self._use_solitary_paging = site_config['use_solitary_paging']

        self._get_job_links_on_page = get_link_finder_func(
            site_config['job_link_selector_type'], self._selenium_driver,
            site_config['job_link_selector'])
        self._get_next_page_link = get_link_finder_func(
            site_config['next_page_selector_type'], self._selenium_driver,
            site_config['next_page_selector'], single_link=True)

    def __enter__(self):
        signal.signal(signal.SIGTERM, self._cleanup)
        signal.signal(signal.SIGINT, self._cleanup)
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._cleanup()

    @log_result
    def start(self):
        """
        Walk through all pages of a site and collect all job posting links.
        """
        logger = logging.getLogger(__class__.__name__)
        while True:
            print('Looking on page {}...'.format(self._current_page))
            logger.info('Looking on page {}...'.format(self._current_page))
            if self._use_solitary_paging:
                self.found_links.extend(self._get_job_links_on_page())
            if not self._go_to_next_page():
                break
        if not self._use_solitary_paging:
            self.found_links.extend(self._get_job_links_on_page())
        return self.found_links

    def _cleanup(self, *args):
        self._selenium_driver.quit()

    def _go_to_next_page(self):
        try:
            self._selenium_driver.get(self._get_next_page_link(formatters=[self._current_page+1]))
        except NoSuchElementException as exc:
            logging.exception(msg='{}, likely reached end of pages.'.format(exc))
            return False
        self._current_page += 1
        return True
