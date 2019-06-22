#!/usr/bin/env python
# coding: utf-8

# In[10]:


# Run this in Python once, it should take effect permanently
from notebook.services.config import ConfigManager
c = ConfigManager()
c.update('notebook', {"CodeCell": {"cm_config": {"autoCloseBrackets": False}}})


# In[11]:


#Imports
import os
from os import path

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


# ## Read in the html page of the Friends episode transcripts

# In[12]:


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


# In[13]:


f = open_html(filename)


# ## Convert html into readable text using html2text

# In[14]:


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


# In[15]:


first_episode = convert_html_to_text(f)


# In[440]:


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
    
    stopwords = set() #set(STOPWORDS) for default exclusion
    
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


# In[479]:


stopwords = add_stopwords_to_wordcloud(True);


# In[480]:


max_font_size = 100
min_font_size = 3
bck_color = 'white'
#width = 500
#height = 300
width=1600
height=800
colourmap = plt.cm.cividis_r
relative_scaling = 0

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
                          max_font_size=max_font_size, stopwords=stopwords, colormap = colourmap,
                         relative_scaling=relative_scaling).generate(episode)
    
    
    plt.figure(figsize=(15,15))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    # The pil way (if you don't have matplotlib)
    # image = wordcloud.to_image()
    # image.show()


# In[481]:


generate_wordcloud_bilinear(first_episode, max_font_size)


# In[487]:


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


# In[488]:


generate_wordcloud_with_mask(mask_image, first_episode)


# In[446]:


import re


# In[482]:


#friend_name = '**Monica:**'
#friend_name = '**Rachel:**'
#friend_name = '**Ross:**'
#friend_name = '**Joey:**'
friend_name = '**Phoebe:**'
#friend_name = '**Chandler:**'

def get_friend_line(friend_name, episode):
    '''
    
    '''
    file_episode = open('testfile.txt','w') 
    file_episode.write(episode) 
    
    
    searchquery = friend_name

    with open('testfile.txt') as f1:
        with open('test_monica.txt', 'w') as f2:
            lines = f1.readlines()
            for i, line in enumerate(lines):
                if line.startswith(searchquery):
                    f2.write(line)
                
    file = open('test_monica.txt', 'r') 
    monica_1 = file.read();
    
    return monica_1


# In[483]:


rachel = get_friend_line(friend_name, first_episode)
print(rachel)


# In[484]:


generate_wordcloud_bilinear(rachel, max_font_size)


# In[268]:


#with open("testfile.txt") as fh:
#    for line in fh:
#        if line.startswith("**Monica:**"):
#            print(line)


# In[270]:


#searchquery = '**Monica:**'
#
#with open('testfile.txt') as f1:
#    with open('test_monica.txt', 'a') as f2:
#        lines = f1.readlines()
#        for i, line in enumerate(lines):
#            if line.startswith(searchquery):
#                f2.write(line)


# In[269]:


#file = open('test_monica.txt', 'r') 
#monica_1 = file.read()


# In[391]:


import collections
import re
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[486]:


#https://medium.com/@agrimabahl/elegant-python-code-reproduction-of-most-common-words-from-a-story-25f5e28e0f8c
file = open('test_monica.txt', 'r')
file = file.read()
#stopwords = set(line.strip() for line in open('stopwords.txt'))
stopwords = stopwords#.union(set(['']))
wordcount = collections.defaultdict(int)
""" 
the next paragraph does all the counting and is the main point of difference from the original article. More on this is explained later.
"""
# \W is regex for characters that are not alphanumerics.
# all non-alphanumerics are replaced with a blank space using re.sub
pattern = r"\W"
for word in file.lower().split():
    word = re.sub(pattern, '', word)
    if word not in stopwords:
        wordcount[word] += 1
# printing most common words
to_print = int(input("How many top words do you wish to print?"))
n = to_print
print(f"The most common {n} words are:")
# the next line sorts the default dict on the values in decreasing  # order and prints the first "to_print".
mc = sorted(wordcount.items(), key=lambda k_v: k_v[1], reverse=True)[:to_print] # this is continued from the previous assignment
for word, count in mc:
    print(word, ":", count)
# Draw the bart chart
mc = dict(mc)
names = list(mc.keys())
values = list(mc.values())
plt.bar(range(len(mc)),values,tick_label=names)
#plt.savefig('bar.png')
plt.show()


# In[ ]:




