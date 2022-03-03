#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 12:59:21 2021

@author: Ari
"""

#%% imports

import re
import pandas as pd
from datetime import datetime
import numpy as np
import datetime
import nltk
from pandas.tseries.offsets import DateOffset
import string
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from collections import defaultdict
from collections import Counter
import string
import sys
from nltk.corpus import words 
nltk.download('words')
#%% read data file

# create empty list for the logs
raw_log = []

# open the file and then read the lines

with open('/home/kali/IMports/hackers.txt', 'r+', errors='ignore') as f:
    raw_log = f.readlines()
    
    
#%% define functions

def is_comment_row(row):
    """
    find rows that start with ---
   
    These rows can tell us when the day has changed 
    Parameters
    ----------
    row : str
        Row from our dataset.
    Returns
    -------
    True/False.
    """
    
    is_comment = re.match('---', row[0:5])
    
    return is_comment
    
def has_joined(row):
    """
    Check to see if a row is a regular chat message.
    Parameters
    ----------
    row : TYPE
        DESCRIPTION.
    Returns
    -------
    True/False.
    """
    
    is_joining = re.search('has joined', row)
    if is_joining:
        return True
    else:
        return False

def has_quit(row):
    """
    Check to see if a row is a regular chat message.
    Parameters
    ----------
    row : TYPE
        DESCRIPTION.
    Returns
    -------
    True/False.
    """
    
    is_quitting = re.search('has quit', row)
    if is_quitting:
        return True
    else:
        return False    


def is_time_row(row):
    """
    Check if a row starts with HH:MM format
    Parameters
    ----------
    row : str
        Row from our dataset.
    Returns
    -------
    True/False.
    """
    
    is_time = re.search('[0-9]{2}:[0-9]{2}', row[:5])
    
    if is_time:
        return True
    else:
        return False  



def is_message_row(row):
    """
    Check to see if a row is a regular chat message.
    Parameters
    ----------
    row : TYPE
        DESCRIPTION.
    Returns
    -------
    True/False.
    """
    
    is_message = re.search('<', row[6:7])
    if is_message:
        return True
    else:
        return False

def is_change_in_day(row):
    """
    Check to see if a row is a regular chat message.
    Parameters
    ----------
    row : TYPE
        DESCRIPTION.
    Returns
    -------
    True/False.
    """
    
    change_in_day = re.search('--- Day changed', row)
    if change_in_day:
        return True
    else:
        return False
    
def is_url_in_code(row):
    """
    Check to see if a row is a regular chat message.
    Parameters
    ----------
    row : TYPE
        DESCRIPTION.
    Returns
    -------
    True/False.
    """
    
    urlfound = re.search('https?://', row)
    if urlfound:
        return True
    else:
        return False
    
    
def is_dw_url(row):
    """
    Check to see if a row is a regular chat message.
    Parameters
    ----------
    row : TYPE
        DESCRIPTION.
    Returns
    -------
    True/False.
    """
    
    DW_urlfound = re.search('\.onion/', row)
    if DW_urlfound:
        return True
    else:
        return False
    

def extract_username(row):
    """
    Assume values passed to this function have already
    been checked if it is a chat message.
    
    Extract the name of the user who posted the chat message
    and return that name.
    Parameters
    ----------
    row : TYPE
        DESCRIPTION.
    Returns
    -------
    a username.
    """
    
    #print(row)
    
    username = re.search(r'<.(\w+)>', row)
    
    #print(username, username)
    
    """
    if we allow any data in that is not clean, hide the errors
    using a try catch, or avoid them entirely by using and if statement
    much like the is_message function
    """
    if username:
        return username.group(1)
    else:
        return None
    
def extract_username_joined(row):
    """
    Assume values passed to this function have already
    been checked if it is a chat message.
    
    Extract the name of the user who posted the chat message
    and return that name.
    Parameters
    ----------
    row : TYPE
        DESCRIPTION.
    Returns
    -------
    a username.
    """
    
    #print(row)
    
    usernamej = re.search(r'\[(\w+)@', row)
    
    #print(username, username)
    
    """
    if we allow any data in that is not clean, hide the errors
    using a try catch, or avoid them entirely by using and if statement
    much like the is_message function
    """
    if usernamej:
        return usernamej.group(1)
    else:
        return None

def extract_URL(row):
#https://codereview.stackexchange.com/questions/249329/finding-the-most-frequent-words-in-pandas-dataframe
#https://www.geeksforgeeks.org/python-check-url-string/
    
    #print(row)
    regex = r"(https?://\S+|www\.\S+')"
    url = re.findall(regex, row)      
    return url

    

def get_time(row):
    """
    This function looks at the start of the row
    and finds the time. It returns the time in HH:MM format.
    Parameters
    ----------
    row : str
        DESCRIPTION.
    Returns
    -------
    The time in the format of HH:MM.
    """
    
    
    time = re.search('[0-9]{2}:[0-9]{2}', row)
    if time:
        return time.group(0)
    else:
        return None
    
def get_hour(row):
    """
    This function looks at the start of the row
    and finds the time. It returns the time in HH:MM format.
    Parameters
    ----------
    row : str
        DESCRIPTION.
    Returns
    -------
    The time in the format of HH:MM.
    """
    
    
    hour = re.search('[0-9]{2}', row)
    if hour:
        return hour.group(0)
    else:
        return None

def get_date(row):
    """
    
    Parameters
    ----------
    row : TYPE
        DESCRIPTION.
    Returns
    -------
    The date in 'YYYY-MM-DD' format.
    """
    
    #  remove this line when done
    row = '--- Log opened Tue Sep 20 00:01:49 2016'
    
    # split on spaces and inspect the parts
    date_parts = row.split()
    
    # join this into a single string
    formatted_date = "-".join([date_parts[7], date_parts[4], date_parts[5]])
    
    # convert from string to datetime format
    dt_date = datetime.datetime.strptime(formatted_date, '%Y-%b-%d')
    
    return dt_date
    

def find_non_english_words(word_counts):
    """
    Pass a dictionary with 'word': count format. 
    Check the words in the dictionary against the list
    of words in NLTK English corpus.
    
    Return a dictionary with only the keys for non-English words, 
    with the count for each word. 
    
    
    The solution is based on this answer-
    https://stackoverflow.com/questions/3420122/filter-dict-to-contain-only-certain-keys
    
    Parameters
    ----------
    word_counts : dict
        dictionary with unique words as keys, and their counts as 
        values.
    Returns
    -------
    dictionary with non-English words and their counts.
    """
    
    
    # things we need-
    # list of English
    # a way to filter out those words 
    
    word_list = set(words.words())
    
    # create the list of non English words
    non_english_keys = set(word_counts.keys()) - (word_list)
    
    # filter them into a new dictionary
    non_english_counts = { your_key: word_counts[your_key] for your_key in non_english_keys }

    return non_english_counts

#%% find rows that start with comments

time_rows = []
message_rows = []
bad_row_list = []

for row in raw_log:
    # print(row)
    
    if is_comment_row(row):
        # print('found comment row', row)
        pass
    
    elif is_message_row(row):
        message_rows.append(row)
        
        # could add an if statement and then call extract_ussernames
        
    # next, check for rows that start with the time in HH:MM format
    
    elif is_time_row(row):
        # print('found time row')
        
        time_rows.append(row)
    
    
    else:
        
        unformatted = ("row did not meet any format", row)
        bad_row_list.append(row)
        

#%% use a dataframe instead of a for loop

# create the dataframe

hacker_log = pd.DataFrame(raw_log, columns=['raw_log'])
#hacker_log = hacker_log.sample(1000)

hacker_log['is_message'] = hacker_log['raw_log'].apply(is_message_row)

#print(hacker_log)


# create a separate dataframe for chat rows
chat_rows = hacker_log.loc[hacker_log['is_message'] == True].copy()

chat_rows['username'] = chat_rows['raw_log'].apply(extract_username)
#%% Filtering out posts from evilbot

#https://stackoverflow.com/questions/19960077/how-to-filter-pandas-dataframe-using-in-and-not-in-like-in-sql

filtered_names = ['evilbot', ' '] 

#this command filters out a certain value, by adding "~" it filters out everything but a given value
# selecting rows based on condition 

chat_rows = chat_rows.loc[~chat_rows['username'].isin(filtered_names)]


#%% 1-1 Find the user with the most messages

#https://stackoverflow.com/questions/48590268/pandas-get-the-most-frequent-values-of-a-column
#Chat rows = messages, find most common username in chat rows
#wants top 5
n = 5
# sort values
T5MM = chat_rows['username'].value_counts()[:n].sort_values(ascending=False)

print ("1-1 The 5 users with the mosts posts are:\n", T5MM)

#%% 1-2 Which user logged in the most times

#Step 1, create a true false column in hacker column whether or not its a joining
hacker_log['has_joined'] = hacker_log['raw_log'].apply(has_joined)

#Step 2 apply to chat_rows
join_rows = hacker_log.loc[hacker_log['has_joined'] == True].copy()

join_rows['username'] = join_rows['raw_log'].apply(extract_username_joined)

#Step 3, find the 5 most common
#N = 5 still from last question

# sort values
T5UJ = join_rows['username'].value_counts()[:n].sort_values(ascending=False)

print ("1-2 The 5 users who joined the most are:\n", T5UJ)



#%% 2-1 Count the total number of written messages

#chat_rows are all message rows
TWM = chat_rows['raw_log'].count()
print ('2-1 Total number of written messages are: ', TWM)

#%% 2-2 Most common words

#https://codereview.stackexchange.com/questions/249329/finding-the-most-frequent-words-in-pandas-dataframe

stop_words = stopwords.words()

def cleaning(text):        
    # converting to lowercase, removing URL links, special characters, punctuations...
    text = text.lower()
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('[’“”…]', '', text)     

    # removing the stop-words          
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in stop_words]
    filtered_sentence = (" ").join(tokens_without_sw)
    text = filtered_sentence
    
    return text

dt = chat_rows['raw_log'].apply(cleaning)

p = Counter(" ".join(dt).split()).most_common(10)
T5MCW = pd.DataFrame(p, columns=['Word', 'Frequency'])
print('2-2 Most common words are \n', T5MCW)

#%%2-3 Find and rank words not in the english dictionary

#Stop words are words not in the english dictionary from previous code
#https://stackoverflow.com/questions/3594514/how-to-find-most-common-elements-of-a-list
tnews = [item for item in Counter(stop_words).most_common()]
print ('2-3 The most common words not in the english dictionary are \n', tnews[:10])

#%% 2-4 Find URLS and count how many are distinct
def find_urls(string):
    urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', str(string))
    return urls
urls = hacker_log['raw_log'].apply(lambda x: find_urls(x))
url_list = urls.tolist() 
#https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
flat_list = [item for sublist in url_list for item in sublist]
caaa = Counter(flat_list)
#Find number of urls that are distinct, begin by turning list into tuple

#https://www.geeksforgeeks.org/python-convert-a-list-into-a-tuple/
def convert(list):
    return tuple(list)
  
#Driver function
list_urls = (convert(flat_list))
l1 = []
count = 0
for item in list_urls:
    if item not in l1:
        count+= 1
        l1.append(item)
print ('2-4 The number of unique URLS is: ', count)

#%% 2-5
top10mostcommonurls = caaa.most_common(5)
print('2-5 The five most commonly posted URLS are:')
for top in top10mostcommonurls:
    print (top)

#%% 2-6 Generate a list of darkweb sites, ending in .onion
#use function created above to make true/false if containing dark web(dw) link
hacker_log['contains_DW_URL'] = hacker_log['raw_log'].apply(is_dw_url)
#create a new list only containing dw linked posts
dw_links = hacker_log.loc[hacker_log['contains_DW_URL'] == True].copy()
#Source in previous reference to same code
def find_dwurls(string):
    dwurls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+.onion', str(string))
    return dwurls
dwurls = dw_links['raw_log'].apply(lambda x: find_dwurls(x))
wurl_list = (convert(dwurls))
dw_list = [item for sublist in wurl_list for item in sublist]
print ('2-6 The following sites are links to the darkweb extracted from messages: ')
for elem in dw_list:
    print (elem)
#%% 3-1 Which hours had the most messages

chat_rows['HH:MM'] = chat_rows['raw_log'].apply(get_time)
chat_rows['HH'] = chat_rows['raw_log'].apply(get_hour)
proportionoH = chat_rows['HH'].groupby(chat_rows['HH']).count()
sortedprop = proportionoH.sort_values(ascending=False)
print('3-1 The hours with the most messages are : \n', sortedprop)
