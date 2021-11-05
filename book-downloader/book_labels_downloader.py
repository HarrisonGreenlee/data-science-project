'''
Book Labels Downloader

This program is used to download the labels associated with a book ID number.
The ID number is assumed to be in a .csv file named "books.csv", located in the current directory.
Output is a csv file similar to "books.csv", but with columns added for each desired label.
"blank" is used to denote missing/unparsed data.
'''

# external imports
import pandas as pd
import os
import regex as re
import urllib.request as req
import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep

# load headers so we actually look like a person (kinda sorta)
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

# set number of labels we want to save
numLabels = 10

# begining url for website to scrape
urlPrefix = "https://www.gutenberg.org/ebooks/"

# load a system profile, again trying to be human here
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
headers = { 'User-Agent' : user_agent }

# reads\ in the book data CSV
#  assumes the CSV is in the parent directory of the project (this can be changed)
filename = os.getcwd() + '\\books.csv'
filename = os.path.normpath(filename)
inpBookData = pd.read_csv(filename)

# create labels columns, using up to 10 labels (this can be changed)
#  using "blank" to track if a label has been found or not
for i in range(numLabels):
    inpBookData[('Label_' + str(i+1))] = 'blank'

# Subject Regex - used to find subject matches of the book
regexSubjectFinder = r"(<th>Subject</th>.*?subject/\d*\">)(.*?)(</a>)"

# use a counter to keep track of our progress
counter = 1

# iterate through the list (second column) and process each book for tags
for i in range(len(inpBookData)):

    # announce file parsing and increase counter
    print("Parsing file ", counter, " of ", len(inpBookData), ".")
    counter += 1

    # wait randomly between 1 and 5 seconds
    sleep(randint(1,5))

    # concat the current book's url together
    webFilePath = urlPrefix + str(inpBookData.iloc[i]['catalog_number'])
    
    # request the website from url
    req = requests.get(webFilePath, headers)
    webSource = str(BeautifulSoup(req.content, 'html.parser'))

    # get the list of matches based on groups
    #  this is a list of lists, with the second item in each list being the match we want
    #  access it using x[n][1]
    labelsPreList = re.findall(regexSubjectFinder, webSource, re.MULTILINE | re.DOTALL)

    # iterate and store labels, first test to make sure list is initialized with data
    if len(labelsPreList) > 0:

        # if initialized, iterate
        #  use range(len()) tos keep track of label numbers and append them to the Pandas dataframe appropriately
        for c in range(len(labelsPreList)):

            # set the current label name to match based on iteration of c
            currLabel = "Label_" + str(c+1)

            # store the book labels, access using [c][1], strip out empty spaces and new lines
            inpBookData.iloc[i, inpBookData.columns.get_loc(currLabel)] = labelsPreList[c][1].strip()

            # storing up to five labels, if c==5 then exit loop
            if c == (numLabels - 1):
                break

# save the data to an output csv file
inpBookData.to_csv("book_labels.csv", encoding='utf-8', index=False)
