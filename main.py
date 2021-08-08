
""" Importing all the libraries which may come in use for current file and future branching """

import regex as re
import pandas as pd
import numpy as np
import emoji
import plotly.express as px
from collections import Counter
import matplotlib.pyplot as plt
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
% matplotlib inline

""" FOLLOWING FUNCTIONS PRE-PROCESS THE DATA SO THAT ANALYSIS CAN BE CARRIED OUT"""

# This function breaks the text into date & time using regex

def StartsWithDate(s):
    pattern = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]):([0-9][0-9]) -'
    result = re.match(pattern,s)
    if result:
        return True
    return False

# This function finds out the author of every message being sent

def StartsWithAuthor(s):
   patterns = ['([\w]+):', '([\w]+[\s]+[\w]+):', '([\w]+[\s]+[\w]+[\s]+[\w]+):']
   pattern = '^' + '|'.join(patterns)
   result = re.match(pattern, s)
   if result:
       return True
   return False

# The real deal. This function gets the message from the text file

def getDataPoint(line):
    splitLine = line.split(' - ')  # splitLine = ['18/06/17, 22:47', 'Hi!! Welcome to group]
    dateTime = splitLine[0]  # dateTime = '18/06/17, 22:47'

    date, time = dateTime.split(', ')  # date = '18/06/17'; time = '22:47'

    message = ' '.join(splitLine[1:])  # message = 'Baba: Who's up for lunch?'

    if StartsWithAuthor(message):  # True
        splitMessage = message.split(': ')  # splitMessage = ['Baba', ' Who's up for lunch?']
        author = splitMessage[0]  # author = 'Baba'
        message = ' '.join(splitMessage[1:])  # message = ' Who's up for lunch?'
    else:
        author = None
    return date, time, author, message

""" MAIN STARTS FROM HERE (LINE 48) """

parsed_data = []

path = '/content/gtm.txt'   # Path of file.
with open(path, encoding="utf-8") as f:
    f.readline()
    buffer = []
    date, time, author = None, None, None
    while True:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        if StartsWithDate(line):
            if len(buffer)>0:
                parsed_data.append([date, time, author, ' '.join(buffer)])
            buffer.clear()
            date, time, author, message = getDataPoint(line)
            buffer.append(message)
        else:
            buffer.append(line)

""" THE DATA NOW IS READY TO BE PROCESSED.

FOLLOWING LINES WOULD MAKE DATA FRAME AND START ANALYSIS AND PLOTTING ON IT. """

#  Making a pandas data frame
df = pd.DataFrame(parsed_data, columns=['Date', 'Time', 'Author', 'Message'])
df.head(10)

df.describe()

# MOST TALKATIVE MEMBERS 
author_value_counts = df['Author'].value_counts()
top_3_author = author_value_counts.head(3)
top_3_author.plot.barh();

# PEOPLE WHO SEND MOST MEDIA (INCREASING ORDERS)

media_df = df[df['Message'] == '<Media omitted>']
media_count = media_df['Author'].value_counts()
top_3_media = media_count.head(3)
top_3_media.plot.barh();

# NO.OF LETTERS AND WORDS BY EACH MEMBER 

df['Letter Count'] = df['Message'].apply(lambda s: len(s))
df['Word Count'] = df['Message'].apply(lambda s: len(s.split(' ')))
print(df)

# FINDING DISCRETE AND CONITNOUS DATA

discrete_columns = [['Date', 'Time', 'Author', 'Message']]
df[discrete_columns].describe()
continous_columns = [['Letter Count', 'Word Count']]
df[continous_columns].describe()

# MOST COMMON WORDS

plt.figure(figsize=(15, 2))
common_words = df['Word Count'].value_counts()
top_10_used = common_words.head(10)
top_10_used.plot.bar()
plt.xlabel('Word Count')
plt.ylabel('Frequency')

# DAYS ON WHICH MOST MESSAGES WERE SENT.

df['Date'].value_counts().head(5).plot.barh();
plt.xlabel('Number of Messages');
plt.ylabel('Date');


df['Time'].value_counts().head(5).plot.barh()
plt.xlabel('Total Messages')
plt.ylabel('Time')
