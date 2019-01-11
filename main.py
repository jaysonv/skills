from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from selenium.webdriver.common.by import By
from datetime import datetime
import logging

SYNONYM_MATCH_THRESHOLD = 90

SYNONYMS = {'software': 30, 'quality': 80, 'assurance': 90, 'qa': 100, 'sqa': 100, 'sdet': 100, 'test': 70, 'automation': 70, 'engineer': 20}


program_languages = ['bash', 'python', 'java', 'c++', 'ruby', 'perl', 'matlab', 'javascript', 'scala', 'firmware'
                     'php', 'Sauce Labs', 'flask', 'shell', 'Telecom', 'NAS', 'SAN', 'iSCSI', 'scripts', 'scripting',
                     'junit', 'selenium', 'react', 'c#', 'TestRail', 'Confluence', 'JMeter']
analysis_software = ['tableau', 'd3.js', 'sas', 'spss', 'd3', 'saas', 'pandas', 'numpy', 'Jenkins', 'scipy', 'plan', 'case',
                     'sps', 'spotfire', 'scikits.learn', 'splunk', 'h2o', 'jira', 'functional', 'integration', 'stress', 'load', 'performance']
bigdata_tool = ['hadoop', 'mapreduce', 'spark', 'pig', 'hive', 'shark', 'oozie', 'zookeeper', 'flume', 'mahout',
                'elasticsearch', 'api', 'Mockito', 'Robotium', 'frontend', 'backend']
databases = ['sql', 'nosql', 'hbase', 'cassandra', 'xml', 'rust', 'mongodb', 'mysql', 'mssql', 'postgre', 'oracle',
             'rdbms', 'mobile', 'android', 'ios', 'cucumber', 'iot', 'black', 'white', 'telecommunications',
             'hive', 'cucumber', 'aws', 'azure', 'amazon', 'google', 'rest', 'docker', 'container', 'puppet', 'chef',
             'kubernetes', 'storage', 'network', 'networking', 'maven', 'ci', 'cd', 'ci/cd', 'gui']
other = ['restassured', 'ios', 'json', 'swift', 'objective-c', 'groovy', '.net', 'angular', 'node.js', 'kafka', 'mesos',
         'django', 'pytest', 'css', 'html', 'appium', 'linux', 'css', 'ui', 'soa', 'unix', 'RESTful', 'Elastic', 'git', 'github', 'database', 'acceptance', 'uat', 'healthcare', 'banking']

KEY_WORDS = program_languages + analysis_software + bigdata_tool + databases + other
STRIP_WORDS = KEY_WORDS + ['senior', 'director', 'manager', 'lead', 'mobile', 'sr', 'jr', 'I', 'II', 'III', 'IV', '(', ')', '.', ',', '/', '\\', "\'", '\"', '-', 'analytics']
for i in range(0,9):
    STRIP_WORDS.append('{}'.format(i))

INDEED_JOB_DESCRIPTION_TITLE_SELECTOR = '/html/body/div[1]/div[3]/div[3]/div/div/div[1]/div[1]/div[1]/h3'
INDEED_URL = 'https://www.indeed.com/jobs?as_and=software+quality+assurance+engineer&as_any=&as_not=&as_ttl=&as_cmp=&jt=fulltime&st=&as_src=&salary=%24145%2C000%2B&radius=50&l=95032&fromage=60&limit=50&sort=&psf=advsrch'
INDEED_PAGING_SELECTOR = '//*[@id="resultsCol"]/div[28]/a[{}]'
INDEED_JOB_LINK_SELECTOR_TYPE = 'tag'
INDEED_JOB_LINK_SELECTOR = 'a'
INDEED_TITLE_SELECTOR_TYPE = 'xpath'

CAREER_BUILDER_URL = 'https://www.careerbuilder.com/jobs-software-quality-assurance-engineer-in-95032?keywords=software+quality+assurance+engineer&location=95032&radius=50&emp=jtft%2Cjtfp&pay=120&sort=distance_asc'
CAREER_BUILDER_JOB_DESCRIPTION_TITLE_SELECTOR = '.large-push-3 > div:nth-child(1) > div:nth-child(1) > h1:nth-child(1)'
CAREER_BUILDER_PAGING_SELECTOR = '/html/body/div[3]/div[7]/div[2]/div[1]/div[2]/div/div/a[{}]'
CAREER_BUILDER_JOB_LINK_SELECTOR_TYPE = 'xpath'
CAREER_BUILDER_JOB_LINK_SELECTOR = '/html/body/div[3]/div[7]/div[2]/div[1]/div[1]/div[2]/div[{}]/div[2]/div[1]/h2[2]/a'
CAREER_BUILDER_TITLE_SELECTOR_TYPE = 'css_selector'



DICE_URL = 'https://www.dice.com/jobs/q-Software_QA_Engineer-jtype-Full+Time-l-Santa_Clara%2C_CA-radius-50-jobs'
DICE_JOB_DESCRIPTION_TITLE_SELECTOR ='//*[@id="jt"]'
DICE_PAGING_SELECTOR = '//*[@id="dice_paging_btm"]/ul/li[{}]/a'
DICE_JOB_LINK_SELECTOR_TYPE = 'xpath'
DICE_JOB_LINK_SELECTOR = '//*[@id="position{}"]'
DICE_TITLE_SELECTOR_TYPE = 'xpath'


driver = webdriver.Firefox()
driver.set_window_position(-2000, -2000)

def make_date_string():
    stamp = datetime.now()
    date_string = stamp.strftime('%Y-%d-%m-%H-%M-%S')
    return date_string

logging.basicConfig(filename='execution_{date}.log'.format(date = make_date_string()), level=logging.INFO)


class JobDescription(object):

    def __init__(self, url, title_selector = None, title_selector_type = None):
        self.url = url
        self.title = ''
        self.should_discard = False
        self.per_title_match_dict = {}
        self.title_selector = title_selector
        self.title_selector_type = title_selector_type

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
            try:
                body_text = driver.find_element_by_tag_name('body').text
                parsed_text = body_text.split()
                return parsed_text
            except NoSuchElementException:
                logging.warning('Can not get body text for ' + self.url)
        else:
            logging.warning('No title found in self.title')


    def match_keywords(self):
        keydict = {}
        for key in KEY_WORDS:
            keydict[key.lower()] = 0
        parsed_body = self._parse_body_text()
        logging.info('Matching keywords for ' + self.title)
        print('Matching keywords for ' + self.title)
        for word in parsed_body:
            for key in KEY_WORDS:
                if word.lower() == key.lower():
                    logging.info('Found match {word} = {keyword}'.format(word = word.lower(), keyword = key.lower()))
                    keydict[key] = 1
                else:
                    logging.debug('Did not find match {word} = {keyword}'.format(word = word.lower(), keyword = key.lower()))
        if self.title:
            self.per_title_match_dict[self.title] = keydict
        else:
            logging.warning('No title found')

    def set_title(self):
        try:
            if self.title_selector_type == 'xpath':
                element = driver.find_element_by_xpath(self.title_selector)
            elif self.title_selector_type == 'tag':
                element = driver.find_element_by_tag_name(self.title_selector)
            elif self.title_selector_type == 'class':
                element = driver.find_element_by_class(self.title_selector)
            elif self.title_selector_type == 'css_selector':
                element = driver.find_element_by_css_selector(self.title_selector)

            if element.text:
                self.title = element.text
                logging.info('Setting title ' + self.title)
                print('Setting title ' + self.title)
            else:
                logging.warning('No title found with selector ' + self.title_selector)
        except NoSuchElementException:
            logging.warning('FAILED TO SET TITLE NoSuchElementException for selector ' + self.title_selector)
            print('FAILED TO SET TITLE NoSuchElementException')

    def set_should_discard(self):
        if self._score_title() < SYNONYM_MATCH_THRESHOLD:
            logging.info('Discarding Title: {} with score {}'.format(self.title, self._score_title()))
            print('Discarding Title: {} with score {}'.format(self.title, self._score_title()))
            self.should_discard = True
        else:
            print('Keeping title: {} with score {}'.format(self.title, self._score_title()))
            logging.info('Keeping title: {} with score {}'.format(self.title, self._score_title()))


    def _strip_title(self):
        clean_words = ''
        lower_title = self.title.lower()
        title_words = lower_title.split()
        logging.info('Title Split to: ' + str(title_words))
        for word in title_words:
            for strip_it in STRIP_WORDS:
                index = word.find(strip_it)
                if index:
                    logging.debug('Stripping "{}" from "{}"'.format(strip_it, word))
                    clean_words = title_words[0:index]
        logging.info('Stripped Title = ' + str(clean_words) + ' | Unstripped = ' + self.title)
        return clean_words


    def _score_title(self):
        words_to_score = self._strip_title()
        score = 0
        for key, value in SYNONYMS.items():
            for word in words_to_score:
                if word == key:
                    score += value
                    logging.info('Keyword match found: {} value: {}'.format(key, value))
        logging.info('Title "{}" score: {}'.format(words_to_score, score))
        return score


class JobSite(object):

    def __init__(self,
                 url, paging_element_selector, job_link_selector_type, job_link_selector, job_descriptions_title_selector, site_id, title_selector_type):
        self.url = url
        self.discarded_job_descriptions = set()
        self.job_descriptions = []
        self.paging_element_selector = paging_element_selector
        self.job_link_selector_type = job_link_selector_type
        self.job_descriptions_title_selector = job_descriptions_title_selector
        self.job_link_selector = job_link_selector
        self.site_id = site_id
        self.title_selector_type = title_selector_type

    def launch_main_page(self):
        driver.get(self.url)

    def page(self, index):
        logging.info('Paging index is ' +str(index))
        try:
            if index >= 1:
                driver.find_element_by_xpath(self.paging_element_selector.format(index)).click()
                logging.info('Page by clicking ' + self.paging_element_selector.format(index))
            else:
                driver.find_element_by_xpath(self.paging_element_selector).click()
                logging.info('Page by clicking ' + self.paging_element_selector)
            print('Paging / clicking "Load More.."')
        except NoSuchElementException:
            print('NoSuchElementException - which might be expected when paging')
            logging.warning('NoSuchElementException - which might be expected when paging using ' + self.paging_element_selector.format(index))
        except ElementClickInterceptedException:
            logging.warning('ElementClickInterceptedException for ' + self.paging_element_selector.format(index))

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
            logging.warning('NoSuchElementException finding job description links by tag name')
            print('NoSuchElementException')


    def get_links_by_xpath(self):
        links = []
        for index in range(0, 1001):
            try:
                elements = driver.find_elements_by_xpath(self.job_link_selector.format(index))
                logging.debug('Found elements by xpath: ' +  self.job_link_selector.format(str(index)))
                links += [element.get_attribute('href') for element in elements]
            except NoSuchElementException:
                logging.warning('NoSuchElementException getting element by xpath: ' + self.job_link_selector.format(str(index)))
                print('NoSuchElementException')

        logging.info('Returning links: ' + str(links))
        return links

    def discard_unmatched_job_descriptions(self):
        for index, jd in enumerate(self.job_descriptions):
            if jd.should_discard:
                logging.info('Adding {title} to discard list'.format(title = jd.title))
                self.discarded_job_descriptions.add(self.job_descriptions.pop(index))

    def clean(self, links):
        if self.site_id == 'indeed':
            logging.info('Cleaning {} links'.format(self.site_id))
            clean_links = []
            clean_links += [link for link in links if 'clk?jk' in link]  #unique identifier for links on indeed to job descriptions = 'clk?jk'
            logging.debug('Clean links : ' + str(clean_links))
            self.job_descriptions += [JobDescription(link) for link in clean_links]
        else:
            self.job_descriptions += [JobDescription(link) for link in links]

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
                    write_string += '\n\n' + job.title.upper() + '\n'
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
            else:
                logging.warning('Unknown paging selector type: {}'.format(self.job_link_selector_type ) )

            for job_description in self.job_descriptions:
                job_description.get_job_description()
                job_description.title_selector = self.job_descriptions_title_selector
                job_description.title_selector_type = self.title_selector_type
                job_description.set_title()
                job_description.set_should_discard()
                if job_description.should_discard:
                    self.discard_unmatched_job_descriptions()
                else:
                    job_description.match_keywords()
        self.file_results()

    def get_links_by_class(self):
        pass


def go():
    # logging.info('PROCESSING INDEED')
    # print('PROCESSING INDEED')
    # indeed = JobSite(
    #                  url=INDEED_URL,
    #                  paging_element_selector = INDEED_PAGING_SELECTOR,
    #                  job_link_selector_type = INDEED_JOB_LINK_SELECTOR_TYPE,
    #                  job_link_selector = INDEED_JOB_LINK_SELECTOR,
    #                  job_descriptions_title_selector = INDEED_JOB_DESCRIPTION_TITLE_SELECTOR,
    #                  site_id = 'indeed',
    #                  title_selector_type = INDEED_TITLE_SELECTOR_TYPE,
    #                  )
    # indeed.process_site()
    #
    # logging.info('PROCESSING CAREER BUILDER')
    # print('PROCESSING CAREER BUILDER')
    # careerbuilder = JobSite(
    #                         url = CAREER_BUILDER_URL,
    #                         paging_element_selector = CAREER_BUILDER_PAGING_SELECTOR,
    #                         job_link_selector_type = CAREER_BUILDER_JOB_LINK_SELECTOR_TYPE,
    #                         job_link_selector = CAREER_BUILDER_JOB_LINK_SELECTOR,
    #                         job_descriptions_title_selector = CAREER_BUILDER_JOB_DESCRIPTION_TITLE_SELECTOR,
    #                         site_id = 'careerbuilder',
    #                         title_selector_type = CAREER_BUILDER_TITLE_SELECTOR_TYPE,
    # )
    # careerbuilder.process_site()
    # logging.info('PROCESSING DICE')
    # print('PROCESSING DICE')
    # dice = JobSite(
    #     url=DICE_URL,
    #     paging_element_selector=DICE_PAGING_SELECTOR,
    #     job_link_selector_type=DICE_JOB_LINK_SELECTOR_TYPE,
    #     job_link_selector=DICE_JOB_LINK_SELECTOR,
    #     job_descriptions_title_selector=DICE_JOB_DESCRIPTION_TITLE_SELECTOR,
    #     site_id='dice',
    #     title_selector_type=DICE_TITLE_SELECTOR_TYPE,
    # )
    # dice.process_site()

    print('Finished')

'''
MAIN
'''
go()
driver.close()
