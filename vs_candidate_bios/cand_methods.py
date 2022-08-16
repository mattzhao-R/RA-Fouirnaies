import time
import os
import csv
import random

import requests
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

def make_query(num):
    query = 'https://justfacts.votesmart.org/candidate/biography/' + str(num)
    return query

def get_personal(cards):
    vals = cards[0].find_all(name = 'p')
    if(len(vals)==1):
        entries = vals[0].string.strip()
    else:
        entries = []
        for x in range(0,len(vals),2):
            if(x==(len(vals)-2)):
                entry = vals[x].string.strip() + vals[x+1].string.strip()
            else:
                entry = vals[x].string.strip() + vals[x+1].string.strip() + ';'
            entries.append(entry)
    
    return entries

def get_edu(edu_card):
    edus = edu_card.find_all(name = 'p')
    edu_list = []
    for edu in edus:
        try:
            edu_list.append(edu.string.strip())
        except:
            pass
    try:
        if((len(edu_list)==1) & ('information on file.' in edu_list[0])):
            edu_list = np.nan
    except:
        edu_list = "IndexError"
    
    return edu_list

def get_others(cards):
    others = []
    if(len(cards)==6):
        cards = cards[1:5]
    else:
        cards = cards[1:]

    for card in cards:
        temp = card.find_all(name = 'p')
        o = []
        for t in temp:
            try:
                o.append(t.string.strip())
            except:
                o.append('NoneTypeError')
        if((len(o)==1) & (' on file.' in o[0])):
            o = np.nan

        others.append(o)
    
    return others

def get_addl(cards):
    try:
        last = cards[5].find_all(name = 'p')
        addl = [l for l in last]
    except:
        addl = np.nan
    
    return addl

def writerow(row, path):
    file = open(path, 'a', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(row)
    file.close()
    return

def check_num(num):
    df = pd.read_csv('./draft_cbios.csv')
    num_list = df['Candidate Number'].tolist()
    return(num in num_list)

def scrape_candbio(num, fname = 'draft_cbios', write = True):
    # to prevent repeat tasks in multiprocessing, check if the candidate number already exists in dataframe
    #if(check_num(num)):
    #    return (Error tokenizing data. C error: Expected 8 fields in line 7, saw 10) skipping for now, doesn't speed up so not useful anyway
    
    query = make_query(num)
    wait = random.randrange(10)
    time.sleep(wait)
    try:
        try:
            req = requests.get(query)
        except:
            row = [num] + ['redirect error' for i in range(0,6)]

        try:
            soup = BeautifulSoup(req.content, 'html.parser')
        except:
            row = [num] + ['unknown' for i in range(0,6)]

        # checking if page is missing/empty i.e. there is no candidate with that id number
        try:
            main = soup.find(name='div', class_ = 'row text-center')
            cont = main.find(name = 'div', class_ = 'container')
            pnf = cont.find(name='h1', class_ = 'title')
            if (pnf.string == 'Page Not Found'):
                row = [num] + [np.nan for i in range(0,6)]
                if(write):
                    path = './' + fname + '.csv'
                    writerow(row,path)
                    return
                else:
                    return row
        except:
            pass

        cards = soup.find_all(name = 'div', class_ = 'card card-plain accordion-card') # all cards besides education
        edu_card = soup.find(name = 'div', class_ = 'card card-plain accordion-card accordion-header')

        row = [num, get_personal(cards), get_edu(edu_card)] + get_others(cards) + [get_addl(cards)]

        if(write):
            path = './' + fname + '.csv'
            writerow(row,path)
        else:
            return row
    except:
        print("error in:",num)
