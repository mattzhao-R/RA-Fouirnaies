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
    
    if((len(edu_list)==1) & ('information on file.' in edu_list[0])):
        edu_list = np.nan
    
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
            o.append(t.string.strip())
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
    file = open(path, 'a')
    writer = csv.writer(file)
    writer.writerow(row)
    file.close()
    return

def scrape_candbio(num, fname = 'draft_cbios', write = True):
    query = make_query(num)
    wait = random.randrange(10)
    time.sleep(wait)
    
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

