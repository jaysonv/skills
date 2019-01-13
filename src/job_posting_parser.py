from collections import Counter
from job_posting import JobPosting
import logging
from selenium.common.exceptions import NoSuchElementException
from utility import log_result, get_element_finder_func

JOB_TITLES = ('Senior Quality Assurance Engineer', 'Senior QA Engineer II', 'Quality Assurance Manager',
              'Quality Assurance Engineer IV', 'Senior Quality Assurance Engineer', 'Sr. Director, Quality Assurance',
              'Lead Quality Engineer', 'software quality assurance', 'sqa', 'qa engineer', 'sdet',
              'software development engineer in test', 'software test engineer', 'software test automation',
              'qa automation', 'software quality assurance engineer', 'QA Automation Engineer')

PROGRAM_LANGUAGES = ('bash', 'python', 'java', 'c++', 'ruby', 'perl', 'matlab', 'javascript', 'scala',
                     'php', 'junit', 'selenium', 'react', 'c#', 'TestRail', 'Confluence')

ANALYSIS_SOFTWARE = ('tableau', 'd3.js', 'sas', 'spss', 'd3', 'saas', 'pandas', 'numpy', 'Jenkins', 'scipy',
                     'sps', 'spotfire', 'scikits.learn', 'splunk', 'h2o', 'jira')

BIGDATA_TOOL = ('hadoop', 'mapreduce', 'spark', 'pig', 'hive', 'shark', 'oozie', 'zookeeper', 'flume', 'mahout',
                'elasticsearch')

DATABASE_LANGUAGES = ('sql', 'nosql', 'hbase', 'cassandra', 'xml', 'rust', 'mongodb', 'mysql', 'mssql', 'postgre',
                      'oracle db', 'rdbms', 'hive', 'cucumber', 'aws', 'azure', 'amazon', 'google', 'rest', 'docker',
                      'container', 'puppet', 'chef', 'kubernetes', 'storage', 'network', 'networking')

OTHER_KEYWORDS = ('restassured', 'ios', 'json', 'swift', 'objective-c', 'groovy', '.net', 'angular', 'node.js', 'kafka',
                  'mesos', 'django', 'pytest', 'css', 'html', 'appium')

KEY_WORDS = frozenset(PROGRAM_LANGUAGES + ANALYSIS_SOFTWARE + BIGDATA_TOOL + DATABASE_LANGUAGES + OTHER_KEYWORDS)


class JobPostingParser(object):
    def __init__(self, selenium_driver, job_posting_links, site_config):
        """
        :param site_configuration:
            * job_posting_title_selector: str
            * job_posting_title_selector_type: str
            * job_posting_description_selector: str
            * job_posting_description_selector_type: str
        """
        self.discarded_job_descriptions = set()
        self.job_postings = []

        self._selenium_driver = selenium_driver
        self._job_posting_links = job_posting_links
        self._job_output_path = job_output_path

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
        self.output_results()
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
            matching_keywords = {word: count for word, count in word_counts.items() if word in KEY_WORDS}
            logging.info('Matching keywords are: {}'.format(matching_keywords))
            return JobPosting(url, title, description, matching_keywords)
        except NoSuchElementException as exc:
            logging.exception(msg=exc)
        return None