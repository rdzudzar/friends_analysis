# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 09:58:08 2019

@author: Rob
"""
import re
from Friends_analysis import *
import pandas as pd



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

    #print('Found {0} matches of {1}'.format(len(count_match), _pattern))

    return len(count_match)


if __name__ == "__main__":

        # Open html page
    f = open_html(filename)

    
    first_season = '*.html'
    first_season_episodes = all_episodes(path, first_season)
    print('There are {0} episodes'.format(len(first_season_episodes)))
    
    #Convert html into readable text using html2text
    first_episode = convert_html_to_text(f)
    #print(first_episode)
    # Get txt for all episodes in a season
    all_episodes_in_a_season_txt = convert_season_html_to_text(first_season_episodes)
    
    #print(all_episodes_in_a_season_txt)

    # A Friend lines
    list_of_friends = ['**Monica:**', '**Rachel:**', '**Ross:**', '**Joey:**', '**Phoebe:**', '**Chandler:**']

    store_sum_sorry = []
    for i, friend in enumerate(list_of_friends):
        friend_name = friend

        # Get a Friend line
        friend, friend_clear, friend_lines = get_friend_line(friend_name, first_episode)
        #print(friend_clear)
        # Get a Friend lines for every episode in a season
        friend_s, friend_clear_s, num_lines = get_friend_line_each_ep_in_season(friend_name, all_episodes_in_a_season_txt)


        # Go through each episode and find occurance of given list of patterns
        lengths = []
        for each_ep in friend_clear_s:
            Phrase = each_ep 
    
        # Find phrases and count them all
            list_patterns = ["i'm sorry", "im sorry", "sorry"]
    
            for _pattern in list_patterns:
                counts = match_phrase(each_ep, _pattern)
                lengths.append(counts)
                total_phrases_found = lengths
                #print(sum(total_phrases_found))
        #print("{0} is sorry {1} times".format(friend_name[2:-3], total_phrases_found))

        store_sum_sorry.append(total_phrases_found)
        
    _friends = ['Monica', 'Rachel', 'Ross', 'Joey', 'Phoebe', 'Chandler']
    # This will give me all ot the phrases: 0, 1, 2 row will be i'm sorry, imsorry and sorry
    # Need to sum every third row to get the sum for each phrase per episode
    df_counted_sorry = pd.DataFrame({'SumMonica': store_sum_sorry[0], 
                               'SumRachel': store_sum_sorry[1],
                               'SumRoss':   store_sum_sorry[2],
                               'SumJoey':   store_sum_sorry[3],
                               'SumPhoebe': store_sum_sorry[4],
                               'SumChandler': store_sum_sorry[5]})
    #print(df_counted_sorry)
    
    # Every third element - to get the numbers of 'sorry'
    # Can get Nth number of any element in a list_patterns
    N = 3
    #new = df_counted_sorry.groupby(df_counted_sorry.index // N).sum()
    df_only_sorry = df_counted_sorry.iloc[::N, :].reset_index()
    df_only_sorry.loc[:, 'Titles'] = store_all_titles
    print(df_only_sorry['Titles'])
    
    