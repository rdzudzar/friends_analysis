# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 11:24:44 2019

@author: Rob
"""

# Create Friends plots
# Import all functions as tuple
from Friends_analysis import *

from wordcloud import WordCloud, STOPWORDS#, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


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
    #print(stopwords)
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


def generate_wordcloud_all_in_season(all_episodes_in_a_season_txt):
    """
    Generate wordclouds for each episode in a season.
    
    Parameters:
    -----------
    all_episodes_in_a_season_txt - A list of all episodes in a season as txt file, converted from html.
    
    Return:
    -------
    Wordcloud figures for each episode
    
    """
    
    for each_ep in np.arange(0, len(all_episodes_in_a_season_txt), 1):
        generate_wordcloud_bilinear(all_episodes_in_a_season_txt[each_ep], max_font_size)

    return

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

    # show
    plt.figure(figsize=(20,20))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")

    plt.show()
    return


# ## WordCloud per season per Friend

def generate_wordcloud_friend_in_season(friend_clear_s):
    """
    Generate a wordloud of a Friend for each episode in a season.
    
    Parameter:
    ----------
    friend_clear_s - Lines of the selected friend, cleared.

    Return:
    -------
    WordClouds.
    
    """
    for each_ep in np.arange(0, len(friend_clear_s), 1):
        try:
            generate_wordcloud_bilinear(friend_clear_s[each_ep],  max_font_size)
    
        # I'm raising value error because s01e16 is formated differently, thus text for a friend is not detected at the moment
        except ValueError:
            pass
            print('There is an error in episode {0}'.format(each_ep+1))
    return


def plot_top_repeating_words(first_x_words, df):

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


def make_plot_selfish_words(i_values, im_values, my_values, sum_values, friend_name):
    """
    Make a bar plot of the selfish words throughout the season.
    
    Parameters:
    -----------
    i_values - List of integers. Word counts.
    im_values - List of integers. Word counts.
    my_values - List of integers. Word counts.
    sum_values - List of integers. Sum of all defined selfish words.
    friend_name - Modified string of a friend nema; e.g. if you want Monica, you type: '**Monica:**'

    
    Return:
    -------
    Plot.
    
    """
    
    
    A = np.arange(1, len(i_count)+1, 1)

    fig, ax = plt.subplots(1, figsize=(15,10))


    #plt.bar(A, i_values, color='grey', edgecolor='k', label='I', alpha=1)
    #plt.bar(A, im_values, color='lightgrey', edgecolor='k', label='I\'m', alpha = 0.5)
    #plt.bar(A, my_values, color='white', edgecolor='k', label='My', alpha = 0.8)

    plt.bar(A, sum_values, color='lightgrey', edgecolor='k', label='I, I\'m, My [{0}]'.format(friend_name[2:-3]), alpha = 1)


    ax.tick_params(axis='both', which='major', labelsize=16)

    plt.xlabel('Episode', fontsize=24)
    plt.ylabel('Counts', fontsize=22)
    plt.legend(loc=0, fontsize=20)

    for bar in ax.patches:
        height = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2.,
                height + 0.2,
                '{}'.format(height),
                ha="center",fontsize=18)
    return

def make_lineplot_selfish_words(i_values, im_values, my_values, sum_values, friend_name):
    """
    Make a bar plot of the selfish words throughout the season.
    
    Parameters:
    -----------
    i_values - List of integers. Word counts.
    im_values - List of integers. Word counts.
    my_values - List of integers. Word counts.
    sum_values - List of integers. Sum of all defined selfish words.
    friend_name - Modified string of a friend nema; e.g. if you want Monica, you type: '**Monica:**'

    
    Return:
    -------
    Plot.
    
    """
    
    
    A = np.arange(1, len(i_count)+1, 1)

    #fig, ax = plt.subplots(1, figsize=(15,10))


    #plt.bar(A, i_values, color='grey', edgecolor='k', label='I', alpha=1)
    #plt.bar(A, im_values, color='lightgrey', edgecolor='k', label='I\'m', alpha = 0.5)
    #plt.bar(A, my_values, color='white', edgecolor='k', label='My', alpha = 0.8)
    #print(store_sum)
    
    # Create a dictionary with a Friend and color selection
    # Place True for a Friend which you want to have highlighted color, 
    # else it will have lightgrey color
    select_dict = {
            'Monica'  : (False, 'lightgrey', 'black'),
            'Rachel'  : (True, 'lightgrey', '#0868ac'),
            'Ross'    : (True, 'lightgrey', '#c51b7d'),
            'Joey'    : (False, 'lightgrey', '#c51b8a'),
            'Phoebe'  : (False, 'lightgrey', '#e34a33'),
            'Chandler': (False, 'lightgrey', '#8c510a')
            }   
    # Create a list of _colors from the dictionary above, based on the selected
    # Friend. 
    _colors = []
    for key in select_dict.keys():
        if select_dict[key][0] == True:
            colors = select_dict[key][2]
        else:
            colors = select_dict[key][1]
        
        _colors.append(colors)
    
    
    #_friends = ['Monica', 'Rachel', 'Ross', 'Joey', 'Phoebe', 'Chandler']
    #_colors = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c']
    #_colors = ['#7fc97f','k','#fdc086','lightgrey','#386cb0','#f0027f']
    #_colors = ['#762a83','#af8dc3','#e7d4e8','#d9f0d3','#7fbf7b','#1b7837']
    
    df_counted.plot(kind='line', color=_colors, figsize=(14,9))

    #ax.tick_params(axis='both', which='major', labelsize=16)

    plt.xlabel('Episode', fontsize=24)
    plt.ylabel('Counts', fontsize=22)
    plt.legend(loc=0, fontsize=20)

    return

##################################################
########### Handle the functions #################
##################################################

if __name__ == "__main__":

    
        # WordCloud
    # Create stopwords
    stopwords = add_stopwords_to_wordcloud(True);
    
    # Define parameters for wordcloud
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

    # Wordcloud for episode
    #generate_wordcloud_bilinear(first_episode, max_font_size)

    # Wordcloud for each episode in a season
    #generate_wordcloud_all_in_season(all_episodes_in_a_season_txt)
    
    # WordCloud with a mask
    mask_image = 'friends_couch.jpg'
    #generate_wordcloud_with_mask(mask_image, first_episode)

    # WordCloud
    #generate_wordcloud_bilinear(friend_clear_s[0], max_font_size)
    
    #generate_wordcloud_friend_in_season(friend_clear_s)

    # A Friend lines
    list_of_friends = ['**Monica:**', '**Rachel:**', '**Ross:**', '**Joey:**', '**Phoebe:**', '**Chandler:**']
       
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

        i_count, im_count, my_count, me_count = selfish_friend_words(dataframe)

        df = make_word_dataframe(friend_clear_s, friend_name)

        i_values, im_values, my_values, me_values, sum_values = selfish_friend_words_values(i_count, im_count, my_count, me_count)
                
        first_x_words = 15
        #plot_top_repeating_words(first_x_words, df)
        #make_plot_selfish_words(i_values, im_values, my_values, sum_values, friend_name)
    
    #print(store_i)

    make_lineplot_selfish_words(store_i, store_my, store_im, store_sum, friend_name)
