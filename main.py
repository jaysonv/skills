from collections import defaultdict, Counter
import get_job_links
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from datetime import datetime
import logging

JOB_OUTPUT_FILENAME = 'job_output.txt'

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

JOB_DESCRIPTION_IDENTIFIER = 'clk?jk'

INDEED_JOB_DESCRIPTION_TITLE_SELECTOR = '//div[@class="jobsearch-DesktopStickyContainer"]/h3[1]'
INDEED_URL = 'https://www.indeed.com/jobs?q=software+quality&l=95032'
INDEED_PAGING_SELECTOR = '//span[.={}]/..'
INDEED_JOB_LINK_SELECTOR_TYPE = 'tag'
INDEED_JOB_LINK_SELECTOR = None


CAREER_BUILDER_URL = 'https://www.careerbuilder.com/jobs-software-quality-assurance-engineer-in-95032?keywords=software+quality+assurance+engineer&location=95032&radius=50&emp=jtft%2Cjtfp&pay=120&sort=distance_asc'
CAREER_BUILDER_JOB_DESCRIPTION_TITLE_SELECTOR = '//*[@id="main-content"]/div[10]/div[3]/div[1]/div/div[1]/h1'
CAREER_BUILDER_PAGING_SELECTOR = '//*[@id="main-content"]/div[7]/div[2]/div[1]/div[2]/div/div/a[{}]'
CAREER_BUILDER_JOB_LINK_SELECTOR_TYPE = 'xpath'
CAREER_BUILDER_JOB_LINK_SELECTOR = '/html/body/div[3]/div[7]/div[2]/div[1]/div[1]/div[2]/div[{}]/div[2]/div[1]/h2[2]/a'

driver = webdriver.Firefox()
driver.set_window_position(-2000, -2000)

def make_date_string():
    stamp = datetime.now()
    date_string = stamp.strftime('%Y-%d-%m-%H-%M-%S')
    return date_string

logging.basicConfig(filename='execution_{date}.log'.format(date=make_date_string()), level=logging.INFO)

'''
SITE_DICT = {


    'dice':
        {
            'url': 'https://www.dice.com/jobs/advancedResult.html?for_one=&for_all={title}&for_exact=&for_none=&for_jt=&for_com=&for_loc=Santa+Clara%2C+CA&jtype=Full+Time&sort=relevance&limit=100&radius=50&jtype=Full+Time&limit=100&radius=50&jtype=Full+Time',
            'format_string': None,
            'job_link_element_selector_type': None,

            'job_element_selector': None,
            'next_page_selector': '/html/body/div[8]/div[3]/div[2]/div[1]/div[6]/div[2]/div/ul/li[{}]/a',
            'paging_type': 'page',
            },
    'monster':
        {
            'url': 'https://www.monster.com/jobs/search/Full-Time_8?q=software-quality-assurance&intcid=skr_navigation_nhpso_searchMain&rad=50&where=Los-Gatos__2c-CA&tm=30',
            'format_string': None,
            'job_link_element_selector_type': None,  # NEED TO BE "PAGED    "
            'job_element_selector': None,
            'next_page_selector': '//*[@id="loadMoreJobs"]',
            'paging_type': 'button',

        },
    'glass_door':
        {
            'url': 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=Software%20Quality%20Assurance%20Engineer&locT=C&locId=1147436&locKeyword=San%20Jose,%20CA&jobType=fulltime&fromAge=30&minSalary=170000&includeNoSalaryJobs=false&radius=25&cityId=-1&minRating=4.00&industryId=-1&companyId=-1&applicationType=0&employerSizes=0&remoteWorkType=0',
            'format_string': None,
            'job_link_element_selector_type': None,
            'job_element_selector': None,
            'next_page_selector': '/html/body/div[3]/div/div/div/div[1]/div/div[2]/section/article/div/div[3]/div[2]/div/div/ul/li[{}]/a',
            'paging_type': 'page',
            },
    'linked_in':
        {
            'url': 'https://www.linkedin.com/jobs/search/?distance=50&f_E=3%2C4&f_JT=F&f_SB2=5&f_TP=1%2C2%2C3%2C4&keywords=software%20quality%20assurance%20engineer&location=Santa%20Clara%2C%20California&locationId=PLACES.us.7-1-0-43-18',
            'format_string': None,
            'job_link_element_selector_type': None,
            'job_element_selector': None,
            'next_page_selector': '//*[@id="ember975"]/li/ol/li[{}]/button',
            'paging_type': 'page',  # yes, page!
            },
'''

class JobDescription(object):

    def __init__(self, url, title, description=None, keyword_matches=None):
        self.url = url
        self.title = title
        self.description = description
        self._keyword_matches = keyword_matches

    def __str__(self):
        return self.title

    def hasNoMatches(self):
        return not self._keyword_matches

    @property
    def keyword_matches(self):
        return ', '.join('{k}: {v}'.format(k=word, v=count) for word, count in self._keyword_matches.items())

    @classmethod
    def from_url(cls, url, selenium_driver, title_selector):
        logging.info('Creating {cls} from url: {url}, driver: {driver}, title_selector:{title_selector}'.format(
            cls=cls.__name__, url=url, driver=selenium_driver, title_selector=title_selector))

        try:
            logging.info('Getting job post at: {url}'.format(url=url))
            driver.get(url)

            title = selenium_driver.find_element_by_xpath(title_selector).text
            logging.info('Title is: {title}'.format(title=title))

            description = selenium_driver.find_element_by_tag_name('body').text

            word_counts = Counter(description.split())
            matching_keywords = {word: count for word, count in word_counts.items() if word in KEY_WORDS}
            logging.info('Matching keywords are: {}'.format(matching_keywords))
            driver.back()
            return cls(url=url, title=title, keyword_matches=matching_keywords)
        except NoSuchElementException as exc:
            logging.exception(msg=exc)
        return None


class JobSite(object):

    def __init__(self, url, next_page_selector, job_link_selector_type, job_link_selector,
                 job_posting_title_selector):
        self.url = url
        self.discarded_job_descriptions = set()
        self.job_postings = []
        self.next_page_selector = next_page_selector
        self.job_posting_title_selector = job_posting_title_selector
        self.get_job_links = get_job_links.get_link_func(
            job_link_selector_type, driver, job_link_selector, logging_context=logging)
        self.current_page = 1

    def go_to_start_page(self):
        driver.get(self.url)
        self.current_page = 1

    def go_to_next_page(self):
        try:
            page_element = driver.find_element_by_xpath(self.next_page_selector.format(self.current_page + 1))
            driver.get(page_element.get_attribute('href'))
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

    def filter_links_by_identifier(self, links):
        logging.info('Filtering links for identifier: ' + JOB_DESCRIPTION_IDENTIFIER)
        clean_links = [link for link in links if JOB_DESCRIPTION_IDENTIFIER in link]
        logging.debug('Filtered links: ' + str(clean_links))
        return clean_links

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
                    JobDescription.from_url(link, driver, self.job_descriptions_title_selector))
            if not self.go_to_next_page():
                break

        self.discard_unmatched_job_descriptions()
        self.output_results()

def go():
    logging.info('PROCESSING INDEED')
    print('PROCESSING INDEED')
    indeed = JobSite(
                     url=INDEED_URL,
                     paging_element_selector=INDEED_PAGING_SELECTOR,
                     job_link_selector_type=INDEED_JOB_LINK_SELECTOR_TYPE,
                     job_link_selector=INDEED_JOB_LINK_SELECTOR,
                     job_posting_title_selector=INDEED_JOB_DESCRIPTION_TITLE_SELECTOR,
                     )
    indeed.process_site()

    logging.info('PROCESSING CAREER BUILDER')
    print('PROCESSING CAREER BUILDER')
    careerbuilder = JobSite(
                            url=CAREER_BUILDER_URL,
                            paging_element_selector=CAREER_BUILDER_PAGING_SELECTOR,
                            job_link_selector_type=CAREER_BUILDER_JOB_LINK_SELECTOR_TYPE,
                            job_link_selector=CAREER_BUILDER_JOB_LINK_SELECTOR,
                            job_posting_title_selector=CAREER_BUILDER_JOB_DESCRIPTION_TITLE_SELECTOR,
                            )
    careerbuilder.process_site()
    print('Finished')


if __name__ == '__main__':
    go()
    driver.close()

