#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 14:27:18 2021
Primary data source
https://www.kaggle.com/fedesoriano/stroke-prediction-dataset
@author: Ari
"""
#%% imports
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
#%% read data
input_folder = '/home/kali/IMports/reddit_aiml'
# list of files
file_list = os.listdir(input_folder)
# empty list to store dataframes
df_list = []

#%% read in dataframes
for file in file_list:
    print("loading", file)
    # lazy way
    # temp_df = pd.read_csv(input_folder + file)
    # fancy way
    temp_df = pd.read_csv(os.path.join(input_folder, file))
    # add the dataframe to the list
    df_list.append(temp_df)

#%% join together
# join them together
# https://stackoverflow.com/questions/32444138/concatenate-a-list-of-pandas-dataframes-together
aiml_data = pd.concat(df_list)

#%% create small sample
#aiml_data = aiml_data.sample(1000)
#%% Assignment 1-1, find which subredit is most popular, top 5
# get top 5 most frequent names
#https://stackoverflow.com/questions/48590268/pandas-get-the-most-frequent-values-of-a-column/48590361
# IT IS NEVER REQUESTED IN INSTRUCTIONS WE LIST NUMBER OF POSTS PER SUBREDDIT, JUST THE TOP 5 MOST POSTED
top_5MostPop = aiml_data['subreddit'].value_counts()[0:5]
print(top_5MostPop)
#%% Assignment 1-2, find which user posts the most
top_5UserPost = aiml_data['author'].value_counts()[0:5]
print(top_5UserPost)
#%% Assignment 1-3, which subreddit has the most distinct post authors
#https://stackoverflow.com/questions/41415017/count-unique-values-using-pandas-groupby/41415028
distinctauthors = aiml_data.groupby(by='subreddit', as_index=False).agg({'author': pd.Series.nunique})
distinctauthors = distinctauthors.sort_values('author', ascending=False)
#%% Assignment 1-4 subreddit with greatest percentages of posts with post body
#find total for each subreddit
#sources, other than me
#https://www.geeksforgeeks.org/python-pandas-isnull-and-notnull/
#https://stackoverflow.com/questions/43321455/pandas-count-null-values-in-a-groupby-function/43322220
#https://stackoverflow.com/questions/26266362/how-to-count-the-nan-values-in-a-column-in-pandas-dataframe
a = ['MachineLearning']
b = ['statistics']
c = ['datascience']
d = ['learnmachinelearning']
e = ['computerscience']
f = ['AskStatistics']
g = ['artificial']
h = ['MLQuestions']
i = ['deeplearning']
j = ['DataScienceJobs']
k = ['analytics']
l = ['computervision']
m = ['datasets']
n = ['rstats']
o = ['data']
p = ['dataengineering']
q = ['dataanalysis']
r = ['datascienceproject']
#find total number of posts per subreddit group
a1 = aiml_data.subreddit.value_counts()['MachineLearning']
b1 = aiml_data.subreddit.value_counts()['statistics']
c1 = aiml_data.subreddit.value_counts()['datascience']
d1 = aiml_data.subreddit.value_counts()['learnmachinelearning']
e1 = aiml_data.subreddit.value_counts()['computerscience']
f1 = aiml_data.subreddit.value_counts()['AskStatistics']
g1 = aiml_data.subreddit.value_counts()['artificial']
h1 = aiml_data.subreddit.value_counts()['MLQuestions']
i1 = aiml_data.subreddit.value_counts()['deeplearning']
j1 = aiml_data.subreddit.value_counts()['DataScienceJobs']
k1 = aiml_data.subreddit.value_counts()['analytics']
l1 = aiml_data.subreddit.value_counts()['computervision']
m1 = aiml_data.subreddit.value_counts()['datasets']
n1 = aiml_data.subreddit.value_counts()['rstats']
o1 = aiml_data.subreddit.value_counts()['data']
p1 = aiml_data.subreddit.value_counts()['dataengineering']
q1 = aiml_data.subreddit.value_counts()['dataanalysis']
r1 = aiml_data.subreddit.value_counts()['datascienceproject']
#find the not null values
a2 = aiml_data[aiml_data.subreddit == 'MachineLearning'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
b2 = aiml_data[aiml_data.subreddit == 'statistics'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
c2 = aiml_data[aiml_data.subreddit == 'datascience'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
d2 = aiml_data[aiml_data.subreddit == 'learnmachinelearning'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
e2 = aiml_data[aiml_data.subreddit == 'computerscience'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
f2 = aiml_data[aiml_data.subreddit == 'AskStatistics'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
g2 = aiml_data[aiml_data.subreddit == 'artificial'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
h2 = aiml_data[aiml_data.subreddit == 'MLQuestions'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
i2 = aiml_data[aiml_data.subreddit == 'deeplearning'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
j2 = aiml_data[aiml_data.subreddit == 'DataScienceJobs'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
k2 = aiml_data[aiml_data.subreddit == 'analytics'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
l2 = aiml_data[aiml_data.subreddit == 'computervision'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
m2 = aiml_data[aiml_data.subreddit == 'datasets'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
n2 = aiml_data[aiml_data.subreddit == 'rstats'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
o2 = aiml_data[aiml_data.subreddit == 'data'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
p2 = aiml_data[aiml_data.subreddit == 'dataengineering'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
q2 = aiml_data[aiml_data.subreddit == 'dataanalysis'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
r2 = aiml_data[aiml_data.subreddit == 'datascienceproject'].groupby('subreddit').agg({'post': lambda x: x.notnull().sum()})
#divide null by not null values
#https://www.geeksforgeeks.org/division-operator-in-python/
#https://www.pythoncentral.io/multiplying-dividing-numbers-python/
a3 = (a2/a1)*100
b3 = (b2/b1)*100
c3 = (c2/c1)*100
d3 = (d2/d1)*100
e3 = (e2/e1)*100
f3 = (f2/f1)*100
g3 = (g2/g1)*100
h3 = (h2/h1)*100
i3 = (i2/i1)*100
j3 = (j2/j1)*100
k3 = (k2/k1)*100
l3 = (l2/l1)*100
m3 = (m2/m1)*100
n3 = (n2/n1)*100
o3 = (o2/o1)*100
p3 = (p2/p1)*100
q3 = (q2/q1)*100
r3 = (r2/r1)*100
a4 = int(a3.post)
b4 = int(b3.post)
c4 = int(c3.post)
d4 = int(d3.post)
e4 = int(e3.post)
f4 = int(f3.post)
g4 = int(g3.post)
h4 = int(h3.post)
i4 = int(i3.post)
j4 = int(j3.post)
k4 = int(k3.post)
l4 = int(l3.post)
m4 = int(m3.post)
n4 = int(n3.post)
o4 = int(o3.post)
p4 = int(p3.post)
q4 = int(q3.post)
r4 = int(r3.post)
totalPercentages = [a4, b4, c4, d4, e4, f4, g4, h4, i4, j4, k4, l4, m4, n4, o4, p4, q4, r4]
totalPercentages2 = (a3, b3, c3, d3, e3, f3, g3, h3, i3, j3, k3, l3, m3, n3, o3, p3, q3, r3)
subredditnames = (a, b, c, d, e, f, g, h, i, j, k, m, n, l, o, p, q, r)
print (totalPercentages)
#https://www.kite.com/python/answers/how-to-convert-a-list-of-tuples-to-a-pandas-dataframe-in-python#:~:text=Use%20pandas.,convert%20data%20to%20a%20DataFrame%20.
#instead of trying to deal with sorting a tuple which seems impossible
#attempting to convert tuple to a new data frame, issue is its 3d and must be 2d
#https://www.tutorialspoint.com/adding-a-new-column-to-existing-dataframe-in-pandas-in-python
dataframeofpercent = pd.DataFrame(totalPercentages, columns = ['percentages'])
#THIS ONE WORKED, NOW NEED TO ADD A ROW CORRESPONDING SUBREDDITS
#https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
dataframeofpercent['Subreddits', 'percentages'] = subredditnames
#GREAT SUCCESS
dataframeofpercent.sort_values('percentages')
#https://www.geeksforgeeks.org/get-n-largest-values-from-a-particular-column-in-pandas-dataframe/
top5percents = dataframeofpercent.nlargest(5, ['percentages'])
print(top5percents)
#%%2-1 total number of posts across all subreddits over time
# convert author created date to human readable time
# https://stackoverflow.com/questions/19231871/convert-unix-time-to-readable-date-in-pandas-dataframe
# https://en.wikipedia.org/wiki/Unix_time
aiml_data['author_created_date'] = pd.to_datetime(aiml_data['author_created_utc'], unit='s')
aiml_data['author_created_date'].head()
aiml_data['created_date'] = pd.to_datetime(aiml_data['created_date'])
# https://stackoverflow.com/questions/30222533/create-a-day-of-week-column-in-a-pandas-dataframe-using-python
aiml_data['dow'] = aiml_data['created_date'].dt.day_name()
temp = aiml_data.groupby('dow').count()
#https://stackoverflow.com/questions/35193808/re-order-pandas-series-on-weekday
aiml_data['dow'] = pd.Categorical(aiml_data['dow'], categories=
    ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],
    ordered=True)
# https://stackoverflow.com/questions/16176996/keep-only-date-part-when-using-pandas-to-datetime
#THIS IS ASSIGNMENT 2-1
plotsovertime = aiml_data.groupby(aiml_data['created_date'].dt.date)['created_date'].count().plot()
plotsovertime.get_figure()
#%%2-2 histogram showing distribution of post scores
#variable = score
#https://stackoverflow.com/questions/12125880/changing-default-x-range-in-histogram-matplotlib
hist1 = aiml_data['score'].plot(kind='hist', logy=True)
hist1.get_figure()
#%%2-3 posts per day of week
dow_plot = aiml_data.groupby('dow')[['created_date']].count().plot(kind='bar')
dow_plot.set(xlabel="Day of Week", ylabel="Number of Posts", title="Posts by day of week")
dow_plot.get_figure()
#%% 2-4 posts per hour of the day
aiml_data['hour'] = aiml_data['created_date'].dt.hour
hod_plot = aiml_data.groupby('hour')[['created_date']].count().plot(kind='bar')
#%%3-1 which subreddit had the most new posts in the last months
#https://stackoverflow.com/questions/43090840/previous-month-datetime-pandas
#https://www.interviewqs.com/ddi-code-snippets/select-pandas-dataframe-rows-between-two-dates
#https://www.kite.com/python/answers/how-to-filter-pandas-dataframe-rows-by-date-in-python
#current date
end_date = pd.to_datetime("today")
print(end_date)
#one month prior
"""
WILL NOT SHOW ANYTHING FOR PAST MONTH DUE TO NOTHING BEING POSTED IN THE PAST MONTH
SINCE DATA HAS BEEN DOWNLOADED, HOWEVER IF MONTHS IS SET TO 2, CODE CAN BE SHOWN WORKING
"""
start_date = (end_date - pd.DateOffset(months=2))
print(start_date)
after_start_date = aiml_data["created_date"] >= start_date
before_end_date = aiml_data["created_date"] <= end_date
between_two_dates = after_start_date & before_end_date
filtered_dates = aiml_data.loc[between_two_dates]
#now find which subreddit most new posts in the last month
top_5MostPoplastmonth = filtered_dates['subreddit'].value_counts()[0:5]
print(top_5MostPoplastmonth)
#%% 3-2 Does the length of a post title correlate with score of the post?
#https://www.kite.com/python/answers/how-to-count-the-number-of-words-in-a-string-in-python
# add the lowercase conversion
#https://stackoverflow.com/questions/19410018/how-to-count-the-number-of-words-in-a-sentence-ignoring-numbers-punctuation-an
titleCount = aiml_data[['title', 'score']].copy()
count = aiml_data['title'].str.split().apply(len).reset_index()
count.rename(columns={'title': 'title_length'}, inplace = True)
titleCount['title_length'] = count['title_length']
#https://stackoverflow.com/questions/42579908/use-corr-to-get-the-correlation-between-two-columns
#Are they correlated??
correlation = titleCount['score'].corr(titleCount['title_length'])
print("Correlation is ", correlation)
#%%3-3 top 20 words in post titles
# https://stackoverflow.com/questions/46786211/counting-the-frequency-of-words-in-a-pandas-data-frame
top20words = aiml_data['title'].str.lower().str.split(expand=True).stack().value_counts()[:20]
print(top20words)
#%%top 10 most linked website domains
#https://stackoverflow.com/questions/6883049/
def find_urls(string):
    urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', str(string))
    return urls
urls = aiml_data['post'].apply(lambda x: find_urls(x))
url_list = urls.tolist() 
#https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
flat_list = [item for sublist in url_list for item in sublist]
from collections import Counter
caaa = Counter(flat_list)
top10mostcommon = caaa.most_common(10)
print(caaa.most_common(10))



















