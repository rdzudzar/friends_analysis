# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 19:29:21 2019

@author: Rob
"""

#Imports
#import os
#from os import path

import functools
import operator

import re
from collections import Counter
import glob

# Imports url
#import urllib.request
#from bs4 import BeautifulSoup
import html2text

#Wordcloud
from wordcloud import WordCloud, STOPWORDS#, ImageColorGenerator
from PIL import Image
import numpy as np

#Plot
import matplotlib.pyplot as plt

#Pandas
import pandas as pd

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
    h.body_width = 0

    #print(h.handle(file))
    episode = h.handle(file)
    #print(episode)
    return episode


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
    h.body_width = 0
    #print(h.handle(file))
    
    all_episodes_in_a_season_txt = []
    for episode in all_episodes_in_a_season: 
        all_episodes = h.handle(episode)
        all_episodes_in_a_season_txt.append(all_episodes)
    return all_episodes_in_a_season_txt


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
                    f2.write(lines[i])

                #Sometimes there are multiple lines, but not all starts with searchquer
                #Add them to the list if they dont start with ** because that would mean different Friend is speaking                       
                # Adjust: remove first 2 characters and rearange last 3
                if line.startswith(searchquery[2:-3]+'**:'): #'Name**:'):
                    f2.write(lines[i])
                    
                # Ross has different formating in ep 16,17, thus this condition:
                if line.startswith(searchquery[0:-3]+'** :'):
                    f2.write(lines[i])
                    

                
    file = open('test_friend.txt', 'r',encoding='utf-8') 
    one_friend = file.read();

    # Remove text within [] and () brackets. These lines are scene description.
    one_friend_tmp = re.sub( "\[[^\]]*\]", "", one_friend) # Removes []
    one_friend_clear = re.sub('\([^)]*\)', "",one_friend_tmp) # Removes ()
    
    return one_friend, one_friend_clear


def get_friend_line_each_ep_in_season(friend_name, all_episodes_in_a_season_txt):
    """
    Get the Friend lines from each episode in a season.
    
    Parameters:
    ----------
    friend_n - Modified string of a friend nema; e.g. if you want Monica, you type: '**Monica:**'
    all_episodes_in_a_season_txt - A list of all episodes in a season as txt file, converted from html.

    Return:
    ------
    friend_s - Lines of the selected friend
    friend_clear_s - Lines of the selected friend, cleared.
    
    """
    friend_s = []
    friend_clear_s = []

    for each_ep in np.arange(0, len(all_episodes_in_a_season_txt), 1):
        friend_tmp, friend_clear_tmp = get_friend_line(friend_name, all_episodes_in_a_season_txt[each_ep])
    
        friend_s.append(friend_tmp)
        friend_clear_s.append(friend_clear_tmp)
    #print(friend_clear_s)
    return friend_s, friend_clear_s


def count_friend_words(friend_clear_s):
    """
    Get the words and count them for a friend.
    
    Parameters:
    ----------
    friend_clear_s - Lines of the selected friend, cleared.

    Return:
    -------
    
    words - List of strings. Unique words.
    dataframe - Pandas Dataframe of words and their counts.
    
    """

    words = []

    for i in np.arange(0, len(friend_clear_s), 1):
        # Use Counter to count the words; It will be dictionary
        words_count = Counter(map(str.lower, friend_clear_s[i].split()))
        words.append(words_count)

    dataframe = []
    for i in np.arange(0, len(words), 1):
    
        # Convert counted words into pandas dataframe
        df = pd.DataFrame.from_dict(words[i], orient='index').reset_index()
        dataframe.append(df)
    
    return words, dataframe

def selfish_friend_words(dataframe):
    """
    Count selfish words, such as: I, Im, Me
    
    Parameters:
    -----------
    dataframe - Pandas Dataframe of words and their counts.

    Return:
    -------
    
    i_count - List of integers. Word counts.
    im_count - List of integers. Word counts.
    my_count - List of integers. Word counts.
    
    """
    i_count = []
    im_count = []
    my_count = []

    for i in np.arange(0, len(dataframe), 1):

        try:
    
            letter_i = dataframe[i][0] [dataframe[i]['index']=='i']
            i_count.append(letter_i.values)
        
            letter_im = dataframe[i][0] [dataframe[i]['index']=='i\'m']
            im_count.append(letter_im.values)
        
            letter_my = dataframe[i][0] [dataframe[i]['index']=='my']
            my_count.append(letter_my.values)

        except KeyError:
            pass
            print('No words in episode {0}'.format(i+1))
            
    return i_count, im_count, my_count

def make_word_dataframe(friend_clear_s, friend_name):
    """
    Make a dataframe from which I can count words.
    
    Parameters:
    -----------
    friend_clear_s - Lines of the selected friend, cleared.

    Return:
    ------
    df - Panadas dataframe.
    
    """
    
    # If I want eason I need to remove nested list
    friend_clear_season = functools.reduce(operator.concat, friend_clear_s)

    # Use Counter to count the words; It will be dictionary
    words_count = Counter(map(str.lower, friend_clear_season.split()))

    # Convert counted words into pandas dataframe
    df = pd.DataFrame.from_dict(words_count, orient='index').reset_index()

    # Rename colums
    df = df.rename(columns={'index':'word', 0:'count'})

    # Sort by the 'count' values, highest first
    df = df.sort_values(['count'], ascending=[False])

    #df.head()
    
    #df.to_csv('./DataFrames/'+str(friend_name[2:-3]), sep='\t', encoding='utf-8')    

    return df

def selfish_friend_words_values(i_count, im_count, my_count):
    """
    Count selfish words, such as: I, Im, Me
    
    Parameters:
    -----------
    i_count - List of integers. Word counts.
    im_count - List of integers. Word counts.
    my_count - List of integers. Word counts.
    
    Return:
    -------
    i_values - List of integers. Word counts.
    im_values - List of integers. Word counts.
    my_values - List of integers. Word counts.
    sum_values - List of integers. Sum of all defined selfish words.
    
    """
    
    
    i_values = []
    im_values = []
    my_values = []

    for i in np.arange(0, len(i_count), 1):
        try:
            value = i_count[i][0]
            i_values.append(value)
        except IndexError:
            i_values.append(0)
        
    for i in np.arange(0, len(im_count), 1):
        try:
            value = im_count[i][0]
            im_values.append(value)
        except IndexError:
            im_values.append(0)
        
    for i in np.arange(0, len(my_count), 1):
        try:
            value = my_count[i][0]
            my_values.append(value)
        except IndexError:
            my_values.append(0)        
        
        # Sum all individual words
    sum_values = [x + y + z for x, y, z in zip(i_values, im_values, my_values)]

    return i_values, im_values, my_values, sum_values


##################################################
########### Handle the functions #################
##################################################

outdir = './output/'    
path = './season/'
filename = '0117.html'


if __name__ == "__main__":

    #Output directory for saving plots/data

    outdir = './output/'
    
    path = './season/'
    filename = '0117.html'


    # Open html page
    f = open_html(filename)
    
    
    first_season = '01*.html'
    first_season_episodes = all_episodes(path, first_season)
    print(len(first_season_episodes))
    
    #Convert html into readable text using html2text
    first_episode = convert_html_to_text(f)
    #print(first_episode)
    # Get txt for all episodes in a season
    all_episodes_in_a_season_txt = convert_season_html_to_text(first_season_episodes)

    print(len(all_episodes_in_a_season_txt))
    #print(all_episodes_in_a_season_txt[18])

    
    # A Friend lines
    list_of_friends = ['**Monica:**', '**Rachel:**', '**Ross:**', '**Joey:**', '**Phoebe:**', '**Chandler:**']
    
    store_i = []
    store_im = []
    store_my = []
    store_sum = []
    
        
    for i, friend in enumerate(list_of_friends):
        friend_name = friend
    
    #friend_name = '**Monica:**'
    #friend_name = '**Rachel:**'
    #friend_name = '**Ross:**'
    #friend_name = '**Joey:**'
    #friend_name = '**Phoebe:**'
    #friend_name = '**Chandler:**'
    
    # Get a Friend line
        friend, friend_clear = get_friend_line(friend_name, first_episode)
    #print(friend_clear)
    # Get a Friend lines for every episode in a season
        friend_s, friend_clear_s = get_friend_line_each_ep_in_season(friend_name, all_episodes_in_a_season_txt)

    # DIFFERENT FORMATING FOR THE EPISODE
    #print(friend_s[15])
    
        words, dataframe = count_friend_words(friend_clear_s)

        i_count, im_count, my_count = selfish_friend_words(dataframe)

        df = make_word_dataframe(friend_clear_s, friend_name)

        i_values, im_values, my_values, sum_values = selfish_friend_words_values(i_count, im_count, my_count)

        store_i.append(i_values)
        store_im.append(im_values)
        store_my.append(my_values)
        store_sum.append(sum_values)
               
    _friends = ['Monica', 'Rachel', 'Ross', 'Joey', 'Phoebe', 'Chandler']

    df_counted = pd.DataFrame({'SumMonica': store_sum[0], 
                               'SumRachel': store_sum[1],
                               'SumRoss':   store_sum[2],
                               'SumJoey':   store_sum[3],
                               'SumPhoebe': store_sum[4],
                               'SumChandler': store_sum[5]})
    print(df_counted)