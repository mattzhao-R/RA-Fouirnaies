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

########################################################## SUB METHODS ##########################################################
# components of the final method(s)

# takes in an input from SIG_state list of votesmart orgs and returns a query for scraping
def make_query(vs_address):
    #parsing input
    vs_id = data.split("/")[-2]
    temp = data.split("/")[-1]
    vs_name = " ".join(temp.lower().split("-"))
    
    #query creation
    search_string = "+".join(vs_name.title().split("-"))
    query = 'https://www.followthemoney.org/search-results/SearchForm?Search=' + search_string
    return query

######################################################### FINAL METHOD #########################################################
# scraping is used in conjuction with parallel to generate a link table (each iteration of scraping creates one row of the table)
# worker is a Chrome webdriver, data is an element of the list of votesmart organizations
def scraping(worker, data):
    # query creation
    query = make_query(data)

    # random wait to avoid site checks
    wait = random.randrange(10)
    time.sleep(wait)
    
    #scraping table
    worker.get(query)
    try:
        WebDriverWait(worker, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#dijit_layout_ContentPane_0 > div')))
    except:
        try:
            time.sleep(60)
            WebDriverWait(worker, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#dijit_layout_ContentPane_0 > div')))
        except:
            row = [data, vs_name, vs_id, "TimeoutException", "TimeoutException"]
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
        row = [data, vs_name, vs_id, "ResultsEmpty", "ResultsEmpty"]
        file = open('draft_table.csv', 'a')
        writer = csv.writer(file)
        writer.writerow(row)
        file.close()
        return
    
    exact = []
    for query in query_list:
        if query.string.lower() == vs_name.lower():
            row = [data, vs_name, vs_id, query.string.title().strip(), query['tokenvalue']]
            exact.append(row)
    
    file = open('draft_table.csv', 'a')
    writer = csv.writer(file)
    if len(exact) != 0:
        for row in exact:
            writer.writerow(row)
    else:
        for x in query_list:
            row = [data, vs_name, vs_id, x.string.title().strip(), x['tokenvalue']]
            writer.writerow(row)
    file.close()