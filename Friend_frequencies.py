# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 19:36:35 2019

@author: Rob
"""

# Find how many times throughout the show each Friend is saying name
# of some other Friend

# Include nicknames: Pheebs, Rach, Mon, Joseph, 


# Create nested dictionary with a Friend and for each friend
# place how many times they are saying name of other Friends

# Each key -- Friend name, should have subdictionary with 
# other Friend names keys and for each of them value will 
# be a list of the counts how many times per episode
# they were called by key Friend. 

def friend_mentions():
    """
    
    Returns: Nested dictionary.
    """
    
    name_mentiones = {
            'Monica'  : (),
            'Rachel'  : (),
            'Ross'    : (),
            'Joey'    : (),
            'Phoebe'  : (),
            'Chandler': ()
            }
    
    return name_mentiones


# Who was the most featured in the beginning in each episode
# Find counts of Friends names before the Openning Credits 
# (Openning title); in a file

def episode_intro():
    
    intro_count = []
    opening_credits = '**Opening Credits**'
    for i, each_ep in enumerate(all_episodes_in_a_season_txt):
        
        # There are plenty formatings for "Opening Credits", fine all of them and replace them with the most used ones
        replace_each_ep = each_ep.replace('### Opening Credits', opening_credits).replace('Opening Credits**', 
                        opening_credits).replace('**OPENING TITLES**', opening_credits).replace('OPENING TITLES', 
                        opening_credits).replace('## Credits', opening_credits).replace('OPENING CREDITS',
                        opening_credits).replace('Opening Credits', opening_credits).replace('**Opening credits.**',
                        opening_credits).replace('Opening credits', opening_credits).replace('OPENING SEQUENCE',opening_credits)

        # Check if the phrase "**Opening Credits**" is in the text 
        if '**Opening Credits**' not in replace_each_ep:
            print(i)
                                          
        get_intro = replace_each_ep.split('**Opening Credits**')[0]
        
        # Remove text within [] and () brackets. These lines are scene description.
        one_intro_tmp = re.sub( "\[[^\]]*\]", "", get_intro) # Removes []
        intro_clear = re.sub('\([^)]*\)', "",one_intro_tmp) # Removes ()
 
        intro_count.append(intro_clear)
    
    print(intro_count[225][0:2600])
    print(len(intro_count))    

    return intro_count 



# Find how many times the scenes are in the Central Perk
# How many times the scene before openning credits in in Central Perk
# Scenes are not always placed in text - locate ep. without that
    
def scene_central_perk():
    
    counts_central_perk = []
    counts_central_perk_openning = []
    
    return counts_central_perk, counts_central_perk_openning


# Divide every episode into scenes and find which of Friends are 
# the most frequent featured in scenes together
    
def frequently_together():
    
    return 

# Find lines, apearance of Janice throughout the series
# Make her cloudword
# Count how many times she says  "Oh My God" 
    
def janice():
    
    return

##################################################
########### Handle the functions #################
##################################################


if __name__ == "__main__":
        
    intro = episode_intro()
    