import pathlib


JOB_TITLES = ('senior quality assurance engineer', 'senior qa engineer ii', 'quality assurance manager',
              'quality assurance engineer iv', 'senior quality assurance engineer', 'sr. director',
              'quality assurance', 'lead quality engineer', 'software quality assurance',
              'sqa', 'qa engineer', 'sdet', 'software development engineer in test', 'software test engineer',
              'software test automation', 'qa automation', 'software quality assurance engineer',
              'qa automation engineer')

PROGRAM_LANGUAGES = ('bash', 'python', 'java', 'c++', 'ruby', 'perl', 'matlab', 'javascript', 'scala',
                     'php', 'junit', 'selenium', 'react', 'c#', 'testrail', 'confluence')

ANALYSIS_SOFTWARE = ('tableau', 'd3.js', 'sas', 'spss', 'd3', 'saas', 'pandas', 'numpy', 'jenkins', 'scipy',
                     'sps', 'spotfire', 'scikits.learn', 'splunk', 'h2o', 'jira')

BIGDATA_TOOL = ('hadoop', 'mapreduce', 'spark', 'pig', 'hive', 'shark', 'oozie', 'zookeeper', 'flume', 'mahout',
                'elasticsearch')

DATABASE_LANGUAGES = ('sql', 'nosql', 'hbase', 'cassandra', 'xml', 'rust', 'mongodb', 'mysql', 'mssql', 'postgre',
                      'oracle db', 'rdbms', 'hive', 'cucumber', 'aws', 'azure', 'amazon', 'google', 'rest', 'docker',
                      'container', 'puppet', 'chef', 'kubernetes', 'storage', 'network', 'networking')

OTHER_KEYWORDS = ('restassured', 'ios', 'json', 'swift', 'objective-c', 'groovy', '.net', 'angular', 'node.js', 'kafka',
                  'mesos', 'django', 'pytest', 'css', 'html', 'appium')

KEY_WORDS = frozenset(PROGRAM_LANGUAGES + ANALYSIS_SOFTWARE + BIGDATA_TOOL + DATABASE_LANGUAGES + OTHER_KEYWORDS)

SITE_CONFIGS_PATH = pathlib.Path('../site_configs/')
LOGS_PATH = pathlib.Path('../logs/')
GECKODRIVER_LOG_PATH = pathlib.Path('../logs/geckodriver.log')
