from selenium.common.exceptions import NoSuchElementException
from utility import get_href_finder_func


class JobPostingLinkCrawler(object):
    def __init__(self, selenium_driver, site_config):
        """
        :param site_config: dict
            * search_start_url: str
            * next_page_selector: str
            * next_page_selector_type: str
            * job_link_selector: str
            * job_link_selector_type: str
            * use_solitary_paging: bool
        """
        self.found_links = []
        self._selenium_driver = selenium_driver
        self._selenium_driver.get(site_config['search_start_url'])
        self._current_page = 1
        self._use_solitary_paging = site_config['use_solitary_paging']

        self._get_job_links_on_page = get_href_finder_func(
            self._selenium_driver, site_config['job_link_selector'],
            site_config['job_link_selector_type'])
        self._get_next_page_link = get_href_finder_func(
            self._selenium_driver, site_config['next_page_selector'],
            site_config['next_page_selector_type'], single_link=True)

    def start(self):
        """
        Walk through all pages of a site and collect all job posting links.
        """
        while True:
            if self._use_solitary_paging:
                self.found_links.extend(self._get_job_links_on_page())
            if not self._go_to_next_page():
                break
        if not self._use_solitary_paging:
            self.found_links.extend(self._get_job_links_on_page())
        return self.found_links

    def _go_to_next_page(self):
        try:
            self._selenium_driver.get(self._get_next_page_link(formatters=[self._current_page+1]))
        except NoSuchElementException:
            return False
        self._current_page += 1
        return True
