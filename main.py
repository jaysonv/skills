from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from selenium.webdriver.common.by import By
from datetime import datetime
import logging

JOB_TITLES = ['Senior Quality Assurance Engineer', 'Senior QA Engineer II', 'Quality Assurance Manager',
              'Quality Assurance Engineer IV', 'Senior Quality Assurance Engineer', 'Sr. Director, Quality Assurance',
              'Lead Quality Engineer', 'software quality assurance', 'sqa', 'qa engineer', 'sdet',
              'software development engineer in test',
              'software test engineer', 'software test automation', 'qa automation',
              'software quality assurance engineer']

program_languages = ['bash', 'python', 'java', 'c++', 'ruby', 'perl', 'matlab', 'javascript', 'scala',
                     'php',
                     'junit', 'selenium', 'react', 'c#']
analysis_software = ['tableau', 'd3.js', 'sas', 'spss', 'd3', 'saas', 'pandas', 'numpy', 'Jenkins', 'scipy',
                     'sps', 'spotfire', 'scikits.learn', 'splunk', 'h2o', 'jira']
bigdata_tool = ['hadoop', 'mapreduce', 'spark', 'pig', 'hive', 'shark', 'oozie', 'zookeeper', 'flume', 'mahout',
                'elasticsearch']
databases = ['sql', 'nosql', 'hbase', 'cassandra', 'xml', 'rust', 'mongodb', 'mysql', 'mssql', 'postgre', 'oracle db',
             'rdbms',
             'hive', 'cucumber', 'aws', 'azure', 'amazon', 'google', 'rest', 'docker', 'container', 'puppet', 'chef',
             'kubernetes', 'storage', 'network', 'networking']
other = ['restassured', 'ios', 'json', 'swift', 'objective-c', 'groovy', '.net', 'angular', 'node.js', 'kafka', 'mesos',
         'django', 'pytest', 'css', 'html', 'appium',]

KEY_WORDS = program_languages + analysis_software + bigdata_tool + databases + other

INDEED_JOB_DESCRIPTION_TITLE_SELECTOR = '/html/body/div[1]/div[3]/div[3]/div/div/div[1]/div[1]/div[1]/h3'
INDEED_URL = 'https://www.indeed.com/jobs?as_and=software+quality+assurance+engineer&as_any=&as_not=&as_ttl=&as_cmp=&jt=fulltime&st=&as_src=&salary=%24145%2C000%2B&radius=50&l=95032&fromage=60&limit=50&sort=&psf=advsrch'
INDEED_PAGING_SELECTOR = '//*[@id="resultsCol"]/div[28]/a[{}]'
INDEED_JOB_LINK_SELECTOR_TYPE = 'tag'
INDEED_JOB_LINK_SELECTOR = None


CAREER_BUILDER_URL = 'https://www.careerbuilder.com/jobs-software-quality-assurance-engineer-in-95032?keywords=software+quality+assurance+engineer&location=95032&radius=50&emp=jtft%2Cjtfp&pay=120&sort=distance_asc'
CAREER_BUILDER_JOB_DESCRIPTION_TITLE_SELECTOR = '//*[@id="main-content"]/div[10]/div[3]/div[1]/div/div[1]/h1'
CAREER_BUILDER_PAGING_SELECTOR = '//*[@id="main-content"]/div[7]/div[2]/div[1]/div[2]/div/div/a[{}]'
CAREER_BUILDER_JOB_LINK_SELECTOR_TYPE = 'xpath'
CAREER_BUILDER_JOB_LINK_SELECTOR = '//*[@id="main-content"]/div[7]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/h2[{}]/a'
# this is also a possible selector //*[@id="job-title"]

driver = webdriver.Firefox()
driver.set_window_position(-2000, -2000)

def make_date_string():
    stamp = datetime.now()
    date_string = stamp.strftime('%Y-%d-%m-%H-%M-%S')
    return date_string

logging.basicConfig(filename='execution_{date}.log'.format(date = make_date_string()), level=logging.INFO)

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

    def __init__(self, url, title_selector = None):
        self.url = url
        self.title = ''
        self.should_discard = False
        self.per_title_match_dict = {}
        self.title_selector = title_selector

    def __str__(self):
        print_string = '==================================\n'
        print_string += 'Job Title {job_title}\n'
        for key, value in self.per_title_match_dict.items():
            print_string += '{key} : {value}, '.format(job_title = self.title, key = key, value = value)

    def get_job_description(self):
        driver.get(self.url)
        logging.info('Getting job description at ' + str(self.url))
        print('Getting job description')

    def _parse_body_text(self):
        if self.title:
            logging.info('Parsing job description for ' + self.title)
            print('Parsing job description for ' + self.title)
            body_text = driver.find_element_by_tag_name('body').text
            parsed_text = body_text.split()
            return parsed_text
        else:
            logging.warning('No title found')


    def match_keywords(self):
        keydict = {}
        for key in KEY_WORDS:
            keydict[key] = 0
        parsed_body = self._parse_body_text()
        logging.info('Matching keywords for ' + self.title)
        print('Matching keywords for ' + self.title)
        for word in parsed_body:
            for key in KEY_WORDS:
                if word == key:
                    logging.info('Found match {word} = {keyword}'.format(word = word, keyword = key))
                    keydict[key] = 1
                else:
                    logging.debug('Did not find match {word} = {keyword}'.format(word = word, keyword = key))
        if self.title:
            self.per_title_match_dict[self.title] = keydict
        else:
            logging.warning('No title found')

    def set_title(self):
        try:
            element = driver.find_element_by_xpath(self.title_selector)
            if element.text:
                self.title = element.text
            else:
                raise NoSuchElementException()
                logging.warning('No title found')

            logging.info('Setting title ' + self.title)
            print('Setting title ' + self.title)
        except NoSuchElementException:
            logging.warning('FAILED TO SET TITLE NoSuchElementException')
            print('FAILED TO SET TITLE NoSuchElementException')


    def set_should_discard(self):
        print('Discarding bad job descriptions')
        set_of_title = set()
        if self.title:
            set_of_title.add(self.title.lower())
        else:
            self.should_discard = True
        set_of_matching = set()
        [set_of_matching.add(title.lower()) for title in JOB_TITLES]
        match = bool(set_of_matching.intersection(set_of_title))
        if match:
            logging.info('Did not discard ' + self.title)
        else:
            logging.info('Discarding ' + self.title)
            self.should_discard = True

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

    def page(self, index = 1):
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
        for index in range(0,500):
            try:
                elements = driver.find_element_by_xpath(self.job_link_selector.format(index))
                logging.info('Found elements by xpath: ' +  self.job_link_selector + '({})'.format(str(index)))
                print('Found elements by xpath: ' +  self.job_link_selector + '({})'.format(str(index)))
                links = []
                links += [element.get_attribute('href') for element in elements]

            except NoSuchElementException:
                logging.warning('NoSuchElementException getting element by xpath: ' + self.job_link_selector + '({})'.format(str(index)))
                print('NoSuchElementException')
                logging.info('Returning links: ' + [link + ', ' for link in links])
                return links
        return links

    def discard_unmatched_job_descriptions(self):
        for index, jd in enumerate(self.job_descriptions):
            if jd.should_discard:
                logging.info('Adding {title} to discard list'.format(title = jd.title))
                self.discarded_job_descriptions.add(self.job_descriptions.pop(index))

    def clean(self, links):
        logging.info('Cleaning links')
        clean_links = []
        clean_links += [link for link in links if 'clk?jk' in link]  #unique identifier for links to job descriptions = 'clk?jk'
        logging.debug('Clean links : ' + str(clean_links))
        self.job_descriptions += [JobDescription(link) for link in clean_links]

    def file_results(self):
            output_filename = 'job_output.txt'
            with open(output_filename, 'a') as file:
                file.write('DISCARDED JOB DESCRIPTIONS (TOTAL {}) \n'.format(len(self.discarded_job_descriptions)))
                write_string = ''
                for jd in self.discarded_job_descriptions:
                    write_string += jd.title + '\n'
                write_string += '\n----------------------------------------------\n'
                write_string += 'COUNTS FOR MATCHING JOB TITLES (Total {})'.format(len(self.job_descriptions))
                write_string += '\n----------------------------------------------\n'
                for job in self.job_descriptions:
                    write_string += '\n' + job.title.upper() + '\n'
                    write_string += '===============================\n'
                    if job.title != '' and job.title:
                        for key, value in job.per_title_match_dict[job.title].items():
                            try:
                                write_string += '{key}:{value}, '.format(key=key, value = value)
                            except KeyError:
                                logging.warning('KeyError key = ' + key)
                                write_string += 'KeyError key = ' + key

                print(write_string)
                print('Writing results to file')
                file.write(write_string)

    def process_site(self):
        self.launch_main_page()

        for page in range(0,6):
            if page >=1:
                self.page(page)
            # Get links by selector type
            if self.job_link_selector_type == 'tag':
                logging.info('Getting links by tag')
                self.clean(self.get_links_by_tag_a())
            elif self.job_link_selector_type == 'xpath':
                logging.info('Getting links by xpath')
                self.clean(self.get_links_by_xpath())
            elif self.job_link_selector_type == 'class':
                self.clean(self.get_links_by_class())

            for job_description in self.job_descriptions:
                job_description.get_job_description()
                job_description.title_selector = self.job_descriptions_title_selector
                job_description.set_title()
                job_description.set_should_discard()
                if job_description.should_discard:
                    self.discard_unmatched_job_descriptions()
                    logging.info('discard_unmatched_job_descriptions added these job descriptions : \n' + str([jd.title + ',' for jd in self.discarded_job_descriptions]))
                else:
                    job_description.match_keywords()
        self.file_results()

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
                     paging_element_selector = INDEED_PAGING_SELECTOR,
                     job_link_selector_type = INDEED_JOB_LINK_SELECTOR_TYPE,
                     job_link_selector = INDEED_JOB_LINK_SELECTOR,
                     job_descriptions_title_selector = INDEED_JOB_DESCRIPTION_TITLE_SELECTOR,
                     )
    indeed.process_site()

    logging.info('PROCESSING CAREER BUILDER')
    print('PROCESSING CAREER BUILDER')
    careerbuilder = JobSite(
                            url = CAREER_BUILDER_URL,
                            paging_element_selector = CAREER_BUILDER_PAGING_SELECTOR,
                            job_link_selector_type = CAREER_BUILDER_JOB_LINK_SELECTOR_TYPE,
                            job_link_selector = CAREER_BUILDER_JOB_LINK_SELECTOR,
                            job_descriptions_title_selector = CAREER_BUILDER_JOB_DESCRIPTION_TITLE_SELECTOR,
                            )
    careerbuilder.process_site()
    print('Finished')

'''
MAIN
'''
go()
driver.close()
