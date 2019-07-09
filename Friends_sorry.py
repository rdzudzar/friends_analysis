# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 10:43:10 2019

@author: Rob
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 23:32:37 2019

@author: Rob
"""
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, BoxSelectTool

from Friends_analysis import *


print(len(store_all_titles))
print(len(df_only_sorry.index))

def make_bokeh_line_plot():
    
    
    
    source = {name: ColumnDataSource(
        data=dict(
            x=df_only_sorry.index,
            y=df_only_sorry['Sum'+name],
            episode = df_only_sorry['Titles'],
        )
    ) for name in _friends}

    hover = HoverTool(
        tooltips=[
            ("index", "Episode $index"),
#            ("(x,y)", "($x, $y)"),
            ("episode", "@episode")
#            ("Desc", "%s" % ([0]*len(df_only_sorry.index))),
#            ("Desc2", "@desc")
        ]
    )
    
    
    
    p = figure(plot_width=1300, plot_height=700, tools=[hover])
    p.title.text = 'Click on a Friend, Series analysis'

    #for data, name, color in zip([AAPL, IBM, MSFT, GOOG], ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4):


    p.line(df_only_sorry.index, df_only_sorry['SumMonica'], line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#8c510a', muted_alpha=1, legend='Monica')
        
    p.line(df_only_sorry.index, df_only_sorry['SumMonica'], line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#8c510a', muted_alpha=1, legend='Monica')

    p.line(df_only_sorry.index, df_only_sorry['SumRachel'], line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#01665e', muted_alpha=1, legend='Rachel')

    p.line(df_only_sorry.index,df_only_sorry['SumPhoebe'], line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#c51b7d', muted_alpha=1, legend='Phoebe')
 
    p.line(df_only_sorry.index,df_only_sorry['SumJoey'], line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#4d4d4d', muted_alpha=1, legend='Joey')
    p.line(df_only_sorry.index,df_only_sorry['SumChandler'], line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#762a83', muted_alpha=1, legend='Chandler')

    p.line(df_only_sorry.index,df_only_sorry['SumRoss'], line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#b2182b', muted_alpha=1, legend='Ross')

    p.select(dict(type=HoverTool)).tooltips = {"episode":"@episode"}

   # p.add_tools(hover)


    p.legend.location = "top_right"
    p.legend.click_policy="mute"

    # Define axis labels and properties

    p.xaxis.axis_label = 'Episode'
    p.yaxis.axis_label = 'Sorry [counts]'

    p.xaxis.axis_label_text_font_size = "15pt"
    p.yaxis.axis_label_text_font_size = "15pt"

    p.title.text_font_size = '18pt'
    p.xaxis.major_label_text_font_size = "15pt"
    p.yaxis.major_label_text_font_size = "15pt"
    p.legend.label_text_font_size = '20pt'
    #output_file("interactive_legend.html", title="interactive_legend.py example")

    show(p)

    return

###########################################
########### Handle the functions #################
##################################################

if __name__ == "__main__":
        
    make_bokeh_line_plot()
    
