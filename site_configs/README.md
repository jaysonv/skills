## Site configuration yaml parameters
* **search_start_url**: Starting url where job postings are listed.
 Should be format string so the user can choose which job titles,
 locations, salary they're looking for.
* **next_page_selector**: A selenium selector that finds the element that will
go to the next page/expand for more results.
* **next_page_selector_type**: The type of selector to use (css, xpath etc)
* **job_link_selector**: From the job listings page, the selenium selector
that has an href/link to the individual job's page.
* **job_link_selector_type**: The type of selector to use (css, xpath etc)
* **job_posting_title_selector**: From the individual jobs description page,
the selenium selector that will point to the job's title.
* **job_posting_title_selector_type**: The type of selector to use (css, xpath etc)
* **job_posting_description_selector**: From the individual jobs description page,
the selenium selector that will point to the job's general description.
* **job_posting_description_selector_type**: The type of selector to use (css, xpath etc)
* **use_solitary_paging**: Whether or not the site uses unique sets of jobs
per page. Use true if each time you click on "more results" or a new
page number, the site shows entirely different posts than before. Use
false if the site has "expanding" behaviour.