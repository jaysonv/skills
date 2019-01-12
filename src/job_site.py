from get_job_links import get_link_func
from job_description import JobDescription
import logging
from selenium.common.exceptions import NoSuchElementException
from utility import log_result


JOB_DESCRIPTION_IDENTIFIER = 'clk?jk'
# TODO, use pathlib
JOB_OUTPUT_FILENAME = '../job_output.txt'


class JobSite(object):
    def __init__(self, selenium_driver, url, next_page_selector, job_link_selector_type, job_link_selector,
                 job_posting_title_selector):
        self.selenium_driver = selenium_driver
        self.url = url
        self.discarded_job_descriptions = set()
        self.job_postings = []
        self.next_page_selector = next_page_selector
        self.job_posting_title_selector = job_posting_title_selector
        self.get_job_links = get_link_func(
            job_link_selector_type, selenium_driver, job_link_selector)
        self.current_page = 1

    def go_to_start_page(self):
        self.selenium_driver.get(self.url)
        self.current_page = 1

    def go_to_next_page(self):
        try:
            page_element = self.selenium_driver.find_element_by_xpath(self.next_page_selector.format(self.current_page + 1))
            self.selenium_driver.get(page_element.get_attribute('href'))
        except NoSuchElementException as exc:
            logging.exception(msg='{}, likely reached end of pages.'.format(exc))
            return False
        self.current_page += 1
        return True

    def discard_unmatched_job_descriptions(self):
        for job in self.job_postings:
            if job is None or job.hasNoMatches():
                logging.info('Adding {title} to discard list'.format(title=job))
                self.discarded_job_descriptions.add(job)
        self.job_postings = list(set(self.job_postings) ^ self.discarded_job_descriptions)

    @log_result
    def filter_links_by_identifier(self, links):
        return [link for link in links if JOB_DESCRIPTION_IDENTIFIER in link]

    def output_results(self):
        with open(JOB_OUTPUT_FILENAME, 'w') as file:
            file.write('DISCARDED JOB DESCRIPTIONS (TOTAL {})\n'.format(len(self.discarded_job_descriptions)))
            for job in self.discarded_job_descriptions:
                file.write('{}\n'.format(job))

            print('-----------------------------')
            print('MATCHING JOB TITLES (TOTAL {})'.format(len(self.job_postings)))
            for job in self.job_postings:
                print(job)
                print('Keyword matches: {}'.format(job.keyword_matches))
                print('===============================')

            logging.info('Writing results to: {output_filename}'.format(output_filename=JOB_OUTPUT_FILENAME))

    def process_site(self):
        self.go_to_start_page()

        while True:
            print('Looking on page {}...'.format(self.current_page))
            logging.info('Looking on page {}...'.format(self.current_page))

            links = self.filter_links_by_identifier(self.get_job_links())
            for link in links:
                self.job_postings.append(
                    JobDescription.from_url(link, self.selenium_driver, self.job_posting_title_selector))
            if not self.go_to_next_page():
                break

        self.discard_unmatched_job_descriptions()
        self.output_results()