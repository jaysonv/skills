from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from selenium.webdriver.common.by import By
from datetime import datetime
import pdb
import pandas as pd

discaded_job_titles = set()

JOB_TITLES = ['Senior Quality Assurance Engineer', 'Senior QA Engineer II', 'Quality Assurance Manager', 'Quality Assurance Engineer IV', 'Senior Quality Assurance Engineer', 'Sr. Director, Quality Assurance', 'Lead Quality Engineer', 'software quality assurance', 'sqa', 'qa engineer', 'sdet', 'software development engineer in test',
                     'software test engineer', 'software test automation', 'qa automation', 'software quality assurance engineer']


program_languages = ['job_title', 'bash', 'python', 'java', 'c++', 'ruby', 'perl', 'matlab', 'javascript', 'scala', 'php',
                     'junit', 'selenium', 'React',  'c#']
analysis_software = ['tableau', 'd3.js', 'sas', 'spss', 'd3', 'saas', 'pandas', 'numpy', 'Jenkins', 'scipy',
                     'sps', 'spotfire', 'scikits.learn', 'splunk', 'h2o', 'jira']
bigdata_tool = ['hadoop', 'mapreduce', 'spark', 'pig', 'hive', 'shark', 'oozie', 'zookeeper', 'flume', 'mahout',
                'elasticsearch']
databases = ['sql', 'nosql', 'hbase', 'cassandra', 'xml' ,'rust', 'mongodb', 'mysql', 'mssql', 'postgre', 'oracle db', 'rdbms',
             'hive', 'cucumber', 'aws', 'azure', 'amazon', 'google', 'rest', 'docker', 'container', 'puppet', 'chef', 'kubernetes', 'storage', 'network', 'networking']
other = ['restassured', 'ios', 'json', 'swift', 'objective-c', 'groovy', '.net', 'angular', 'node.js', 'kafka', 'mesos', 'django', 'pytest', 'css', 'html', 'appium', 'testng']

COLUMNS = program_languages + analysis_software + bigdata_tool + databases + other

driver = webdriver.Firefox()
driver.set_window_position(-2000, -2000)

job_data = pd.DataFrame(columns = COLUMNS)

SITE_URLS = {
    'indeed' :
    {'url': 'https://www.indeed.com/jobs?as_and=software+quality+assurance+engineer&as_any=&as_not=&as_ttl=&as_cmp=&jt=fulltime&st=&as_src=&salary=%24145%2C000%2B&radius=50&l=95032&fromage=60&limit=50&sort=&psf=advsrch',
     'format_string' : None,
     'select_by' : 'class',
     'select_string': 'turnstileLink',
     'paging_element_select_by': None,
     'paging_select_string': None,
    },
    'career_builder':
    {'url': 'https://www.careerbuilder.com/jobs-software-quality-assurance-engineer-in-95032?keywords=software+quality+assurance+engineer&location=95032&radius=50&emp=jtft%2Cjtfp&pay=120&sort=distance_asc',
     'format_string' : None,
     'select_by' : None,
     'select_string': None,
     'paging_element_select_by': None,
     'paging_select_string': None,
    },
    'dice':
    {'url': 'https://www.dice.com/jobs/advancedResult.html?for_one=&for_all={title}&for_exact=&for_none=&for_jt=&for_com=&for_loc=Santa+Clara%2C+CA&jtype=Full+Time&sort=relevance&limit=100&radius=50&jtype=Full+Time&limit=100&radius=50&jtype=Full+Time',
    'format_string' : None,
    'select_by' : None,
    'select_string': None,
    'paging_element_select_by': None,
    'paging_select_string': None,
    },
    'monster':
    {
    'url': 'https://www.monster.com/jobs/search/Full-Time_8?q=software-quality-assurance&intcid=skr_navigation_nhpso_searchMain&rad=50&where=Los-Gatos__2c-CA&tm=30',
    'format_string': None,
    'select_by' : None,
    'select_string': None,
    'paging_element_select_by': None,
    'paging_select_string': None,
    },
    'glass_door':
    {'url': 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=Software%20Quality%20Assurance%20Engineer&locT=C&locId=1147436&locKeyword=San%20Jose,%20CA&jobType=fulltime&fromAge=30&minSalary=170000&includeNoSalaryJobs=false&radius=25&cityId=-1&minRating=4.00&industryId=-1&companyId=-1&applicationType=0&employerSizes=0&remoteWorkType=0',
    'format_string': None,
    'select_by' : None,
    'select_string': None,
    'paging_element_select_by': None,
    'paging_select_string': None,
    },
    'linked_in':
    {'url' : 'https://www.linkedin.com/jobs/search/?distance=50&f_E=3%2C4&f_JT=F&f_SB2=5&f_TP=1%2C2%2C3%2C4&keywords=software%20quality%20assurance%20engineer&location=Santa%20Clara%2C%20California&locationId=PLACES.us.7-1-0-43-18',
    'format_string' : None,
    'select_by' : None,
    'select_string': None,
    'paging_element_select_by': None,
    'paging_select_string': None,
    },
    }

'''
- Go to website with specific job query url string
- For each job title listed, get job title
- For each job title listed, get link to job description
- For each job description link, go to job description
- Grab body text
- Convert raw body text to words
- Count words = search terms
- Generalize for any initial search query and keyword set

'''

def open_primary_query_site_url(site):
    print('Going to site ' + site)
    driver.get(SITE_URLS[site]['url'])

def select_job_descrition_urls_and_titles(site):
    job_description_urls = []
    job_titles =[]
    if SITE_URLS[site]['select_by'] == 'class':
        #element.get_attribute('href'))
        elements = driver.find_elements_by_class_name(SITE_URLS[site]['select_string'])
        job_hyperlinks = [element.get_attribute('href') for element in elements]
        raw_titles = [element.text for element in elements]
        matching_titles = [title for title in raw_titles if [True for item in JOB_TITLES if title == item]]
        for title in raw_titles:
            for jt in JOB_TITLES:
                if title != jt:
                    discaded_job_titles.add(title)
                    
    return {'job_hyperlinks': job_hyperlinks, 'job_titles' : matching_titles}

def go():
    for site in SITE_URLS:
        if site == 'indeed':
            open_primary_query_site_url(site)
            urls_titles_dict = select_job_descrition_urls_and_titles(site)

    #print('URLS: ' + str(urls_titles_dict['job_hyperlinks']))
    print('--------------------------------')
    print('Titles: ' + str(urls_titles_dict['job_titles']))
    print('--------------------------------')
    print('Discards: ' + str(discaded_job_titles))

go()
driver.close()
