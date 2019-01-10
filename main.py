from collections import defaultdict, Counter
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

INDEED_JOB_DESCRIPTION_TITLE_SELECTOR = '/html/body/div[1]/div[3]/div[3]/div/div/div[1]/div[1]/div[1]/h3'
INDEED_URL = 'https://www.indeed.com/jobs?as_and=software+quality+assurance+engineer&as_any=&as_not=&as_ttl=&as_cmp=&jt=fulltime&st=&as_src=&salary=%24145%2C000%2B&radius=50&l=95032&fromage=60&limit=50&sort=&psf=advsrch'
INDEED_PAGING_SELECTOR = '//*[@id="resultsCol"]/div[28]/a[{}]'
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
            'paging_element_selector': '/html/body/div[8]/div[3]/div[2]/div[1]/div[6]/div[2]/div/ul/li[{}]/a',
            'paging_type': 'page',
            },
    'monster':
        {
            'url': 'https://www.monster.com/jobs/search/Full-Time_8?q=software-quality-assurance&intcid=skr_navigation_nhpso_searchMain&rad=50&where=Los-Gatos__2c-CA&tm=30',
            'format_string': None,
            'job_link_element_selector_type': None,  # NEED TO BE "PAGED    "
            'job_element_selector': None,
            'paging_element_selector': '//*[@id="loadMoreJobs"]',
            'paging_type': 'button',

        },
    'glass_door':
        {
            'url': 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=Software%20Quality%20Assurance%20Engineer&locT=C&locId=1147436&locKeyword=San%20Jose,%20CA&jobType=fulltime&fromAge=30&minSalary=170000&includeNoSalaryJobs=false&radius=25&cityId=-1&minRating=4.00&industryId=-1&companyId=-1&applicationType=0&employerSizes=0&remoteWorkType=0',
            'format_string': None,
            'job_link_element_selector_type': None,
            'job_element_selector': None,
            'paging_element_selector': '/html/body/div[3]/div/div/div/div[1]/div/div[2]/section/article/div/div[3]/div[2]/div/div/ul/li[{}]/a',
            'paging_type': 'page',
            },
    'linked_in':
        {
            'url': 'https://www.linkedin.com/jobs/search/?distance=50&f_E=3%2C4&f_JT=F&f_SB2=5&f_TP=1%2C2%2C3%2C4&keywords=software%20quality%20assurance%20engineer&location=Santa%20Clara%2C%20California&locationId=PLACES.us.7-1-0-43-18',
            'format_string': None,
            'job_link_element_selector_type': None,
            'job_element_selector': None,
            'paging_element_selector': '//*[@id="ember975"]/li/ol/li[{}]/button',
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
            logging.info('Description is: {description}'.format(description=description))

            word_counts = Counter(description.split())
            matching_keywords = {word: count for word, count in word_counts.items() if word in KEY_WORDS}
            logging.info('Matching keywords are: {}'.format(matching_keywords))
            return cls(url=url, title=title, keyword_matches=matching_keywords)
        except NoSuchElementException as exc:
            logging.exception(msg=exc)
        return None


class JobSite(object):

    def __init__(self,
                 url, paging_element_selector, job_link_selector_type, job_link_selector, job_descriptions_title_selector):
        self.url = url
        self.discarded_job_descriptions = set()
        self.job_descriptions = []
        self.paging_element_selector = paging_element_selector
        self.job_link_selector_type = job_link_selector_type
        self.job_descriptions_title_selector = job_descriptions_title_selector
        self.job_link_selector = job_link_selector

    def launch_main_page(self):
        driver.get(self.url)

    def page(self, index):
        logging.info('Paging index is ' + str(index))
        try:
            if index >= 1:
                driver.find_element_by_xpath(self.paging_element_selector.format(index)).click()
                logging.info('Page by clicking ' + self.paging_element_selector.format(index))
            else:
                driver.find_element_by_xpath(self.paging_element_selector).click()
                logging.info('Page by clicking ' + self.paging_element_selector)
            print('Paging / clicking "Load More.."')
        except NoSuchElementException:
            print('NoSuchElementException - which might be expected')
            logging.warning('NoSuchElementException - which might be expected')
        except ElementClickInterceptedException:
            logging.warning('ElementClickInterceptedException for index ' + str(index))

    def get_links_by_tag_a(self):
        try:
            links = []
            logging.info('Finding link elements')
            print('Finding link elements')
            elements = driver.find_elements_by_tag_name('a')
            print('Extracting links')
            links += ([element.get_attribute('href') for element in elements if element.get_attribute('href') != None ])
            logging.debug('Links found : ' + str(links))
            return links
        except NoSuchElementException:
            logging.warning('NoSuchElementException finding job description links')
            print('NoSuchElementException')

    def get_links_by_xpath(self):
        links = []
        for index in range(1001):
            try:
                elements = driver.find_elements_by_xpath(self.job_link_selector.format(index))
                logging.info('Found elements by xpath: ' + self.job_link_selector.format(str(index)))
                links += [element.get_attribute('href') for element in elements]
            except NoSuchElementException:
                logging.warning('NoSuchElementException getting element by xpath: ' + self.job_link_selector.format(str(index)))
        if links:
            logging.info('Returning links: ' + str(links))
        else:
            logging.info('No links found')
        return links

    def discard_unmatched_job_descriptions(self):
        for job in self.job_descriptions:
            if job is None or job.hasNoMatches():
                logging.info('Adding {title} to discard list'.format(title=job))
                self.discarded_job_descriptions.add(job)
        self.job_descriptions = list(set(self.job_descriptions) ^ self.discarded_job_descriptions)

    def clean(self, links):
        logging.info('Cleaning links')
        clean_links = [link for link in links if JOB_DESCRIPTION_IDENTIFIER in link]
        logging.debug('Clean links : ' + str(clean_links))
        self.job_descriptions += [JobDescription.from_url(link, driver, self.job_descriptions_title_selector) for link in clean_links]

    def output_results(self):
        with open(JOB_OUTPUT_FILENAME, 'w') as file:
            file.write('DISCARDED JOB DESCRIPTIONS (TOTAL {})\n'.format(len(self.discarded_job_descriptions)))
            for job in self.discarded_job_descriptions:
                file.write('{}\n'.format(job))

            print('-----------------------------')
            print('MATCHING JOB TITLES (TOTAL {})'.format(len(self.job_descriptions)))
            for job in self.job_descriptions:
                print(job)
                print('Keyword matches: {}'.format(job.keyword_matches))
                print('===============================')

            logging.info('Writing results to: {output_filename}'.format(output_filename=JOB_OUTPUT_FILENAME))

    def process_site(self):
        self.launch_main_page()

        #TODO, change back to 6
        for page_number in range(1):
            if page_number >= 1:
                self.page(page_number)
            # Get links by selector type
            if self.job_link_selector_type == 'tag':
                logging.info('Getting links by tag')
                self.clean(self.get_links_by_tag_a())
            elif self.job_link_selector_type == 'xpath':
                logging.info('Getting links by xpath')
                self.clean(self.get_links_by_xpath())
            elif self.job_link_selector_type == 'class':
                self.clean(self.get_links_by_class())
            else:
                logging.warning('Unknown paging selector type: {}'.format(self.job_link_selector_type))

            self.discard_unmatched_job_descriptions()

        self.output_results()

    def get_links_by_class(self):
        pass
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

def go():
    logging.info('PROCESSING INDEED')
    print('PROCESSING INDEED')
    indeed = JobSite(
                     url=INDEED_URL,
                     paging_element_selector=INDEED_PAGING_SELECTOR,
                     job_link_selector_type=INDEED_JOB_LINK_SELECTOR_TYPE,
                     job_link_selector=INDEED_JOB_LINK_SELECTOR,
                     job_descriptions_title_selector=INDEED_JOB_DESCRIPTION_TITLE_SELECTOR,
                     )
    indeed.process_site()

    logging.info('PROCESSING CAREER BUILDER')
    print('PROCESSING CAREER BUILDER')
    careerbuilder = JobSite(
                            url=CAREER_BUILDER_URL,
                            paging_element_selector=CAREER_BUILDER_PAGING_SELECTOR,
                            job_link_selector_type=CAREER_BUILDER_JOB_LINK_SELECTOR_TYPE,
                            job_link_selector=CAREER_BUILDER_JOB_LINK_SELECTOR,
                            job_descriptions_title_selector=CAREER_BUILDER_JOB_DESCRIPTION_TITLE_SELECTOR,
                            )
    careerbuilder.process_site()
    print('Finished')


if __name__ == '__main__':
    go()
    driver.close()

