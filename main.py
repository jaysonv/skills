from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from selenium.webdriver.common.by import By
from datetime import datetime
import pdb
import pandas as pd
import pprint as pretty_print

JOB_TITLES = ['Senior Quality Assurance Engineer', 'Senior QA Engineer II', 'Quality Assurance Manager',
              'Quality Assurance Engineer IV', 'Senior Quality Assurance Engineer', 'Sr. Director, Quality Assurance',
              'Lead Quality Engineer', 'software quality assurance', 'sqa', 'qa engineer', 'sdet',
              'software development engineer in test',
              'software test engineer', 'software test automation', 'qa automation',
              'software quality assurance engineer']

program_languages = ['job_title', 'bash', 'python', 'java', 'c++', 'ruby', 'perl', 'matlab', 'javascript', 'scala',
                     'php',
                     'junit', 'selenium', 'React', 'c#']
analysis_software = ['tableau', 'd3.js', 'sas', 'spss', 'd3', 'saas', 'pandas', 'numpy', 'Jenkins', 'scipy',
                     'sps', 'spotfire', 'scikits.learn', 'splunk', 'h2o', 'jira']
bigdata_tool = ['hadoop', 'mapreduce', 'spark', 'pig', 'hive', 'shark', 'oozie', 'zookeeper', 'flume', 'mahout',
                'elasticsearch']
databases = ['sql', 'nosql', 'hbase', 'cassandra', 'xml', 'rust', 'mongodb', 'mysql', 'mssql', 'postgre', 'oracle db',
             'rdbms',
             'hive', 'cucumber', 'aws', 'azure', 'amazon', 'google', 'rest', 'docker', 'container', 'puppet', 'chef',
             'kubernetes', 'storage', 'network', 'networking']
other = ['restassured', 'ios', 'json', 'swift', 'objective-c', 'groovy', '.net', 'angular', 'node.js', 'kafka', 'mesos',
         'django', 'pytest', 'css', 'html', 'appium', 'testng']

KEY_WORDS = program_languages + analysis_software + bigdata_tool + databases + other

driver = webdriver.Firefox()
driver.set_window_position(-2000, -2000)

job_data = pd.DataFrame(columns=KEY_WORDS)

SITE_DICT = {
    'indeed':
        {
            'url': 'https://www.indeed.com/jobs?as_and=software+quality+assurance+engineer&as_any=&as_not=&as_ttl=&as_cmp=&jt=fulltime&st=&as_src=&salary=%24145%2C000%2B&radius=50&l=95032&fromage=60&limit=50&sort=&psf=advsrch',
            'job_element_selector': '//*[@id="sja{}"]/',
            'paging_element_selector': '//*[@id="resultsCol"]/div[27]/a[{}]',
            'paging_type': 'page'

            # //*[@id="sja4"]
            # //*[@id="sja10"]
            },
    'career_builder':
        {
            'url': 'https://www.careerbuilder.com/jobs-software-quality-assurance-engineer-in-95032?keywords=software+quality+assurance+engineer&location=95032&radius=50&emp=jtft%2Cjtfp&pay=120&sort=distance_asc',
            'job_link_element_selector_type': None,
            # /html/body/div[3]/div[7]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/h2[2]/a
            'job_element_selector': None,
            'paging_element_selector': '/html/body/div[3]/div[7]/div[2]/div[1]/div[2]/div/div/a[{}]',
            'paging_type': 'page',
            },
    'dice':
        {
            'url': 'https://www.dice.com/jobs/advancedResult.html?for_one=&for_all={title}&for_exact=&for_none=&for_jt=&for_com=&for_loc=Santa+Clara%2C+CA&jtype=Full+Time&sort=relevance&limit=100&radius=50&jtype=Full+Time&limit=100&radius=50&jtype=Full+Time',
            'format_string': None,
            'job_link_element_selector_type': None,
            '''
    //*[@id="position0"]
    //*[@id="position2"]
    //*[@id="position0"]>> next page
    '''
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
}


class JobDescription(object):

    def __init__(self):
        self.url = ''
        self.title = ''
        self.key_words_to_match = KEY_WORDS
        self.matched_key_words = set()

    def _parse_body_text(self):
        body_text = driver.find_element_by_tag_name('body').text
        parsed_text = body_text.split()
        return parsed_text

    def get_matched_key_words(self):
        parsed_body = _parse_body_text()
        [self.matched_key_words.add(word) for word in parsed_body if
         [True for w in self.key_words_to_match if word == w]]

    def set_title(self, path):
        element = driver.find_element_by_xpath(path)
        self.title = element.text


class JobSite(object):

    def __init__(self,
                 url):
        self.url = url
        self.discarded_titles = []
        self.job_descriptions = []

    def launch_main_page(self):
        driver.get(self.url)

    def page(self, index=None):
        try:
            if index > 1:
                driver.find_element_by_xpath(self.paging_element_selector.format(index)).click()
            else:
                driver.find_element_by_xpath(self.paging_element_selector).click()
        except NoSuchElementException:
            print('NoSuchElementException')

    def get_links_by_tag_name(self, tag_name):
        try:
            links = []
            print('Finding link elements')
            elements = driver.find_elements_by_tag_name(tag_name)
            print('Extracting links')
            links += ([element.get_attribute('href') for element in elements])
            print(links)
            return links
        except NoSuchElementException:
            print('NoSuchElementException')


    def get_links_by_class(self, class_name):
        try:
            links = []
            print('Finding link elements')
            elements = driver.find_elements_by_class_name(class_name)
            print('Extracting links')
            for element in elements:
                links += element.get_attribute('href')
            print(links)
            return links
        except NoSuchElementException:
            print('NoSuchElementException')

    def get_links_by_xpath(self, path, index=None):
        try:
            if index:
                print('Index True')
                elements = driver.find_element_by_xpath(path.format(index))
                print('Found elements by xpath ' + path + ' at index ' + str(index))

            else:
                elements = driver.find_element_by_xpath(path)
                print('Found elements by xpath ' + path)
            links = []
            links += [element.get_attribute('href') for element in elements]
            return links
        except NoSuchElementException:
            print('NoSuchElementException')


def go():
    indeed = JobSite(
                     #paging_element_selector='//*[@id="resultsCol"]/div[27]/a[{}]',
                     url='https://www.indeed.com/jobs?as_and=software+quality+assurance+engineer&as_any=&as_not=&as_ttl=&as_cmp=&jt=fulltime&st=&as_src=&salary=%24145%2C000%2B&radius=50&l=95032&fromage=60&limit=50&sort=&psf=advsrch'
                     )
    indeed.launch_main_page()
    indeed.get_links_by_tag_name('a')

    career_builder = JobSite(
        #job_element_selector='/html/body/div[3]/div[7]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/h2[{}]/a',
        #paging_element_selector='/html/body/div[3]/div[7]/div[2]/div[1]/div[2]/div/div/a[{}]',
        url='https://www.careerbuilder.com/jobs-software-quality-assurance-engineer-in-95032?keywords=software+quality+assurance+engineer&location=95032&radius=50&emp=jtft%2Cjtfp&pay=120&sort=distance_asc',
        )


go()
