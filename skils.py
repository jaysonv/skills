from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from selenium.webdriver.common.by import By
from datetime import datetime
import logging

def make_date_string():
    stamp = datetime.now()
    date_string = stamp.strftime('%Y-%d-%m-%H-%M-%S')
    return date_string

logging.basicConfig(filename='execution_{date}.log'.format(date = make_date_string()), level=logging.INFO)

SYNONYM_MATCH_THRESHOLD = 90

SYNONYMS = {'software': 30, 'quality': 80, 'assurance': 90, 'qa': 100, 'sqa': 100, 'sdet': 100, 'test': 70, 'automation': 70, 'engineer': 20}

KEY_WORDS = ['bash', 'python', 'java', 'c++', 'ruby', 'perl', 'matlab', 'javascript', 'scala', 'firmware'
            'php', 'sauce', 'flask', 'shell', 'nas', 'san', 'iscsi', 'scripts', 'scripting',
            'junit', 'selenium', 'react', 'c#', 'testrail', 'confluence', 'jmeter', 'wifi',
            'tableau', 'd3.js', 'sas', 'spss', 'd3', 'wireless', 'saas', 'pandas', 'numpy', 'jenkins', 'scipy', 'plan', 'case',
            'sps', 'spotfire', 'scikits.learn', 'splunk', 'h2o', 'jira', 'functional', 'integration', 'stress', 'load', 'performance',
            'hadoop', 'mapreduce', 'spark', 'pig', 'hive', 'shark', 'oozie', 'zookeeper', 'flume', 'mahout',
            'elasticsearch', 'api', 'Mockito', 'Robotium', 'frontend', 'backend', 'cloud', 'tdd', 'driven', 'bdd',
            'sql', 'nosql', 'hbase', 'cassandra', 'xml', 'rust', 'mongodb', 'mysql', 'mssql', 'postgre', 'oracle',
            'rdbms', 'mobile', 'android', 'ios', 'cucumber', 'iot', 'black', 'white', 'telecommunications',
            'hive', 'cucumber', 'aws', 'azure', 'amazon', 'google', 'rest', 'docker', 'container', 'puppet', 'chef',
            'kubernetes', 'storage', 'network', 'networking', 'maven', 'ci', 'cd', 'ci/cd', 'gui', 'virtual', 'vmware',
            'restassured', 'ios', 'json', 'swift', 'objective-c', 'groovy', '.net', 'angular', 'node.js', 'kafka', 'mesos',
            'django', 'pytest', 'css', 'html', 'appium', 'linux', 'css', 'ui', 'soa', 'unix', 'RESTful', 'Elastic', 'git', 'github',
            'database', 'acceptance', 'uat', 'healthcare', 'banking',]

STRIP_WORDS = KEY_WORDS + ['senior', 'director', 'enterprise', 'architect', 'manager', 'lead','&', 'mobile', 'sr', 'jr', 'I', 'II', 'III', 'IV', '(', ')', '.', ',', '/', '\\', "\'", '\"', '-', 'analytics',]
for i in range(0,9):
    STRIP_WORDS.append('{}'.format(i))

summary_dict = {}
for key in KEY_WORDS:
    summary_dict[key] = 0

driver = webdriver.Firefox()
#driver.set_window_position(-2000, -2000)

LINKEDIN_URL = 'https://www.linkedin.com/jobs/search?keywords=Software+Quality+Assurance+Engineer&distance=25&locationId=PLACES%2Eus%2E7-1-0-43-18&f_TP=1%2C2%2C3%2C4&f_JT=FULL_TIME&orig=FCTD&trk=jobs_jserp_facet_job_type'
LINKEDIN_JOB_DESCRIPTION_TITLE_SELECTOR = '/html/body/div/main/div[2]/div/div/div/section[5]/section[1]/div/div[1]/div[2]/div[1]/div[1]/h1'
LINKEDIN_PAGING_SELECTOR = '/html/body/div[5]/div[5]/div[2]/section[1]/div[3]/div/div/div[1]/div[2]/div/section/ol/li/ol/li[{}]/button'
LINKEDIN_JOB_LINK_SELECTOR = "//*[starts-with[(@id, 'ember')]"
LINKEDIN_SITE_ID= 'linkedin'

class JobSite(object):

    def __init__(self, url, site_id, paging_element_selector, job_link_selector):
        self.url = url
        self.site_id = site_id
        self.paging_element_selector = paging_element_selector
        self.job_link_selector = job_link_selector
        self.discarded_job_descriptions = set()
        self.job_descriptions = []

    def _open_main(self):
        driver.get(self.url)
        logging.info('Opening: "{}""'.format(self.url))

    def _page(self):
        try:
            if self.site_id == 'linkedin':
                for index in range(1,6):
                    driver.find_element_by_xpath(self.paging_element_selector.format(index)).click()
                    logging.info('{} - Paging index: {}, selector "{}"'.format(self.site_id.upper(), index, self.paging_element_selector))
        except NoSuchElementException:
            logging.info('{} - NoSuchElementException: May be expected with paging\n
                         Paging index: {}, selector "{}"'.format(self.site_id.upper(), index, self.paging_element_selector))
        except ElementClickInterceptedException:
            logging.warning('{} - ElementClickInterceptedException selector: {}'.format(self.site_id.upper(), self.paging_element_selector.format(index))

    def _get_job_description_links(self):
        links = []
        if self.site_id == 'linkedin':
            try:
                elements = driver.find_elements_by_xpath(self.job_link_selector)
                logging.debug('Found elements by xpath = ' + self.job_link_selector)
                links += [element.get_attribute('href') for element in elements]
            except NoSuchElementException:
                logging.warning('{} - NoSuchElementException: selector: "{}"'.format(self.site_id.upper(),self.job_link_selector))
