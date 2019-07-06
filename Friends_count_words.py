# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 23:32:37 2019

@author: Rob
"""
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, output_file, show

from Friends_analysis import *
_colors = ['#7fc97f','k','#fdc086','lightgrey','#386cb0','#f0027f']


def make_bokeh_line_plot():
    
    p = figure(plot_width=1300, plot_height=700)
    p.title.text = 'Click on a Friend, Season 1 analysis'

    #for data, name, color in zip([AAPL, IBM, MSFT, GOOG], ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4):

    p.line(df_counted.index, df_counted['SumMonica'], line_width=4, color='#d8b365', 
       alpha=0.4, muted_color='#8c510a', muted_alpha=0.8, legend='Monica')

    p.line(df_counted.index, df_counted['SumRachel'], line_width=4, color='#5ab4ac', 
       alpha=0.4, muted_color='#01665e', muted_alpha=0.8, legend='Rachel')

    p.line(df_counted.index,df_counted['SumPhoebe'], line_width=4, color='#e9a3c9', 
       alpha=0.4, muted_color='#c51b7d', muted_alpha=0.8, legend='Phoebe')

    p.line(df_counted.index,df_counted['SumJoey'], line_width=4, color='#999999', 
       alpha=0.4, muted_color='#4d4d4d', muted_alpha=0.8, legend='Joey')

    p.line(df_counted.index,df_counted['SumChandler'], line_width=4, color='#af8dc3', 
       alpha=0.4, muted_color='#762a83', muted_alpha=0.8, legend='Chandler')

    p.line(df_counted.index,df_counted['SumRoss'], line_width=4, color='#ef8a62', 
       alpha=0.4, muted_color='#b2182b', muted_alpha=0.8, legend='Ross')


    p.legend.location = "top_right"
    p.legend.click_policy="mute"

    # Define axis labels and properties

    p.xaxis.axis_label = 'Episode'
    p.yaxis.axis_label = 'Word Count [Selfish]'

    p.xaxis.axis_label_text_font_size = "15pt"
    p.yaxis.axis_label_text_font_size = "15pt"

    p.title.text_font_size = '18pt'
    p.xaxis.major_label_text_font_size = "15pt"
    p.yaxis.major_label_text_font_size = "15pt"
    p.legend.label_text_font_size = '20pt'
    #output_file("interactive_legend.html", title="interactive_legend.py example")

    show(p)

    return



def make_bokeh_bar_plot():

    p = figure(plot_width=1300, plot_height=700)
    p.title.text = 'Click on a Friend, Season 1 analysis'

    #for data, name, color in zip([AAPL, IBM, MSFT, GOOG], ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4):

    p.vbar(df_counted.index, top = df_counted['SumMonica'], width=0.2, line_width=4, color='grey', 
       alpha=0.4, muted_color='black', muted_alpha=1, legend='Monica')

    p.vbar(df_counted.index,top = df_counted['SumRachel'], width = 0.2, line_width=4, color='#a8ddb5', 
       alpha=0.4, muted_color='#0868ac', muted_alpha=1, legend='Rachel')

    p.vbar(df_counted.index,top = df_counted['SumPhoebe'], width = 0.2, line_width=4, color='#fdbb84', 
       alpha=0.4, muted_color='#e34a33', muted_alpha=1, legend='Phoebe')

    p.vbar(df_counted.index,top = df_counted['SumJoey'],width = 0.2, line_width=4, color='#fa9fb5', 
       alpha=0.4, muted_color='#c51b8a', muted_alpha=1, legend='Joey')

    p.vbar(df_counted.index,top = df_counted['SumChandler'],width = 0.2, line_width=4, color='#d8b365', 
       alpha=0.4, muted_color='#8c510a', muted_alpha=1, legend='Chandler')

    p.vbar(df_counted.index,top = df_counted['SumRoss'],width = 0.2, line_width=4, color='#e9a3c9', 
       alpha=0.4, muted_color='#c51b7d', muted_alpha=1, legend='Ross')


    p.legend.location = "top_right"
    p.legend.click_policy="mute"

    # Define axis labels and properties

    p.xaxis.axis_label = 'Episode'
    p.yaxis.axis_label = 'Word Count [I, I\'m, My]'

    p.xaxis.axis_label_text_font_size = "15pt"
    p.yaxis.axis_label_text_font_size = "15pt"

    p.title.text_font_size = '18pt'
    p.xaxis.major_label_text_font_size = "15pt"
    p.yaxis.major_label_text_font_size = "15pt"

    #output_file("interactive_legend.html", title="interactive_legend.py example")

    show(p)
    
    return

##################################################
########### Handle the functions #################
##################################################

if __name__ == "__main__":
    
    #make_bokeh_bar_plot()
    
    make_bokeh_line_plot()