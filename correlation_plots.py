# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 11:12:37 2019

@author: Rob
"""
from Friends_analysis import *
import seaborn as sns



def poly_fit_friends():
  
    y_predicted_all = []
    std_all = []
    for i, friend in enumerate(friend_lines):
    
        data = np.polyfit(df_counted.index, df_counted[friend], 1, full=True)
        slope = data[0][0]
        intercept = data[0][1]
        y_predicted = [slope*j + intercept  for j in df_counted.index]
        y_predicted_all.append(y_predicted)
        # STD is large: 13-16
        std_data = np.std(df_counted[friend])
        std_all.append(std_data)

    return y_predicted_all, std_all
    
def fit_num_lines_friend():
    
       
    for i, friend in enumerate(friend_lines):
        
        fig, ax = plt.subplots(1, figsize=(12,8))
        #plt.plot(df_counted.index, df_counted['NumLinesPho'], 'k-')
        sns.regplot(x = df_counted.index, y = friend, data = df_counted, 
                color='black',  order=1, label = _friends[i])

        for each_fit in y_predicted:
            plt.plot(df_counted.index, each_fit, '-')

        plt.xlabel('Episode', fontsize=18)
        plt.ylabel('Number of Lines', fontsize=18)
        
        plt.legend(loc=2, fontsize=20)
        plt.show()
    
def only_fit_lines(show_points):

               
    fig, ax = plt.subplots(1, figsize=(13,7))
        #plt.plot(df_counted.index, df_counted['NumLinesPho'], 'k-')

    for i, each_fit in enumerate(y_predicted):
            plt.plot(df_counted.index, each_fit, linestyle=_lines[i], linewidth=4,
                     color = _colors[i], label = _friends[i])

    #sns.kdeplot(df_counted.index, df_counted['NumLinesRos'], 
    #            cmap="Greys", shade=True, shade_lowest=False, n_levels=5)
    if show_points == True:

        for i, each_friend in enumerate(friend_lines):
            plt.plot(df_counted.index, df_counted[each_friend], 
                 'ko', color=_colors[i], label = '', alpha=0.2)


    ax.tick_params(direction="in")
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    
    plt.xlabel('Episode', fontsize=18)
    plt.ylabel('Number of Lines', fontsize=18)
        
    plt.legend(loc=2, fontsize=20)
    plt.show()
    
    
##################################################
########### Handle the functions #################
##################################################

friend_lines = ['NumLinesMon','NumLinesRac','NumLinesRos',
                    'NumLinesJoe','NumLinesPho','NumLinesCha']
    #_friends = ['Monica', 'Rachel', 'Ross', 'Joey', 'Phoebe', 'Chandler']
_colors = ['black', '#0868ac', '#b2182b', 'grey', '#762a83', '#8c510a']
_lines = ['-', '-', '-', '-', '-', '-']



if __name__ == "__main__":    
    
    y_predicted, std_all = poly_fit_friends()
    
    #fit_num_lines_friend()

    _show = True
    only_fit_lines(_show)