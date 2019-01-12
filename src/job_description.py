from collections import Counter
import logging
from selenium.common.exceptions import NoSuchElementException
from utility import make_date_string


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


# TODO, make a logger config
logging.basicConfig(filename='../logs/execution_{date}.log'.format(date=make_date_string()), level=logging.INFO)


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
            selenium_driver.get(url)

            title = selenium_driver.find_element_by_xpath(title_selector).text
            logging.info('Title is: {title}'.format(title=title))

            description = selenium_driver.find_element_by_tag_name('body').text

            word_counts = Counter(description.split())
            matching_keywords = {word: count for word, count in word_counts.items() if word in KEY_WORDS}
            logging.info('Matching keywords are: {}'.format(matching_keywords))
            selenium_driver.back()
            return cls(url=url, title=title, keyword_matches=matching_keywords)
        except NoSuchElementException as exc:
            logging.exception(msg=exc)
        return None
