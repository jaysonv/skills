from collections import Counter
from keywords import KEY_WORDS
from job_posting import JobPosting
import logging
from selenium.common.exceptions import NoSuchElementException
from utility import log_result, get_element_finder_func


class JobPostingParser(object):
    def __init__(self, selenium_driver, job_posting_links, site_config):
        """
        :param site_config: dict
            * job_posting_title_selector: str
            * job_posting_title_selector_type: str
            * job_posting_description_selector: str
            * job_posting_description_selector_type: str
        """
        self.discarded_job_descriptions = set()
        self.job_postings = []

        self._selenium_driver = selenium_driver
        self._job_posting_links = job_posting_links

        self._get_job_posting_title_element = get_element_finder_func(
            selenium_driver, site_config['job_posting_title_selector'],
            site_config['job_posting_title_selector_type'])
        self._get_job_posting_description_element = get_element_finder_func(
            selenium_driver, site_config['job_posting_description_selector'],
            site_config['job_posting_description_selector_type'])

    def start(self):
        for link in self._job_posting_links:
            self.job_postings.append(self._create_job_posting_from_url(link))
        self._discard_unmatched_job_descriptions()
        return self.job_postings

    def _discard_unmatched_job_descriptions(self):
        for job in self.job_postings:
            if job is None or job.hasNoMatches():
                logging.info('Adding {title} to discard list'.format(title=job))
                self.discarded_job_descriptions.add(job)
        self.job_postings = list(set(self.job_postings) ^ self.discarded_job_descriptions)

    @log_result
    def _create_job_posting_from_url(self, url):
        try:
            log = logging.getLogger(__class__.__name__)
            log.info('Getting job post at: {url}'.format(url=url))
            self._selenium_driver.get(url)

            title = self._get_job_posting_title_element().text
            log.info('Title is: {title}'.format(title=title))

            description = self._get_job_posting_description_element().text

            word_counts = Counter(description.split())
            matching_keywords = {word: count for word, count in word_counts.items() if word.lower() in KEY_WORDS}
            logging.info('Matching keywords are: {}'.format(matching_keywords))
            return JobPosting(url, title, description, matching_keywords)
        except NoSuchElementException as exc:
            logging.exception(msg=exc)
        return None
