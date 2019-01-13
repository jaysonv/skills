SITE_CONFIGURATIONS = {
    'indeed': {
        'search_start_url': 'https://www.indeed.com/jobs?q=software+quality&l=95032',
        'next_page_selector': '//span[.={}]/..',
        'next_page_selector_type': 'xpath',
        'job_link_selector': 'a[class="jobtitle turnstileLink"]',
        'job_link_selector_type': 'css',
        'job_posting_title_selector': 'h3[class$="JobInfoHeader-title"]',
        'job_posting_title_selector_type': 'css',
        'job_posting_description_selector': 'div[class^="jobsearch-JobComponent-description"]',
        'job_posting_description_selector_type': 'css',
        'use_solitary_paging': True
    }
}
