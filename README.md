# Job Skill Reporter
Scrapes Job Websites to help determine skill demand.
This is a personal project that I'd like to morph into something useful for the general public.

## Goals:
* User able to input job title
* User able to input job skill key words related to job title
* A report is produced that displays a summary of the skills most in demand.  This can be filtered: 
** User able to specify zip code and radius of job openings (job descriptions/ JD)
** User able to specify JD salary range
** User able to specify JD hours style (part time, full time, contract, internship)
** User able to specify JD posted within a certain number of days (desire newer JD)

## Design
* ATM there is a ton of stuff that is hard coded and needs to be generic
* There is no interface, but there should be at least command line
* The set of Job Titles is hard coded, but should be something entered by user
* The mechanism for matching Job Titles is brittle and only matches exact titles
** Should be more flexable, perhaps using RegEx or ML

** Must not use something like for job_title_specified in job_title_found.  'in' is far too generic and will return too many bad matches

