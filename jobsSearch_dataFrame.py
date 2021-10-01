#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, sys, itertools, json
import pandas as pd
import workday_linkgen

CHROME_PATH     = "./selenium/chromedriver"
BAH_WORKDAY_URL = "https://bah.wd1.myworkdayjobs.com/en-US/BAH_Jobs"
TM_WORKDAY_URL = "https://trendmicro.wd3.myworkdayjobs.com/en-US/External"

url_dict = {'Booz Allen Hamilton': 'https://bah.wd1.myworkdayjobs.com/en-US/BAH_Jobs', 
            'Trend Micro'        : 'https://trendmicro.wd3.myworkdayjobs.com/en-US/External'}

def job_search(job_title):
    retStr = ""
    # Create Options to make chrome browser 'headless'
    chrome_options = Options()
    chrome_options.headless = True

    # create selenium webdriver session using google chrome, and use the options created
    # from the options object above
    driver = webdriver.Chrome(CHROME_PATH, options=chrome_options)
    
    # go to the Workday Booz Allen Hamilton page
    driver.get(BAH_WORKDAY_URL)
    #driver.get(TM_WORKDAY_URL)
    time.sleep(3)

    site_title = None
    for key in url_dict:
        if url_dict[key] == driver.current_url:
            site_title = key
            break

    job_search_str = job_title

    # search for job postings containing 'cyber security junior'
    search = driver.find_element_by_xpath('//*[@id="wd-AdvancedFacetedSearch-SearchTextBox-input"]')
    search.send_keys(job_search_str)
    search.send_keys(Keys.ENTER)

    time.sleep(4)

    # 
    body = driver.execute_script('return document.documentElement.innerHTML')
    soup = BeautifulSoup(body, 'lxml')

    '''
    # locations is founf using the css selector for every <div> tag whos "class" attribute begins with "gwt-Label"
    '''

    jobs = driver.find_elements_by_css_selector('div[class^=gwt-Label')

    '''
    # locations is found using the css selector for every <span> tag whos "class" attribute begins with "gwt-InlineLabel"

    i.e. <span class="gwt-InlineLabel WCAG WB5F" title="R0097267   |   USA, VA, Fort Belvoir (8725 John J Kingman Rd)
    |   Posted 30+ Days Ago" id="gwt-uid-2" data-automation-id="compositeSubHeaderOne">
            "R0097267   
            |   USA, VA, Fort Belvoir (8725 John J Kingman Rd)   
            |   Posted 30+ Days Ago"
    </span>
    
    '''
    
    locations = driver.find_elements_by_css_selector('span[class^=gwt-InlineLabel')

    # dictionary to store job information
    # this dictionary will end up being a nested dictionary with each unique jobID being used as the key
    # jobs_dict = {_jobID_ : {'job_title': value0, 'job_location': value1, 'job_post_date': value2}, _jobID_: {...}, ... }
    jobs_dict = {}

    for k in locations:
        line = k.text

        # condition used to check if the items in the locations list are actually what we are looking for
        if '|' not in line:
            continue
        line = line.split('|')
        j_id = line[0].strip()
        j_location = line[1].strip()
        j_post_date = line[2].strip()

        # add values into the jobs_dict dictionary 
        # the 'job_title' is filled with a temporary value I added in the for loop below
        #jobs_dict[j_id] = {'job_title': None, 'job_location': j_location, 'job_post_date': j_post_date}
        jobs_dict[j_id] = {'job_title': None, 'job_location': j_location, 'job_post_date': j_post_date, 'url': None}

    # this for loop iterates through my_dict and adds the job title each unique jobID key
    for f in jobs:
        line = f.text

        # condition used to check if the items in the locations list are actually what we are looking for
        if line.strip() == "":
            continue

        # below is where we need to check for the temporary value and if its found
        # replace it with the job title
        for c in jobs_dict:
            if jobs_dict[c]['job_title'] == None:
                jobs_dict[c]['job_title'] = line
                break
    
    #results_count = soup.find("span", {"class:", "gwt-InlineLabel WNTO WOTO"}).text
    #results_count = results_count.split()[0]
    
    results_count = soup.select("span[id$=Report_Entry]")
    results_count = results_count[0].text
    results_count = results_count.split()[0]    

    if int(results_count) == 0:
        print("NO JOBS FOUND")
        print("EXITING ...")
        driver.quit()
        sys.exit(0)

    count_jobs = 1

    #my_file = open('/Users/nicholausbrell/Desktop/jobs.txt', 'a')
    for job_id in jobs_dict.keys():
        job_title = jobs_dict[job_id]['job_title']
        job_location = jobs_dict[job_id]['job_location']
        job_post_date = jobs_dict[job_id]['job_post_date']

        link = workday_linkgen.linkGen(job_title, job_location, job_id, site_title)
        
        jobs_dict[job_id]['url'] = link
        count_jobs += 1
    
    #my_file.close()
    driver.quit()
    jobs_dict_json = json.dumps(jobs_dict, indent=4)
    #return retStr
    
    new_jobs_dict = json.dumps(jobs_dict, indent=2, default=str)
    
    df = pd.DataFrame(jobs_dict)
    
    #pd.set_option('display.max_columns', None)
    #pd.set_option('display.max_rows', None)
    #pd.set_option('display.max_colwidth', None)
    
    return df.transpose()

