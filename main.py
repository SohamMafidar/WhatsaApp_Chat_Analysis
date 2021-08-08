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

def StartsWithDate(s):
    pattern = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]):([0-9][0-9]) -'
    result = re.match(pattern,s)
    if result:
        return True
    return False

def StartsWithAuthor(s):
   patterns = ['([\w]+):', '([\w]+[\s]+[\w]+):', '([\w]+[\s]+[\w]+[\s]+[\w]+):']
   pattern = '^' + '|'.join(patterns)
   result = re.match(pattern, s)
   if result:
       return True
   return False


def getDataPoint(line):
    splitLine = line.split(' - ')  # splitLine = ['18/06/17, 22:47', 'Loki: Why do you have 2 numbers, Banner?']

    dateTime = splitLine[0]  # dateTime = '18/06/17, 22:47'

    date, time = dateTime.split(', ')  # date = '18/06/17'; time = '22:47'

    message = ' '.join(splitLine[1:])  # message = 'Loki: Why do you have 2 numbers, Banner?'

    if StartsWithAuthor(message):  # True
        splitMessage = message.split(': ')  # splitMessage = ['Loki', 'Why do you have 2 numbers, Banner?']
        author = splitMessage[0]  # author = 'Loki'
        message = ' '.join(splitMessage[1:])  # message = 'Why do you have 2 numbers, Banner?'
    else:
        author = None
    return date, time, author, message


parsed_data = []
path = '/content/gtm.txt'
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

#  Making a pandas data frame
df = pd.DataFrame(parsed_data, columns=['Date', 'Time', 'Author', 'Message'])
df.head(10)

df.describe()

author_value_counts = df['Author'].value_counts()
top_3_author = author_value_counts.head(3)
top_3_author.plot.barh();

media_df = df[df['Message'] == '<Media omitted>']
media_count = media_df['Author'].value_counts()
top_3_media = media_count.head(3)
top_3_media.plot.barh();


df['Letter Count'] = df['Message'].apply(lambda s: len(s))
df['Word Count'] = df['Message'].apply(lambda s: len(s.split(' ')))
print(df)

discrete_columns = [['Date', 'Time', 'Author', 'Message']]
df[discrete_columns].describe()
continous_columns = [['Letter Count', 'Word Count']]
df[continous_columns].describe()

plt.figure(figsize=(15, 2))
common_words = df['Word Count'].value_counts()
top_10_used = common_words.head(10)
top_10_used.plot.bar()
plt.xlabel('Word Count')
plt.ylabel('Frequency')


df['Date'].value_counts().head(5).plot.barh();
plt.xlabel('Number of Messages');
plt.ylabel('Date');


df['Time'].value_counts().head(5).plot.barh()
plt.xlabel('Total Messages')
plt.ylabel('Time')