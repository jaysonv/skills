from constants import SITE_CONFIGS_PATH, GECKODRIVER_LOG_PATH, LOGS_PATH
import logging
from functools import partial
from job_posting_link_crawler import JobPostingLinkCrawler
from job_posting_parser import JobPostingParser
import multiprocessing
from selenium import webdriver
import signal
import utility


def cleanup(driver):
    driver.quit()


def crawl_site_for_job_links(site_config):
    driver = webdriver.Firefox(service_log_path=GECKODRIVER_LOG_PATH)
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

    driver = webdriver.Firefox(service_log_path=GECKODRIVER_LOG_PATH)
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
    logger_path = f'{LOGS_PATH}/execution{utility.get_logger_date_string()}.log'
    logging.basicConfig(filename=logger_path, level=logging.INFO)

    site_configurations = utility.load_all_site_configurations(SITE_CONFIGS_PATH)
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    job_posting_links = pool.map(crawl_site_for_job_links, site_configurations.values())
    job_postings_per_site = pool.starmap(
        parse_job_posting_links, zip(job_posting_links, site_configurations.values()))
    for site_postings in job_postings_per_site:
        for job in site_postings:
            print(job)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        logging.exception(exc)
        raise
