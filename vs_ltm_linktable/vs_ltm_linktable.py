import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import random
import time

######################################################### INITIAL METHODS ###################################################
# these methods are drawn from the work done in the vs_ltm_linktable notebook and are not methods that end up being used

# takes in element from VoteSmart organization list and returns vs organization name,id and list of scraped organization matches 
# list takes the form of FTMname_FTMd
def scrape(in_string):
    #parsing input
    vs_id = in_string.split("/")[-2]
    vs_name = in_string.split("/")[-1]
    
    #query creation
    search_string = "+".join(vs_name.title().split("-"))
    query = 'https://www.followthemoney.org/search-results/SearchForm?Search=' + search_string
    
    #scraping table
    options = Options()
    options.binary_location = './Mozilla Firefox/firefox.exe' #r'C:\Program Files\Mozilla Firefox\firefox.exe'
    driver1 = webdriver.Firefox(executable_path='./geckodriver.exe', options=options)
    driver1.get(url)
    html = driver1.page_source
    driver1.close()
    
    #extracting info from table
    sample = BeautifulSoup(html, 'html.parser')
    query_table = sample.find_all(name='div', class_ = 'table-responsive')
    query_list = query_table[0].find_all(name='td', style = 'text-align: left;')
    
    names = []
    ids = []
    if len(query_list)==1:
        names.append(query_list[0].string)
        ids.append(row['tokenvalue'])
    
    return vs_name, vs_id, names, ids

# given an org name from VoteSmart and a scraped list of possible matches, return the most likely organization's FTM name and id
def match_org(vs_name, search_results):
    
    
    return ftm_id, ftm_name


#################################################### FINAL METHOD ###############################################
# this final method is the one that gets used in the parallelized scraping at the end of the notebook
# worker is a Chrome webdriver, data is an element of the list of votesmart organizations
def scraping(worker, data):
    #parsing input
    vs_id = data.split("/")[-2]
    temp = data.split("/")[-1]
    vs_name = " ".join(temp.lower().split("-"))
    
    #query creation
    search_string = "+".join(vs_name.title().split("-"))
    query = 'https://www.followthemoney.org/search-results/SearchForm?Search=' + search_string
    wait = random.randrange(10)
    time.sleep(wait)
    
    
    #scraping table
    worker.get(query)
    try:
        WebDriverWait(worker, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#dijit_layout_ContentPane_0 > div')))
    except:
        row = [vs_name, vs_id, "TimeoutException", "TimeoutException"]
        file = open('draft_table.csv', 'a')
        writer = csv.writer(file)
        writer.writerow(row)
        file.close()
        return
    
    html = worker.page_source
    
    #extracting info from table
    sample = BeautifulSoup(html, 'html.parser')
    query_table = sample.find_all(name='div', class_ = 'table-responsive')
    try:
        query_list = query_table[0].find_all(name='td', style = 'text-align: left;')
    except:
        row = [vs_name, vs_id, "ResultsEmpty", "ResultsEmpty"]
        file = open('draft_table.csv', 'a')
        writer = csv.writer(file)
        writer.writerow(row)
        file.close()
        return
    
    exact = []
    for query in query_list:
        if query.string.lower() == vs_name.lower():
            row = [vs_name, vs_id, query.string.title().strip(), query['tokenvalue']]
            exact.append(row)
    
    file = open('draft_table.csv', 'a')
    writer = csv.writer(file)
    if len(exact) != 0:
        for row in exact:
            writer.writerow(row)
    else:
        for x in range(0,min(10,len(query_list))):
            row = [vs_name, vs_id, query_list[x].string.title().strip(), query_list[x]['tokenvalue']]
            writer.writerow(row)
    file.close()