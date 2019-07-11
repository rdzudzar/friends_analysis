# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 19:29:21 2019

@author: Rob
"""

#Imports
import os
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
    line_numbers - Integers. Number of lines per Friend per episode.
    
    Explanation:
    ------------
    searchqueries explained:
        
        #Sometimes there are multiple lines, but not all starts with searchquer
        #Add them to the list if they dont start with ** because that would mean different Friend is speaking                       
        # Adjust: remove first 2 characters and rearange last 3
        
        # if line.startswith(searchquery[2:-3]+'**:'): #'Name**:'):
        #                    
        ## Ross has different formating in ep 16,17, thus this condition:
        # if line.startswith(searchquery[0:-3]+'** :'):
        #                    
        ## Most of season 2 has CAPITAL names "ROSS" etc.
        #  if line.startswith((searchquery[2:-3]+':').upper()):
        #                    
        ## SEASON 2 EPISODE 7,8, 10, have their names: MNCA, RACH, JOEY, ROSS, CHAN, PHOE
        #  if line.startswith(searchquery[2:6].upper()):
        #  if line.startswith((searchquery[2]+searchquery[4]+searchquery[6:8]).upper()):
        #                
        ## Season 3 'Name:**'
        # if line.startswith(searchquery[2:]):
        #                    
        ## ROSS s6e10 ****Ross:****
        # if line.startswith('**'+searchquery+'**'):
        #                    
        ## S8E15 " Ross: ** "
        # if line.startswith(searchquery[2:-3]+': **'):
    
    '''
    
    
    # Import episode into the testfile.txt
    file_episode = open('testfile.txt','w', encoding='utf-8') 
    file_episode.write(episode) 
    
    # Search friend lines
    searchquery = friend_name
    
    # Get all the searchqueries, due to the different text formating
    #
    searchqueries = (searchquery, searchquery[2:-3]+'**:', searchquery[0:-3]+'** :',
                     (searchquery[2:-3]+':').upper(), searchquery[2:6].upper(),
                     (searchquery[2]+searchquery[4]+searchquery[6:8]).upper(),
                     searchquery[2:], '**'+searchquery+'**', searchquery[2:-3]+': **')
   
   # From the episode file (testfile) read and write all friend lines into test_friend file.
    with open('testfile.txt', encoding='utf-8') as f1:
        with open('test_friend.txt', 'w', encoding='utf-8') as f2:
            lines = f1.readlines()

            for i, line in enumerate(lines):

                # Add lines that starts with searcquery
                if line.startswith(searchqueries):
                    f2.write(lines[i])
            
            
                
    file = open('test_friend.txt', 'r',encoding='utf-8') 
    one_friend = file.read();

    # Count the number of lines in a file
    # Shape: Friend x episode (example: Monica: 44, 55, ... etc.)
    # And then other friend and other friend
    line_numbers = sum(1 for line in open('test_friend.txt', encoding='utf-8'))

    # Remove text within [] and () brackets. These lines are scene description.
    one_friend_tmp = re.sub( "\[[^\]]*\]", "", one_friend) # Removes []
    one_friend_clear = re.sub('\([^)]*\)', "",one_friend_tmp) # Removes ()
    
    return one_friend, one_friend_clear, line_numbers


def get_episode_title(episode):
    '''
    Get the titles of the episode.
    
    Parameters:
    ----------
    episode - .txt file, converted from html in a function convert_html_to_text.

    Return:
    ------

    title_friend - Strings. Contain title of the episode.
        
    '''
    
    
    # Import episode into the testfile.txt
    file_episode = open('titlefile.txt','w', encoding='utf-8') 
    file_episode.write(episode) 
    
    # Search for titles, most of them start with #, however, off course
    # There are lot of different formatings+
    searchqueries = ('#', 'The One', '9', 'FRIENDS - THE ONE', '**The One', '10')
    skipqueries = ('###', '## credits', '## friends', '# friends')
    
    # From the episode file (testfile) read and write all friend lines into test_friend file.
    with open('titlefile.txt', encoding='utf-8') as f1:
        with open('title_friend.txt', 'w', encoding='utf-8') as f2:
            lines = f1.readlines()

            for i, line in enumerate(lines):
                # Some lines starts with # but they are not titles, skip those
                if line.lower().startswith(skipqueries):
                    continue
                
                # Add lines that starts with searcqueries
                if line.startswith(searchqueries):
                    f2.write(lines[i])

    file = open('title_friend.txt', 'r',encoding='utf-8') 
    title_friend = file.read();
        
    #clean titles; remove (), #, numbers
    title_bracket = re.sub('\([^)]*\)', "",title_friend)
    # Remove everythin befor the first `The` in the title
    # Using only 'T' because some of them are strting with 
    # THE and some of them starting with TOW (the one with)
    title_clean = title_bracket[title_bracket.find('T'):].capitalize()

    return title_clean


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
    num_lines - List of integers. Number of lines for each Friend.
    
    """
    friend_s = []
    friend_clear_s = []
    num_lines = []

    for each_ep in np.arange(0, len(all_episodes_in_a_season_txt), 1):
        friend_tmp, friend_clear_tmp, lines = get_friend_line(friend_name, all_episodes_in_a_season_txt[each_ep])
        num_lines.append(lines)
        
        friend_s.append(friend_tmp)
        friend_clear_s.append(friend_clear_tmp)

    return friend_s, friend_clear_s, num_lines


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
    me_count - List of integers. Word counts.
    
    """
    i_count = []
    im_count = []
    my_count = []
    me_count = []

    for i in np.arange(0, len(dataframe), 1):

        try:
    
            letter_i = dataframe[i][0] [ (dataframe[i]['index']=='i') | (dataframe[i]['index']=='_i')]
            i_count.append(letter_i.values)
        
            letter_im = dataframe[i][0] [ (dataframe[i]['index']=='i\'m') | (dataframe[i]['index']=='i\'ve') | (dataframe[i]['index']=='i\'ll') | (dataframe[i]['index']=='i\'d') ]
            im_count.append(letter_im.values)

            
            letter_my = dataframe[i][0] [ (dataframe[i]['index']=='my') | (dataframe[i]['index']=='mine')]
            my_count.append(letter_my.values)
            
            letter_me = dataframe[i][0] [dataframe[i]['index']=='me']
            me_count.append(letter_me.values)
            
        except KeyError:
            pass
            print('No words in episode {0}'.format(i+1))
            
    return i_count, im_count, my_count, me_count

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

def selfish_friend_words_values(i_count, im_count, my_count, me_count):
    """
    Count selfish words, such as: I, Im, Me
    
    Parameters:
    -----------
    i_count - List of integers. Word counts.
    im_count - List of integers. Word counts.
    my_count - List of integers. Word counts.
    me_count - List of integers. Word counts.

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
    me_values = []

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
        
    for i in np.arange(0, len(me_count), 1):
        try:
            value = me_count[i][0]
            me_values.append(value)
        except IndexError:
            me_values.append(0)  
            
        # Sum all individual words
    sum_values = [x + y + z + w for x, y, z, w in zip(i_values, im_values, my_values, me_values)]

    return i_values, im_values, my_values, me_values, sum_values

def match_phrase(input_text, _pattern):
    
    """
    Find phrases in the text and count how many times it appears.
    
    Parameters
    ----------
    input_text - Strings.
    _pattern - List f string for search.
    
    Return
    ------
    len(count_match) - how many instances of the search query were found
    """
    
    # Search for a repeating pattern in a text
    count_match = []
    pattern = _pattern
    for match in re.finditer(pattern, input_text.lower()):
        
        count_match.append(match)

    print('Found {0} matches of {1}'.format(len(count_match), _pattern))

    return len(count_match)

def count_ep_in_season(list_of_seasons):
    """
    Count episodes in a season.
    
    Parameters
    ----------
    list_of_seasons - List of strings denoting seasons: ['01', '02' ...]
    
    Returns
    -------
    num_episodes - List of integers. Number of episodes in a season.
    
    """
    
    import fnmatch

    season_list = list_of_seasons
    
    num_episodes = []
    for season in season_list:

        episodes = (len(fnmatch.filter(os.listdir(path), '{0}*.html'.format(season))))
        num_episodes.append(episodes)

    return num_episodes

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
    filename = '0101.html'

    

    # Open html page
    f = open_html(filename)

    
    first_season = '*.html'
    list_of_seasons = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']

    
    first_season_episodes = all_episodes(path, first_season)
    #print(first_season_episodes[0][0])
    
    #Convert html into readable text using html2text
    first_episode = convert_html_to_text(f)

    #print(first_episode[0:200])
    # Get txt for all episodes in a season
    all_episodes_in_a_season_txt = convert_season_html_to_text(first_season_episodes)

    #print(all_episodes_in_a_season_txt)
    #print(all_episodes_in_a_season_txt[18])
    
    store_all_titles = []
    for i, each_ep in enumerate(all_episodes_in_a_season_txt):
        title = get_episode_title(each_ep)
        #print('Episode {0} is: {1}'.format(i, title))
        store_all_titles.append(title)
        
    # A Friend lines
    list_of_friends = ['**Monica:**', '**Rachel:**', '**Ross:**', '**Joey:**', '**Phoebe:**', '**Chandler:**']
    
    
    store_i = []
    store_im = []
    store_my = []
    store_me = []
    store_sum = []
    number_of_lines = []
        
    for i, friend in enumerate(list_of_friends):
        friend_name = friend

    
    # Get a Friend line
        friend, friend_clear, friend_lines = get_friend_line(friend_name, first_episode)

        #gives number of characters wit space
        #print(len(friend_clear))
    
    # Get a Friend lines for every episode in a season
        friend_s, friend_clear_s, num_lines = get_friend_line_each_ep_in_season(friend_name, all_episodes_in_a_season_txt)
        number_of_lines.append(num_lines)
    # DIFFERENT FORMATING FOR THE EPISODE
        #print(friend_s[2])
    
        words, dataframe = count_friend_words(friend_clear_s)

        i_count, im_count, my_count, me_count = selfish_friend_words(dataframe)

        df = make_word_dataframe(friend_clear_s, friend_name)

        i_values, im_values, my_values, me_values, sum_values = selfish_friend_words_values(i_count, im_count, my_count, me_count)

        store_i.append(i_values)
        store_im.append(im_values)
        store_my.append(my_values)
        store_me.append(me_values)
        store_sum.append(sum_values)


    _friends = ['Monica', 'Rachel', 'Ross', 'Joey', 'Phoebe', 'Chandler']

    df_counted = pd.DataFrame({'SumMonica': store_sum[0], 
                               'SumRachel': store_sum[1],
                               'SumRoss':   store_sum[2],
                               'SumJoey':   store_sum[3],
                               'SumPhoebe': store_sum[4],
                               'SumChandler': store_sum[5]})
    
    # Add total number of spoken lines per Friend
    df_counted.loc[:, 'NumLinesMon'] = number_of_lines[0]
    df_counted.loc[:, 'NumLinesRac'] = number_of_lines[1]
    df_counted.loc[:, 'NumLinesRos'] = number_of_lines[2]
    df_counted.loc[:, 'NumLinesJoe'] = number_of_lines[3]
    df_counted.loc[:, 'NumLinesPho'] = number_of_lines[4]
    df_counted.loc[:, 'NumLinesCha'] = number_of_lines[5]

    #print(df_counted)

    num_episodes = count_ep_in_season(list_of_seasons)