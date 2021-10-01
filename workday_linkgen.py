import re
"""
========== Booz Allen Hamilton ==========
https://bah.wd1.myworkdayjobs.com/en-US/BAH_Jobs/job/USA-DC-Washington-1000-Independence-Ave-SW/Information-Systems-Security-Officer--Junior_R0102774
https://bah.wd1.myworkdayjobs.com/en-US/BAH_Jobs/job/USA-TX-San-Antonio-3133-General-Hudnell-Dr/Cyber-Network-Engineer--Junior_R0097661

========== Trend Micro ==========
https://trendmicro.wd3.myworkdayjobs.com/en-US/External/job/San-Jose/Cloud-Security-Architect_R0000907
"""

url_dict = {'Booz Allen Hamilton': 'https://bah.wd1.myworkdayjobs.com/en-US/BAH_Jobs/job/', 
            'Trend Micro'        : 'https://trendmicro.wd3.myworkdayjobs.com/en-US/External/job/'}
            
def replaceNonAlpha(my_str, flag=False):
    if '(' in my_str and ')' in my_str:
        my_str = my_str.replace('(', ',')
        my_str = my_str.replace(')', '')

    if flag:
        my_str = my_str.replace(',', ' ')
    else:    
        my_str = my_str.replace(',', '')
    my_str = my_str.replace(' ', '-')

    return my_str


def linkGen(job_title, job_location, job_id, site_title):
    link = ''
    #link_start = 'https://bah.wd1.myworkdayjobs.com/en-US/BAH_Jobs/job/'
    link_start = ''
    for key in url_dict:
        if key == site_title:
            link_start = url_dict[key]
    link += link_start
    
    #job_location = replaceNonAlpha(job_location)
    link += replaceNonAlpha(job_location) + '/'

    link += replaceNonAlpha(job_title, True) + '_'
    link += job_id
    return link
    



title = 'Information Systems Security Officer, Junior'
loc   = 'USA, DC, Washington (1000 Independence Ave SW)'
j_id  = 'R0102774'

"""
2. Information Systems Security Officer, Junior
        JobID   : R0102774
        Location: USA, DC, Washington (1000 Independence Ave SW)
        Date    : Posted 30+ Days Ago
"""

