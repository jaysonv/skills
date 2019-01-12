from job_site import JobSite
from selenium import webdriver
import logging
import signal
from utility import make_date_string


INDEED_JOB_DESCRIPTION_TITLE_SELECTOR = '//div[@class="jobsearch-DesktopStickyContainer"]/h3[1]'
INDEED_JOB_DESCRIPTION_TITLE_SELECTOR_TYPE = ''
INDEED_URL = 'https://www.indeed.com/jobs?q=software+quality&l=95032'
INDEED_PAGING_SELECTOR = '//span[.={}]/..'
INDEED_PAGING_SELECTOR_TYPE = 'xpath'
INDEED_JOB_LINK_SELECTOR = 'a[class="jobtitle turnstileLink"]'
INDEED_JOB_LINK_SELECTOR_TYPE = 'css'


CAREER_BUILDER_URL = 'https://www.careerbuilder.com/jobs-software-quality-assurance-engineer-in-95032?keywords=software+quality+assurance+engineer&location=95032&radius=50&emp=jtft%2Cjtfp&pay=120&sort=distance_asc'
CAREER_BUILDER_JOB_DESCRIPTION_TITLE_SELECTOR = '//*[@id="main-content"]/div[10]/div[3]/div[1]/div/div[1]/h1'
CAREER_BUILDER_PAGING_SELECTOR = '//*[@id="main-content"]/div[7]/div[2]/div[1]/div[2]/div/div/a[{}]'
CAREER_BUILDER_JOB_LINK_SELECTOR_TYPE = 'xpath'
CAREER_BUILDER_JOB_LINK_SELECTOR = '/html/body/div[3]/div[7]/div[2]/div[1]/div[1]/div[2]/div[{}]/div[2]/div[1]/h2[2]/a'

driver = webdriver.Firefox(service_log_path='../logs/geckodriver.log')
driver.set_window_position(-2000, -2000)

# TODO, logger config
logging.basicConfig(filename='../logs/execution_{date}.log'.format(date=make_date_string()), level=logging.INFO)

'''
SITE_DICT = {


    'dice':
        {
            'url': 'https://www.dice.com/jobs/advancedResult.html?for_one=&for_all={title}&for_exact=&for_none=&for_jt=&for_com=&for_loc=Santa+Clara%2C+CA&jtype=Full+Time&sort=relevance&limit=100&radius=50&jtype=Full+Time&limit=100&radius=50&jtype=Full+Time',
            'format_string': None,
            'job_link_element_selector_type': None,

            'job_element_selector': None,
            'next_page_selector': '/html/body/div[8]/div[3]/div[2]/div[1]/div[6]/div[2]/div/ul/li[{}]/a',
            'paging_type': 'page',
            },
    'monster':
        {
            'url': 'https://www.monster.com/jobs/search/Full-Time_8?q=software-quality-assurance&intcid=skr_navigation_nhpso_searchMain&rad=50&where=Los-Gatos__2c-CA&tm=30',
            'format_string': None,
            'job_link_element_selector_type': None,  # NEED TO BE "PAGED    "
            'job_element_selector': None,
            'next_page_selector': '//*[@id="loadMoreJobs"]',
            'paging_type': 'button',

        },
    'glass_door':
        {
            'url': 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword=Software%20Quality%20Assurance%20Engineer&locT=C&locId=1147436&locKeyword=San%20Jose,%20CA&jobType=fulltime&fromAge=30&minSalary=170000&includeNoSalaryJobs=false&radius=25&cityId=-1&minRating=4.00&industryId=-1&companyId=-1&applicationType=0&employerSizes=0&remoteWorkType=0',
            'format_string': None,
            'job_link_element_selector_type': None,
            'job_element_selector': None,
            'next_page_selector': '/html/body/div[3]/div/div/div/div[1]/div/div[2]/section/article/div/div[3]/div[2]/div/div/ul/li[{}]/a',
            'paging_type': 'page',
            },
    'linked_in':
        {
            'url': 'https://www.linkedin.com/jobs/search/?distance=50&f_E=3%2C4&f_JT=F&f_SB2=5&f_TP=1%2C2%2C3%2C4&keywords=software%20quality%20assurance%20engineer&location=Santa%20Clara%2C%20California&locationId=PLACES.us.7-1-0-43-18',
            'format_string': None,
            'job_link_element_selector_type': None,
            'job_element_selector': None,
            'next_page_selector': '//*[@id="ember975"]/li/ol/li[{}]/button',
            'paging_type': 'page',  # yes, page!
            },
'''

def main():
    logging.info('PROCESSING INDEED')
    print('PROCESSING INDEED')
    indeed = JobSite(
                     selenium_driver=driver,
                     url=INDEED_URL,
                     next_page_selector=INDEED_PAGING_SELECTOR,
                     next_page_selector_type=INDEED_PAGING_SELECTOR_TYPE,
                     job_link_selector_type=INDEED_JOB_LINK_SELECTOR_TYPE,
                     job_link_selector=INDEED_JOB_LINK_SELECTOR,
                     job_posting_title_selector=INDEED_JOB_DESCRIPTION_TITLE_SELECTOR,
                     )
    indeed.process_site()

    logging.info('PROCESSING CAREER BUILDER')
    print('PROCESSING CAREER BUILDER')
    careerbuilder = JobSite(
                            selenium_driver=driver,
                            url=CAREER_BUILDER_URL,
                            next_page_selector=CAREER_BUILDER_PAGING_SELECTOR,
                            next_page_selector_type=INDEED_PAGING_SELECTOR_TYPE,
                            job_link_selector_type=CAREER_BUILDER_JOB_LINK_SELECTOR_TYPE,
                            job_link_selector=CAREER_BUILDER_JOB_LINK_SELECTOR,
                            job_posting_title_selector=CAREER_BUILDER_JOB_DESCRIPTION_TITLE_SELECTOR,
                            )
    careerbuilder.process_site()
    print('Finished')


if __name__ == '__main__':
    def cleanup(*args):
        driver.quit()

    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)
    try:
        main()
    except Exception as exc:
        logging.exception(exc)
        raise
    finally:
        cleanup()

