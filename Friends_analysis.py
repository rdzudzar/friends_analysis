#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Run this in Python once, it should take effect permanently
from notebook.services.config import ConfigManager
c = ConfigManager()
c.update('notebook', {"CodeCell": {"cm_config": {"autoCloseBrackets": False}}})


# In[2]:


#Imports
import os
from os import path
import functools
import operator

import re
from collections import Counter
import glob

# Imports url
import urllib.request
from bs4 import BeautifulSoup
import html2text

#Wordcloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np

#Plot
import matplotlib.pyplot as plt

#Pandas
import pandas as pd


# ## Read in the html page of the Friends episode transcripts

# In[3]:


path = './season/'
filename = '0101.html'

def open_html(filename_html):
    '''
    Import html screenplay file.
    
    Parameters:
    ----------
    filename_html - String. File name.
    
    Return:
    ------
    File.
    
    '''
    
    filename = path+filename_html
    
    f = open(filename, 'r').read()
    #print(f)
    return f

#filename = './season/0101.html'
#f = open(filename, "r").read()
#print(f)


# In[4]:


f = open_html(filename)


# ## Get entire season

# In[5]:


def all_episodes(path, season):
    '''
    Creates a html list with all the episodes in a season.
    
    Parameters:
    ----------
    path - String. Path to a season.
    season - String. Conins characters to recognize a season. For example: '01*.html' will give all episodes in the first season.

    Returns:
    -------
    all_episodes_in_a_season - A list containing all html data for each episode in a season.
    '''
    
    list_of_episodes = glob.glob(path+season)
    
    all_episodes_in_a_season = []
    for episode in list_of_episodes:
        f = open(episode, 'r').read()
        all_episodes_in_a_season.append(f)
        
    return all_episodes_in_a_season


# In[6]:


first_season = '01*.html'
first_season_episodes = all_episodes(path, first_season)


# In[7]:


print(len(first_season_episodes))


# ## Convert html into readable text using html2text

# In[8]:


def convert_html_to_text(file):
    '''
    Convert html file into text file. 
    
    Parameters:
    ----------
    file - Html file. 
    
    Return:
    ------
    episode - txt file, converted from html.
    '''
    
    h = html2text.HTML2Text()
    # Ignore converting links from HTML
    h.ignore_links = True
    print(h.handle(file))
    episode = h.handle(file)
    return episode


# In[9]:


first_episode = convert_html_to_text(f)


# ## Get txt for all episodes in a season

# In[12]:


def convert_season_html_to_text(all_episodes_in_a_season):
    '''
    Convert html file into text file. 
    
    Parameters:
    ----------
    all_episodes_in_a_season - A list containing all html data for each episode in a season/
    
    Return:
    ------
    all_episodes_in_a_season_txt - A list of all episodes in a season as txt file, converted from html.
    '''
    
    h = html2text.HTML2Text()
    # Ignore converting links from HTML
    h.ignore_links = True
    #print(h.handle(file))
    
    all_episodes_in_a_season_txt = []
    for episode in all_episodes_in_a_season: 
        all_episodes = h.handle(episode)
        all_episodes_in_a_season_txt.append(all_episodes)
    return all_episodes_in_a_season_txt


# In[38]:


all_episodes_in_a_season_txt = convert_season_html_to_text(first_season_episodes)


# In[73]:


print(len(all_episodes_in_a_season_txt))

print(all_episodes_in_a_season_txt[18])


# # WordCloud

# In[15]:


def add_stopwords_to_wordcloud(stop_friends_on_off):
    '''
    Set on and off stopwords - whether to use Friends names or not. If 'True' it will add Friends names to stopwords.
    
    Parameters:
    ----------
    stop_friends_on_off - True/False statement.
    
    Return:
    ------
    stopwords - list of the used stopwords.
    '''
    
    stopwords = set(STOPWORDS) #set(STOPWORDS) for default exclusion
    
    stopwords.add("Scene")
    print(stopwords)
    # Need to add stopwords for Frinds if I don't want to show their names
    stop_friends = stop_friends_on_off

    if stop_friends == True:
        stopwords.add("Monica")
        stopwords.add("Rachel")
        stopwords.add("Ross")
        stopwords.add("Phoebe")
        stopwords.add("Chandler")
        stopwords.add("Joey")
        print('Friends names will be excluded.')
    else:
        print('Firends names will be included.')

    return stopwords


# In[17]:


stopwords = add_stopwords_to_wordcloud(True);


# In[18]:


max_font_size = 100
min_font_size = 20
bck_color = 'white'
#width = 500
#height = 300
width=1600
height=800
colourmap = plt.cm.cividis_r
relative_scaling = 1 # relative scaling sets how to adjust the font sizes based on frequency
                    # relative_scaling == 1.0 means frequency dictates font-size -> Hides low-frequency words
                    # relative_scaling == 0.0 means rank dictates the relative font-size -> hides how frequently a word might appear

collocations = False # if true, it will group phrases; if false it will take single words

def generate_wordcloud_bilinear(episode, max_font_size ):
    '''
    Make a wordcloud based on the episode. Use bilinear interpolation and max font size.
    
    Parametes:
    ---------
    episode - txt of the loaded episode.
    font_size - Integer. Maximum font size used on the image.
    
    Return:
    ------
    Makes a wordcloud and plots it.
    '''
    
    # lower max_font_size
    wordcloud = WordCloud(width=width, height=height, background_color=bck_color, 
                          min_font_size=min_font_size, stopwords=stopwords, colormap = colourmap,
                         relative_scaling=relative_scaling, collocations=collocations).generate(episode)
    
    
    plt.figure(figsize=(15,15))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    # The pil way (if you don't have matplotlib)
    # image = wordcloud.to_image()
    # image.show()


# In[19]:


generate_wordcloud_bilinear(first_episode, max_font_size)


# ## WordCloud for each episode in a season

# In[21]:


#for each_ep in np.arange(0, len(all_episodes_in_a_season_txt), 1):
#    generate_wordcloud_bilinear(all_episodes_in_a_season_txt[each_ep], max_font_size)


# ## WordCloud with a mask

# In[22]:


mask_image = 'friends_couch.jpg'

def generate_wordcloud_with_mask(mask_image, episode):
    '''
    Make a wordcloud using image as a mask.
    
    Parameters:
    ----------
    mask_image - Image. Used as a mask.
    episode - txt file. 
    
    Return:
    ------
    Saves wordcloud figure and plots the output.
    '''

    friends_mask = np.array(Image.open(mask_image))

    wc = WordCloud(width=width, height=height, background_color="white", max_words=2000, mask=friends_mask,
               stopwords=stopwords, contour_width=2, min_font_size=min_font_size, contour_color='grey', 
                  colormap = colourmap).generate(episode)

    # store to file
    wc.to_file("F.png")
    # show
    plt.figure(figsize=(20,20))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")

    plt.show()
    return


# In[23]:


generate_wordcloud_with_mask(mask_image, first_episode)


# # A Friend lines

# In[93]:


#friend_name = '**Monica:**'
#friend_name = '**Rachel:**'
#friend_name = '**Ross:**'
#friend_name = '**Joey:**'
friend_name = '**Phoebe:**'
#friend_name = '**Chandler:**'

def get_friend_line(friend_name, episode):
    '''
    Get the lines of a friend in an episode. These lines can include (one_friend) or exclude (one_friend_clear) the scene description.
    
    Parameters:
    ----------
    friend_name - Modified string of a friend nema; e.g. if you want Monica, you type: '**Monica:**'
    episode - .txt file, converted from html in a function convert_html_to_text.

    Return:
    ------

    one_friend - Strings. Contain all lines of a friend.
    one_friend_clear - Strings. Contain all lines of a friend withoud scene description.
        
    '''
    # Import episode into the testfile.txt
    file_episode = open('testfile.txt','w', encoding='utf-8') 
    file_episode.write(episode) 
    
    # Search friend lines
    searchquery = friend_name
    # From the episode file (testfile) read and write all friend lines into test_friend file.
    with open('testfile.txt', encoding='utf-8') as f1:
        with open('test_friend.txt', 'w', encoding='utf-8') as f2:
            lines = f1.readlines()
            for i, line in enumerate(lines):
                # Add lines that starts with searcquery
                if line.startswith(searchquery):
                    f2.write(line)
                    
                    #Sometimes there are multiple lines, but not all starts with searchquer
                    #Add them to the list if they dont start with ** because that would mean different Friend is speaking                       
                    if not lines[i+1].startswith('**'):
                        f2.write(lines[i+1])
                    
                        # Need to check several levels whether it is true or not
                        if not lines[i+2].startswith('**'):
                            f2.write(lines[i+2])
                            
                            if not lines[i+3].startswith('**'):
                                f2.write(lines[i+3])
                                
                                if not lines[i+4].startswith('**'):
                                    f2.write(lines[i+4])
                                    
                                    if not lines[i+5].startswith('**'):
                                        f2.write(lines[i+5])
                                        
                
    file = open('test_friend.txt', 'r',encoding='utf-8') 
    one_friend = file.read();
    
    # Remove text within [] and () brackets. These lines are scene description.
    one_friend_tmp = re.sub( "\[[^\]]*\]", "", one_friend) # Removes []
    one_friend_clear = re.sub('\([^)]*\)', "",one_friend_tmp) # Removes ()
    
    return one_friend, one_friend_clear


# In[ ]:





# In[94]:


phoebe, phoebe_clear = get_friend_line(friend_name, first_episode)
#print(phoebe_clear)


# In[95]:


phoebe_s = []
phoebe_clear_s = []

for each_ep in np.arange(0, len(all_episodes_in_a_season_txt), 1):
    phoebe_tmp, phoebe_clear_tmp = get_friend_line(friend_name, all_episodes_in_a_season_txt[each_ep])
    
    phoebe_s.append(phoebe_tmp)
    phoebe_clear_s.append(phoebe_clear_tmp)


# In[101]:


# DIFFERENT FORMATING FOR THE EPISODE
print(phoebe_clear_s[15]) 


# ## WordCloud

# In[54]:


generate_wordcloud_bilinear(phoebe_clear, max_font_size)


# ## WordCloud per season per Friend

# In[99]:


for each_ep in np.arange(0, len(phoebe_clear_s), 1):
    try:
        generate_wordcloud_bilinear(phoebe_clear_s[each_ep],  max_font_size)
    
    # I'm raising value error because s01e16 is formated differently, thus text for a friend is not detected at the moment
    except ValueError:
        pass
        print('There is an error in episode {0}'.format(each_ep+1))
    


# ## Count words and plot frequency

# In[201]:



# If I want entire season I need to remove nested list
#phoebe_clear_season = functools.reduce(operator.concat, phoebe_clear_s)

#print(flat_list)

words = []

for i in np.arange(0, len(phoebe_clear_s), 1):
# Use Counter to count the words; It will be dictionary
    words_count = Counter(map(str.lower, phoebe_clear_s[i].split()))
    words.append(words_count)

dataframe = []
for i in np.arange(0, len(words), 1):
    
    # Convert counted words into pandas dataframe
    df = pd.DataFrame.from_dict(words[i], orient='index').reset_index()
    dataframe.append(df)

    
print(dataframe)


# In[259]:


i_count = []

for i in np.arange(0, len(dataframe), 1):

    try:
    
        letter_i = dataframe[i][0] [dataframe[i]['index']=='i']
        i_count.append(letter_i.values)

    except KeyError:
        pass
        print('No value at position {0}'.format(i+1))


# In[288]:


print(i_count)
print(len(i_count))


# In[ ]:





# In[138]:



# If I want entire season I need to remove nested list
phoebe_clear_season = functools.reduce(operator.concat, phoebe_clear_s)

#print(flat_list)

# Use Counter to count the words; It will be dictionary
words_count = Counter(map(str.lower, phoebe_clear_season.split()))

# Convert counted words into pandas dataframe
df = pd.DataFrame.from_dict(words_count, orient='index').reset_index()

# Rename colums
df = df.rename(columns={'index':'word', 0:'count'})

# Sort by the 'count' values, highest first
df = df.sort_values(['count'], ascending=[False])

df.head()


# In[139]:


print(np.asarray(df['word']))


# In[140]:


first_x_words = 15

fig, ax = plt.subplots(1, figsize=(15,10))

#plt.figure(figsize=(10,10))
plt.bar(df['word'][0:first_x_words], df['count'][0:first_x_words], color='lightgrey', edgecolor='k')

ax.tick_params(axis='both', which='major', labelsize=16)

plt.xlabel('Words', fontsize=24)
plt.ylabel('Count', fontsize=22)


for bar in ax.patches:
    height = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2.,
            height + 0.2,
            '{:1.2f}'.format(height),
            ha="center",fontsize=18) 


# # Count 'I' per season per person

# In[353]:


A = np.arange(1, len(i_count)+1, 1)
i_values = []

for i in np.arange(0, len(i_count), 1):
    try:
        value = i_count[i][0]
        i_values.append(value)
    except IndexError:
        i_values.append(0)
        
fig, ax = plt.subplots(1, figsize=(15,10))

#plt.figure(figsize=(10,10))
plt.bar(A, i_values, color='lightgrey', edgecolor='k', label='Phoebe')

ax.tick_params(axis='both', which='major', labelsize=16)

plt.xlabel('Episode', fontsize=24)
plt.ylabel('\' I \' [counts]', fontsize=22)
plt.legend(loc=0, fontsize=20)

for bar in ax.patches:
    height = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2.,
            height + 0.2,
            '{}'.format(height),
            ha="center",fontsize=18)


# In[330]:


i_count[22][0]


# In[ ]:




