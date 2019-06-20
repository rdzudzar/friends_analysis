#!/usr/bin/env python
# coding: utf-8

# In[1]:


import urllib.request
from bs4 import BeautifulSoup
import html2text


# ## Read in the html page of the Friends episode transcripts

# In[2]:


filename = './season/0101.html'
f = open(filename, "r").read()
print(f)


# ## Convert html into readable text using html2text

# In[3]:


h = html2text.HTML2Text()
# Ignore converting links from HTML
h.ignore_links = True
print(h.handle(f))
first_episode = h.handle(f)


# In[45]:


from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
stopwords = set(STOPWORDS)

stopwords.add("Scene")

# Need to add stopwords for Frinds if I don't want to show their names
stop_friends = True

if stop_friends == True:
    stopwords.add("Monica")
    stopwords.add("Rachel")
    stopwords.add("Ross")
    stopwords.add("Phoebe")
    stopwords.add("Chandler")
    stopwords.add("Joey")
else:
    print('Firends listed')


# In[46]:


import os
from os import path


# Generate a word cloud image
wordcloud = WordCloud().generate(first_episode)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(first_episode)
plt.figure(figsize=(15,15))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# The pil way (if you don't have matplotlib)
# image = wordcloud.to_image()
# image.show()


# In[64]:


wordcloud = WordCloud(width=500, height=300, background_color='white', max_font_size=40, stopwords=stopwords).generate(first_episode)
plt.figure(figsize=(10,10))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()


# In[ ]:




