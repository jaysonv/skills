import logging
from functools import partial
from job_posting_link_crawler import JobPostingLinkCrawler
from job_posting_parser import JobPostingParser
import multiprocessing
from selenium import webdriver
import signal
from utility import make_date_string


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
