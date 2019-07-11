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
    
    
    
    source = ColumnDataSource(
        data=dict(
            x=df_only_sorry.index,
            mon=df_only_sorry['SumMonica'],
            rac=df_only_sorry['SumRachel'],
            pho=df_only_sorry['SumPhoebe'],
            joe=df_only_sorry['SumJoey'],
            cha=df_only_sorry['SumChandler'],
            ros=df_only_sorry['SumRoss'],
            episode = df_only_sorry['Titles'],
        )
    ) 

    hover = HoverTool(
        tooltips=[
            ("Episode", "$index"),
            ("Title", "@episode")
        ]
    )
    
    
    
    p = figure(plot_width=1300, plot_height=700, tools=[hover, "pan,wheel_zoom,box_zoom,reset"])
    p.title.text = 'Click on a Friend, Series analysis'

    p.vbar(season_delim, top=num_delim, width=0.2, color='purple', legend='')   

    p.line('x','mon', source=source, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#8c510a', muted_alpha=1, legend='Monica')
        
    p.line('x', 'rac', source=source, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#01665e', muted_alpha=1, legend='Rachel')

    p.line('x', 'pho', source=source, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#c51b7d', muted_alpha=1, legend='Phoebe')
 
    p.line('x', 'joe', source=source, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#4d4d4d', muted_alpha=1, legend='Joey')
    
    p.line('x', 'cha', source=source, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#762a83', muted_alpha=1, legend='Chandler')

    p.line('x', 'ros', source=source, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#b2182b', muted_alpha=1, legend='Ross')


    x_positions = [7, 29.5, 53.5, 78.5, 99.5, 123.5, 146.5, 168.5, 192.5, 211.5]
    season_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i, each_label in enumerate(x_positions):
        mytext = Label(x=each_label, y=0, text='Season {0}'.format(season_num[i]),
                       border_line_color='black', border_line_alpha=0.5,text_font_size="13pt")
        p.add_layout(mytext)   
    
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

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
    
    season_delim = np.cumsum(num_episodes).tolist()
    num_delim = [4]*10

    
    make_bokeh_line_plot()
    
