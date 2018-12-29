from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import TimeoutException, InvalidArgumentException
from selenium.webdriver.common.by import By
from datetime import datetime
import pdb

driver = webdriver.Firefox()
driver.set_window_position(-2000, -2000)

SITE_URLS = {
    'indeed' :
    {'url': 'https://www.indeed.com/jobs?as_and=&as_any=&as_not=&as_ttl=&as_cmp=&jt=fulltime&st=&as_src=&salary=%24145%2C000%2B&radius=50&l=95032&fromage=60&limit=50&sort=&psf=advsrch',
     'format_string' : None,
     'select_by' : 'class',
     'select_string': 'turnstileLink',
    },
    'career_builder':
    {'url': 'https://www.careerbuilder.com/jobs-software-quality-assurance-engineer-in-95032?keywords=software+quality+assurance+engineer&location=95032&radius=50&emp=jtft%2Cjtfp&pay=120&sort=distance_asc',
     'format_string' : None,
     'select_by' : None,
     'select_string': None,
    },
    'dice':
    {'url': 'https://www.dice.com/jobs/advancedResult.html?for_one=&for_all={title}&for_exact=&for_none=&for_jt=&for_com=&for_loc=Santa+Clara%2C+CA&jtype=Full+Time&sort=relevance&limit=100&radius=50&jtype=Full+Time&limit=100&radius=50&jtype=Full+Time',
    'format_string' : None,
    'select_by' : None,
    'select_string': None,
    },
    'monster':
    {
    'url': 'https://www.monster.com/jobs/search/Full-Time_8?q=software-quality-assurance&intcid=skr_navigation_nhpso_searchMain&rad=50&where=Los-Gatos__2c-CA&tm=30',
    'format_string': None,
    'select_by' : None,
    'select_string': None,
    },
    'glass_door':
    {'url': 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=Software%20Quality%20Assurance%20Engineer&locT=C&locId=1147436&locKeyword=San%20Jose,%20CA&jobType=fulltime&fromAge=30&minSalary=170000&includeNoSalaryJobs=false&radius=25&cityId=-1&minRating=4.00&industryId=-1&companyId=-1&applicationType=0&employerSizes=0&remoteWorkType=0',
    'format_string': None,
    'select_by' : None,
    'select_string': None,
    },
    'linked_in':
    {'url' : 'https://www.linkedin.com/jobs/search/?distance=50&f_E=3%2C4&f_JT=F&f_SB2=5&f_TP=1%2C2%2C3%2C4&keywords=software%20quality%20assurance%20engineer&location=Santa%20Clara%2C%20California&locationId=PLACES.us.7-1-0-43-18',
    'format_string' : None,
    'select_by' : None,
    'select_string': None,
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

def open_primary_query_site_url():
    url =   SITE_URLS['indeed']['url']
    driver.get(url)

open_primary_query_site_url()
