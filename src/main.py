import logging
from functools import partial
from job_posting_link_crawler import JobPostingLinkCrawler
from job_posting_parser import JobPostingParser
import multiprocessing
from selenium import webdriver
import signal
from utility import make_date_string

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


def cleanup(driver):
    driver.quit()


def crawl_site_for_job_links(site_config):
    driver = webdriver.Firefox()
    signal.signal(signal.SIGTERM, partial(cleanup, driver))
    signal.signal(signal.SIGINT, partial(cleanup, driver))
    try:
        crawler = JobPostingLinkCrawler(driver, site_config)
        crawler.start()
    except Exception:
        raise
    finally:
        cleanup(driver)
    return crawler.found_links


def parse_job_posting_links(*args):
    posting_links, site_config = args

    driver = webdriver.Firefox()
    signal.signal(signal.SIGTERM, partial(cleanup, driver))
    signal.signal(signal.SIGINT, partial(cleanup, driver))
    try:
        parser = JobPostingParser(driver, posting_links, site_config)
        parser.start()
    except Exception:
        raise
    finally:
        cleanup(driver)
    return parser.job_postings



def main():
    sites = {'indeed': {
            'search_start_url': 'https://www.indeed.com/jobs?q=software+quality&l=95032',
            'next_page_selector': '//span[.={}]/..',
            'next_page_selector_type': 'xpath',
            'job_link_selector': 'a[class="jobtitle turnstileLink"]',
            'job_link_selector_type': 'css',
            'job_posting_title_selector': 'h3[class$="JobInfoHeader-title"]',
            'job_posting_title_selector_type': 'css',
            'job_posting_description_selector': 'div[class^="jobsearch-JobComponent-description"]',
            'job_posting_description_selector_type': 'css',
            'use_solitary_paging': True},
        'careerbuilder': {
            'search_start_url': 'https://www.indeed.com/jobs?q=software+quality&l=95032',
            'next_page_selector': '//span[.={}]/..',
            'next_page_selector_type': 'xpath',
            'job_link_selector': 'a[class="jobtitle turnstileLink"]',
            'job_link_selector_type': 'css',
            'job_posting_title_selector': 'h3[class$="JobInfoHeader-title"]',
            'job_posting_title_selector_type': 'css',
            'job_posting_description_selector': 'div[class^="jobsearch-JobComponent-description"]',
            'job_posting_description_selector_type': 'css',
            'use_solitary_paging': True}
        }

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    job_posting_links = pool.map(crawl_site_for_job_links, sites.values())
    job_postings = pool.starmap(parse_job_posting_links, zip(job_posting_links, sites.values()))
    job_postings = [item for sublist in job_postings for item in sublist]
    for job in job_postings:
        print(job)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        logging.exception(exc)
        raise
