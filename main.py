from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from selenium.webdriver.common.by import By
from datetime import datetime
import pdb
import pandas as pd

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

INDEED_TITLE_XPATH = '/html/body/div[1]/div[3]/div[3]/div/div/div[1]/div[1]/div[1]/h3'
INDEED_URL = 'https://www.indeed.com/jobs?as_and=software+quality+assurance+engineer&as_any=&as_not=&as_ttl=&as_cmp=&jt=fulltime&st=&as_src=&salary=%24145%2C000%2B&radius=50&l=95032&fromage=60&limit=50&sort=&psf=advsrch'





driver = webdriver.Firefox()
driver.set_window_position(-2000, -2000)

job_data = pd.DataFrame(columns=KEY_WORDS)
'''
SITE_DICT = {

    'career_builder':
        {
            'url': 'https://www.careerbuilder.com/jobs-software-quality-assurance-engineer-in-95032?keywords=software+quality+assurance+engineer&location=95032&radius=50&emp=jtft%2Cjtfp&pay=120&sort=distance_asc',

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

    def __init__(self, url):
        self.url = url
        self.key_words_to_match = KEY_WORDS
        self.matched_key_words = set()
        self.title = ''
        self.should_discard = False
        self.titles_to_match = JOB_TITLES

    def get_job_description(self, url):
        driver.get(url)
        print('Getting job description for ' + self.title)

    def _parse_body_text(self):
        print('Parsing job description for ' + self.title)
        body_text = driver.find_element_by_tag_name('body').text
        parsed_text = body_text.split()
        return parsed_text

    def set_matched_key_words(self):
        print('Matching keywords for ' + self.title)
        parsed_body = self._parse_body_text()
        [self.matched_key_words.add(word) for word in parsed_body if
         [True for w in self.key_words_to_match if word.lower() == w.lower()]]

    def set_title(self, path):
        try:
            element = driver.find_element_by_xpath(path)
            self.title = element.text
        except NoSuchElementException:
            print('FAILED TO SET TITLE NoSuchElementException')

    def set_should_discard(self):
        print('Should title {} get discarded?'.format(self.title))
        match_list = self.titles_to_match
        [match_list.pop(index) for index, match_title in enumerate(self.titles_to_match) if self.title != match_title]
        if match_list:
            self.should_discard = False
            print('Do not discard ' + self.title)
        else:
            self.should_discard = True
            print('Yes, discard ' + self.title)


class JobSite(object):

    def __init__(self,
                 url):
        self.url = url
        self.discarded_job_descriptions = set()
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
            links += ([element.get_attribute('href') for element in elements if element.get_attribute('href') != None ])
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

    def discard_unmatched_job_descriptions(self):
        self.discarded_job_descriptions += [self.job_descriptions.pop(index)for index, jd in enumerate(self.job_descriptions) if jd.should_discard]


def go():
    clean_links =[]

    '''
            INDEED
    '''
    indeed = JobSite(
                     url=INDEED_URL
                     )
    indeed.launch_main_page()
    raw_links = indeed.get_links_by_tag_name('a')
    clean_links += [link for link in raw_links if 'clk?jk' in link]  #unique identifier for links to job descriptions = 'clk?jk'
    indeed.job_descriptions += [JobDescription(link) for link in clean_links]
    for job_description in indeed.job_descriptions:
        job_description.get_job_description(job_description.url)
        job_description.set_title(INDEED_TITLE_XPATH)
        job_description.set_should_discard()
        if job_description.should_discard:
            indeed.discard_unmatched_job_descriptions()
        else:
            job_description.set_matched_key_words()


    career_builder = JobSite(
        url='https://www.careerbuilder.com/jobs-software-quality-assurance-engineer-in-95032?keywords=software+quality+assurance+engineer&location=95032&radius=50&emp=jtft%2Cjtfp&pay=120&sort=distance_asc',
        )


    stamp = datetime.now()
    date_string = stamp.strftime('%Y-%d-%m-%H-%M-%S')
    output_filename = 'output_{}.txt'.format(date_string)



go()
