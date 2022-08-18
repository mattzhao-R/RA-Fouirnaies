# Overview

This repo contains work which I completed as a Research Assistant for Professor Fouirnaies. It contains the inputs, scripts, notebooks, and outputs for two projects I assisted with: [(1) VoteSmart-FollowTheMoney Organization Linktable](#votesmart-followthemoney-linktable) and [(2) Scraping Candidate Biographies](#scraping-candidate-biographies). Both projects heavily involve webscraping and make use of parallelization to improve runtime (both were run on a laptop utilizing 6 out of 8 cores). 

*Note: While the final methods for both projects could be converted to and run as python scripts, I am unable to run scripts myself via terminal despite my best debugging efforts and so I have left them as final notebooks.*


## Workflow

For each project, I began with a working Jupyter Notebook that fully illustrates the work I did to complete each task, including how I created helper functions and my general thought process as I worked on these tasks. The notebooks are vs_ltm_linktable.ipynb and cand_bios.ipynb. The methods developed in these notebooks end up in Python scripts and are used by the final notebooks which contain a short chunk of code that, when run, produces the output of each project. 

*Note: For the Linktable project, chromedriver is required and you must [download](https://chromedriver.chromium.org/downloads) the version online that matches your current version of Chrome*

## TOC  
[LinkTable](#votesmart-followthemoney-linktable) | [Biographies](#scraping-candidate-biographies)
--- | --- 
[Data](#data) | [Input](#input)
[Scripts](#methods-and-parallelization-scripts) | [Scripts](#methods-script)
[Output](#linktable-output) | [Output](#biography-output)



### VoteSmart-FollowTheMoney LinkTable

The objective of this project was to create a table that would link organizations as they are named on the VoteSmart website to their corresponding name/id on the FollowTheMoney website. This was accomplished by feeding the VoteSmart organization name into  FollowTheMoney's built-in organization searcher and scraping organization names and ids from the results table. 

#### Data

I was given a file (SIG_state.csv) containing the website links for the VoteSmart organizations we wanted to match to FollowTheMoney. Each link contained the VoteSmart organization name and id. Example: AK;https://justfacts.votesmart.org/interest-group/689/alaska-state-chamber-of-commerce. 


#### Methods and Parallelization Scripts

**Method**

The final method (vs_ltm_linktable.py) for this project takes in a chromedriver worker object and VoteSmart organization website link and outputted the VoteSmart name, id, and the corresponding FollowTheMoney name(s) and id(s) scraped from the results table. It first takes in the url and parses it to create a query in FollowTheMoney. This query then goes to the worker which loads the results table (this table cannot be directly obtained using BeautifulSoup). The method then extracts the html and feeds it into BeautifulSoup where we extract the FollowTheMoney organization name(s) and id(s) and writes the row or rows into a csv (draft_table.csv). 

**Parallelization**

The parallelization script adapts a script from [wooddar's repo](https://gist.github.com/wooddar/df4c89f381fa20ce819e94782dc5bc04) to parallelize the tasks of Selenium webscraping worker objects. 

#### Linktable Output

The final output (final_draft_table.csv) contains the VoteSmart organization name and id and the corresponding FollowTheMoney name and id. For each VoteSmart organization, if the query was unsuccessful, the entries for FollowTheMoney will be "TimeoutException". If the query was successful but the results table was empty, indicating that the organization is not in FollowTheMoney's database, the entries will be "ResultsEmpty". 


### Scraping Candidate Biographies

The objective of this project was to scrape the biographical information of candidates from the VoteSmart website. This includes information such as their past positions, education, etc. An example can be found [here](https://justfacts.votesmart.org/candidate/biography/74/emil-rossi). This was accomplished by scraping the pages of these candidates using BeautifulSoup and putting each section into a csv file (draft_cbios.csv). 

#### Input

Since the candidate ids are just numbers running from 1 to approximately 210,000, we can simply create a query by feeding in a list of numbers into the method, meaning that candidate name is not required. As a result, the input is simply a list from 1 to 210,000.

#### Methods Script

The final method takes in a number and creates a query following the format for each candidate biography page. It then uses BeautifulSoup to parse the html file and extracts information from each section and places it in a list. Each of these lists is put into another list which constitutes the row that gets written to the csv. 

#### Biography Output

The final output is a csv with columns corresponding to Candidate Number, Personal, Education, Political Experience, Caucuses/Former Committees, Professional Experience, Religious, Civic, and other Memberships, and Additional Information. All the sections besides Candidate Number correspond to dropdown sections in the candidate biography website. Currently, the largest output file contains 10k candidates which took <3 hours. 
