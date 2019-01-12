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
                     'php', 'sauce', 'flask', 'shell', 'nas', 'san', 'iscsi', 'scripts', 'scripting',
                     'junit', 'selenium', 'react', 'c#', 'testrail', 'confluence', 'jmeter', 'wifi',]
analysis_software = ['tableau', 'd3.js', 'sas', 'spss', 'd3', 'wireless', 'saas', 'pandas', 'numpy', 'jenkins', 'scipy', 'plan', 'case',
                     'sps', 'spotfire', 'scikits.learn', 'splunk', 'h2o', 'jira', 'functional', 'integration', 'stress', 'load', 'performance',]
bigdata_tool = ['hadoop', 'mapreduce', 'spark', 'pig', 'hive', 'shark', 'oozie', 'zookeeper', 'flume', 'mahout',
                'elasticsearch', 'api', 'Mockito', 'Robotium', 'frontend', 'backend', 'cloud', 'tdd', 'driven', 'bdd']
databases = ['sql', 'nosql', 'hbase', 'cassandra', 'xml', 'rust', 'mongodb', 'mysql', 'mssql', 'postgre', 'oracle',
             'rdbms', 'mobile', 'android', 'ios', 'cucumber', 'iot', 'black', 'white', 'telecommunications',
             'hive', 'cucumber', 'aws', 'azure', 'amazon', 'google', 'rest', 'docker', 'container', 'puppet', 'chef',
             'kubernetes', 'storage', 'network', 'networking', 'maven', 'ci', 'cd', 'ci/cd', 'gui', 'virtual', 'vmware',]
other = ['restassured', 'ios', 'json', 'swift', 'objective-c', 'groovy', '.net', 'angular', 'node.js', 'kafka', 'mesos',
         'django', 'pytest', 'css', 'html', 'appium', 'linux', 'css', 'ui', 'soa', 'unix', 'RESTful', 'Elastic', 'git', 'github', 'database', 'acceptance', 'uat', 'healthcare', 'banking',]

KEY_WORDS = program_languages + analysis_software + bigdata_tool + databases + other
STRIP_WORDS = KEY_WORDS + ['senior', 'director', 'enterprise', 'architect', 'manager', 'lead','&', 'mobile', 'sr', 'jr', 'I', 'II', 'III', 'IV', '(', ')', '.', ',', '/', '\\', "\'", '\"', '-', 'analytics',]
for i in range(0,9):
    STRIP_WORDS.append('{}'.format(i))


summary_dict = {}
for key in KEY_WORDS:
    summary_dict[key] = 0


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

MONSTER_URL = 'https://www.monster.com/jobs/search/Full-Time_8?q=software-quality-assurance-engineer&rad=60&where=san-jose__2c-ca&tm=30'
MONSTER_JOB_DESCRIPTION_TITLE_SELECTOR = '/html/body/div[1]/main/div[1]/header/div[2]/h1'
MONSTER_PAGING_SELECTOR = '//*[@id="loadMoreJobs"]'
MONSTER_JOB_LINK_SELECTOR_TYPE = 'xpath'
MONSTER_JOB_LINK_SELECTOR = '/html/body/div[2]/main/div[1]/div[1]/div/div[1]/div/div/section[{}]/div/div[2]/header/h2/a'
MONSTER_TITLE_SELECTOR_TYPE = 'xpath'

LINKEDIN_URL = 'https://www.linkedin.com/jobs/search?keywords=Software+Quality+Assurance+Engineer&distance=25&locationId=PLACES%2Eus%2E7-1-0-43-18&f_TP=1%2C2%2C3%2C4&f_JT=FULL_TIME&orig=FCTD&trk=jobs_jserp_facet_job_type'
LINKEDIN_JOB_DESCRIPTION_TITLE_SELECTOR = '/html/body/div/main/div[2]/div/div/div/section[5]/section[1]/div/div[1]/div[2]/div[1]/div[1]/h1'
LINKEDIN_PAGING_SELECTOR = '/html/body/div/main/div[2]/div/section[4]/div[2]/div/section[6]/div/div/ul/li[{}]/a'
LINKEDIN_JOB_LINK_SELECTOR_TYPE = 'xpath'
LINKEDIN_JOB_LINK_SELECTOR = '/html/body/div/main/div[2]/div/section[4]/div[2]/div/section[3]/div/ul/li[{}]/div/div[1]/h2/a'
LINKEDIN_TITLE_SELECTOR_TYPE = 'xpath'

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

    def _get_job_description(self):
        driver.get(self.url)
        logging.info('Getting job description at ' + str(self.url))
        print('Getting job description')

    def _parse_body_text(self):
        if self.title:
            logging.info('Parsing job description for ' + self.title +'\nURL: ' + self.url)
            print('Parsing job description for ' + self.title)
            try:
                body_text = driver.find_element_by_tag_name('body').text
                parsed_text = body_text.split()
                return parsed_text
            except NoSuchElementException:
                logging.warning('Can not get body text for ' + self.url)
        else:
            logging.warning('No title found in self.title')


    def _match_keywords(self):
        keydict = {}
        for key in KEY_WORDS:
            keydict[key.lower()] = 0
        parsed_body = self._parse_body_text()
        logging.info('Matching keywords for ' + self.title +'\nURL: ' + self.url)
        print('Matching keywords for ' + self.title)
        for word in parsed_body:
            for key in KEY_WORDS:
                if word.lower() == key.lower() and word.islower() and key.islower():
                    logging.info('Found match word to keyword {word} = {keyword}'.format(word = word.lower(), keyword = key.lower()))
                    keydict[key] = 1
                else:
                    logging.debug('Did not find match {word} = {keyword}'.format(word = word.lower(), keyword = key.lower()))
        if self.title:
            self.per_title_match_dict[self.title] = keydict
        else:
            logging.warning('No title found')

    def _set_title(self):
        try:
            if self.title_selector_type == 'xpath':
                element = driver.find_element_by_xpath(self.title_selector)
            elif self.title_selector_type == 'tag':
                element = driver.find_element_by_tag_name(self.title_selector)
            elif self.title_selector_type == 'class':
                element = driver.find_element_by_class(self.title_selector)
            elif self.title_selector_type == 'css_selector':
                element = driver.find_element_by_css_selector(self.title_selector)

            title = element.text.lower()

            if title and (title.islower() or title.isupper()) and title != ' ':
                self.title = title.lower()
                logging.info('Setting title ' + self.title +'\nURL: ' + self.url)
                print('Setting title ' + self.title)
            else:
                logging.warning('No title found with selector ' + self.title_selector +'\nURL: ' + self.url)
        except NoSuchElementException:
            logging.warning('FAILED TO SET TITLE NoSuchElementException for selector ' + self.title_selector +'\nURL: ' + self.url)
            print('FAILED TO SET TITLE NoSuchElementException')

    def set_should_discard(self):
        if self._score_title() < SYNONYM_MATCH_THRESHOLD:
            logging.info('Discarding Title: {} with score {}'.format(self.title, self._score_title()) +'\nURL: ' + self.url)
            print('Discarding Title: {} with score {}'.format(self.title, self._score_title()))
            self.should_discard = True
        else:
            print('Keeping title: {} with score {}'.format(self.title, self._score_title()))
            logging.info('Keeping title: {} with score {}'.format(self.title, self._score_title()) +'\nURL: ' + self.url)


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

    def _page(self, index):
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

    def _get_links_by_tag_a(self):
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


    def _get_links_by_xpath(self):
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

    def _discard_unmatched_job_descriptions(self):
        for index, jd in enumerate(self.job_descriptions):
            if jd.should_discard:
                logging.info('Adding {title} to discard list'.format(title = jd.title) +'\nURL: ' + self.url)
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

    def _get_totals(self):
        for job in self.job_descriptions:
            try:
                for key, value in job.per_title_match_dict[job.title].items():
                    summary_dict[key] += value
                    logging.info('Adding key: {k} value total: {v}'.format(k = key, v = summary_dict[key]))
            except KeyError:
                    logging.warning('KeyError key = "{}"'.format(str(key)))

    def _file_results(self):
            output_filename = 'job_output.txt'
            write_string = ''
            with open(output_filename, 'a') as file:
                write_string += '-----------------------------------------------\n'
                write_string += 'DISCARDED JOB DESCRIPTIONS TOTAL {}) \n'.format(len(self.discarded_job_descriptions))
                for jd in self.discarded_job_descriptions:
                    write_string += jd.title + '\n'
                write_string += '\n-----------------------------------------------\n'
                write_string += 'KEPT JOB DESCRIPTIONS TOTAL {} \n'.format(len(self.job_descriptions))
                write_string += '-----------------------------------------------\n'
                for job in self.job_descriptions:
                    if job.title != ' ' and job.title:
                        write_string += '\n\n' + job.title.upper() + '\n'
                        write_string += '\nURL: ' + job.url + '\n'
                        write_string += '===============================\n'
                        for key, value in job.per_title_match_dict[job.title].items():
                            try:
                                write_string += '{key}:{value}, '.format(key=key, value = value)
                            except KeyError:
                                logging.warning('KeyError key = ' + key)
                                write_string += 'KeyError key = ' + key
                file.write(write_string)
                print(write_string)
                print('Writing results to file')

    def process_site(self):
        self.launch_main_page()

        for page in range(0,6):
            if page >=1:
                self._page(page)
                logging.info('Paging . . . . . .')
            # Get links by selector type
            if self.job_link_selector_type == 'tag':
                logging.info('Getting links by tag')
                self.clean(self._get_links_by_tag_a())
            elif self.job_link_selector_type == 'xpath':
                logging.info('Getting links by xpath')
                self.clean(self._get_links_by_xpath())
            elif self.job_link_selector_type == 'class':
                self.clean(self._get_links_by_class())
            else:
                logging.warning('Unknown paging selector type: {}'.format(self.job_link_selector_type ) )

            for job_description in self.job_descriptions:
                job_description._get_job_description()
                job_description.title_selector = self.job_descriptions_title_selector
                job_description.title_selector_type = self.title_selector_type
                job_description._set_title()
                job_description.set_should_discard()
                if job_description.should_discard:
                    self._discard_unmatched_job_descriptions()
                else:
                    job_description._match_keywords()
        self._get_totals()
        self._file_results()

    def _get_links_by_class(self):
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

    # print('PROCESSING MONSTER')
    # monster = JobSite(
    #     url= MONSTER_URL,
    #     paging_element_selector=MONSTER_PAGING_SELECTOR,
    #     job_link_selector_type=MONSTER_JOB_LINK_SELECTOR_TYPE,
    #     job_link_selector=MONSTER_JOB_LINK_SELECTOR,
    #     job_descriptions_title_selector=MONSTER_JOB_DESCRIPTION_TITLE_SELECTOR,
    #     site_id='monster',
    #     title_selector_type=MONSTER_TITLE_SELECTOR_TYPE,
    # )
    # monster.process_site()

    print('PROCESSING LINKEDIN')
    linkedin = JobSite(
        url= LINKEDIN_URL,
        paging_element_selector=LINKEDIN_PAGING_SELECTOR,
        job_link_selector_type=LINKEDIN_JOB_LINK_SELECTOR_TYPE,
        job_link_selector=LINKEDIN_JOB_LINK_SELECTOR,
        job_descriptions_title_selector=LINKEDIN_JOB_DESCRIPTION_TITLE_SELECTOR,
        site_id='monster',
        title_selector_type=LINKEDIN_TITLE_SELECTOR_TYPE,
    )
    linkedin.process_site()
    print('Finished')

'''
MAIN
'''
go()
summary_string = '\n\n************************************************\n'
summary_string +='                  SUMMARY'
summary_string += '\n************************************************\n'
summary_string += str([(key, value) for key, value in summary_dict.items() if value > 0])
summary_string += '\n RAW SUMMARY DICT\n'
summary_string += str(summary_dict)

print(summary_string)
logging.info(summary_string)
driver.close()
