from job_description import JobDescription
import logging
from selenium.common.exceptions import NoSuchElementException
from utility import log_result, get_link_finder_func


JOB_DESCRIPTION_IDENTIFIER = 'clk?jk'
# TODO, use pathlib
JOB_OUTPUT_FILENAME = '../job_output.txt'


class JobSite(object):
    def __init__(self, selenium_driver, url, next_page_selector, next_page_selector_type, job_link_selector_type, job_link_selector,
                 job_posting_title_selector):
        self.selenium_driver = selenium_driver
        self.url = url
        self.current_page = 1
        self.discarded_job_descriptions = set()
        self.job_postings = []

        self.next_page_selector = next_page_selector
        self.job_link_title_selector = job_posting_title_selector
        self.job_link_selector = job_link_selector

        self.get_job_links_on_page = get_link_finder_func(
            job_link_selector_type, selenium_driver, job_link_selector)
        self.get_next_page_link = get_link_finder_func(
            next_page_selector_type, selenium_driver, next_page_selector, single_link=True)

    def go_to_start_page(self):
        self.selenium_driver.get(self.url)
        self.current_page = 1

    def go_to_next_page(self):
        try:
            self.selenium_driver.get(self.get_next_page_link(formatters=[self.current_page+1]))
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

    @log_result
    def get_all_job_post_links(self, solitary_pages=False):
        """
        Walk through all pages of a site and collect all job posting links.
        :param solitary_pages: If True, results will be collected on a per-page basis.
        If False, all results will be collected at once. Use True if the website goes to
        a new page when you click on "more results" or a page number, False if the site has
        "expanding" results behaviour.
        :return: List of job posting hrefs.
        """
        logger = logging.getLogger(__class__.__name__)
        self.go_to_start_page()
        job_posting_links = []
        while True:
            print('Looking on page {}...'.format(self.current_page))
            logger.info('Looking on page {}...'.format(self.current_page))
            if solitary_pages:
                job_posting_links.extend(self.get_job_links_on_page())
            if not self.go_to_next_page():
                break
        if not solitary_pages:
            job_posting_links.extend(self.get_job_links_on_page())
        return job_posting_links

    def process_site(self):
        links = self.get_all_job_post_links(solitary_pages=True)
        for link in links:
            self.job_postings.append(
                JobDescription.from_url(link, self.selenium_driver, self.job_link_title_selector))
        self.discard_unmatched_job_descriptions()
        self.output_results()
