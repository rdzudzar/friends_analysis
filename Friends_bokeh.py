# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 23:32:37 2019

@author: Rob
"""
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, ColorBar, HoverTool, BoxSelectTool, LabelSet, Label

from Friends_analysis import *




def make_bokeh_line_plot():
    
    source = ColumnDataSource(
        data=dict(
            x=df_counted.index,
            mon=df_counted['NumLinesMon'],
            rac=df_counted['NumLinesRac'],
            pho=df_counted['NumLinesPho'],
            joe=df_counted['NumLinesJoe'],
            cha=df_counted['NumLinesCha'],
            ros=df_counted['NumLinesRos'],
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

    p.vbar(season_delim, top=num_delim, width=0.2, color='purple', legend='Season+')   


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


    p.legend.location = "top_right"
    p.legend.click_policy="mute"

    # Define axis labels and properties

    p.xaxis.axis_label = 'Episode'
    p.yaxis.axis_label = 'Number of Lines'

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
    p.title.text = 'Click on a Friend, Series analysis'

    p.vbar(season_delim, top=num_delim, width=0.2, color='purple', legend='Season+')   

    #for data, name, color in zip([AAPL, IBM, MSFT, GOOG], ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4):

    p.vbar(df_counted.index, top = df_counted['SumMonica'], width=0.2, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='black', muted_alpha=1, legend='Monica')

    p.vbar(df_counted.index,top = df_counted['SumRachel'], width = 0.2, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#0868ac', muted_alpha=1, legend='Rachel')

    p.vbar(df_counted.index,top = df_counted['SumPhoebe'], width = 0.2, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#e34a33', muted_alpha=1, legend='Phoebe')

    p.vbar(df_counted.index,top = df_counted['SumJoey'],width = 0.2, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#c51b8a', muted_alpha=1, legend='Joey')

    p.vbar(df_counted.index,top = df_counted['SumChandler'],width = 0.2, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#8c510a', muted_alpha=1, legend='Chandler')

    p.vbar(df_counted.index,top = df_counted['SumRoss'],width = 0.2, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#c51b7d', muted_alpha=1, legend='Ross')


    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    p.legend.click_policy="mute"

    # Define axis labels and properties

    p.xaxis.axis_label = 'Episode'
    p.yaxis.axis_label = 'Word Count [I, I\'m, My]'

    p.xaxis.axis_label_text_font_size = "15pt"
    p.yaxis.axis_label_text_font_size = "15pt"

    p.title.text_font_size = '18pt'
    p.xaxis.major_label_text_font_size = "15pt"
    p.yaxis.major_label_text_font_size = "15pt"

    p.output_file("Friends_interactive.html")

    show(p)
    
    return

def make_bokeh_normalized_plot():
    
    source = ColumnDataSource(
        data=dict(
            x=df_counted.index,
            mon=df_counted['SumMonica']/df_counted['NumLinesMon'],
            rac=df_counted['SumRachel']/df_counted['NumLinesRac'],
            pho=df_counted['SumPhoebe']/df_counted['NumLinesPho'],
            joe=df_counted['SumJoey']/df_counted['NumLinesJoe'],
            cha=df_counted['SumChandler']/df_counted['NumLinesCha'],
            ros=df_counted['SumRoss']/df_counted['NumLinesRos'],
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


    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    p.legend.click_policy="mute"

    # Define axis labels and properties

    p.xaxis.axis_label = 'Episode'
    p.yaxis.axis_label = '\"Self-oriented\" [counts]'

    p.xaxis.axis_label_text_font_size = "15pt"
    p.yaxis.axis_label_text_font_size = "15pt"

    p.title.text_font_size = '18pt'
    p.xaxis.major_label_text_font_size = "15pt"
    p.yaxis.major_label_text_font_size = "15pt"
    p.legend.label_text_font_size = '20pt'
    #output_file("interactive_legend.html", title="interactive_legend.py example")

    x_positions = [7, 29.5, 53.5, 78.5, 99.5, 123.5, 146.5, 168.5, 192.5, 211.5]
    season_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i, each_label in enumerate(x_positions):
        mytext = Label(x=each_label, y=0, text='Season {0}'.format(season_num[i]),
                       border_line_color='black', border_line_alpha=0.5,text_font_size="13pt")
        p.add_layout(mytext)

    show(p)

    return

def make_bokeh_correlation_numline_plot():
    
    source = ColumnDataSource(
        data=dict(
            x=df_counted.index,
            monica=df_counted['NumLinesMon'],
            rachel=df_counted['NumLinesRac'],
            phoebe=df_counted['NumLinesPho'],
            joey=df_counted['NumLinesJoe'],
            chandler=df_counted['NumLinesCha'],
            ross=df_counted['NumLinesRos'],
            episode = df_only_sorry['Titles'],
        )
    ) 


    hover = HoverTool(
        tooltips=[
            ("Episode", "$index"),
            ("Title", "@episode")
        ]
    )
    

    p = figure(plot_width=1500, plot_height=800, tools=[hover, "pan,wheel_zoom,box_zoom,reset"])
    p.title.text = 'Click on a Friend, Series analysis'

    x_corr = 'x'
    
    p.vbar(season_delim, top=num_delim_lines, width=0.2, color='purple', legend='')   
    
    p.line(x_corr,'monica', source=source, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#8c510a', muted_alpha=1, legend='Monica')
        
    p.line(x_corr, 'rachel', source=source, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#01665e', muted_alpha=1, legend='Rachel')

    p.line(x_corr, 'phoebe', source=source, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#c51b7d', muted_alpha=1, legend='Phoebe')
 
    p.line(x_corr, 'joey', source=source, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#4d4d4d', muted_alpha=1, legend='Joey')
    
    p.line(x_corr, 'chandler', source=source, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#762a83', muted_alpha=1, legend='Chandler')

    p.line(x_corr, 'ross', source=source, line_width=4, color='lightgrey', 
       alpha=0.4, muted_color='#b2182b', muted_alpha=1, legend='Ross')

    x_positions = [7, 29.5, 53.5, 78.5, 99.5, 123.5, 146.5, 168.5, 192.5, 211.5]
    season_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for i, each_label in enumerate(x_positions):
        mytext = Label(x=each_label, y=0, text='Season {0}'.format(season_num[i]),
                       border_line_color='black', border_line_alpha=0.5,text_font_size="13pt")
        p.add_layout(mytext)   
    
    
# THIS IS GOOD BUT IT DOESNT WORK ON ZOOM    
#    source_labels = ColumnDataSource(data=dict(x_positions = np.cumsum(num_episodes),
#                                        num_delim = num_delim_lines, 
#                                        names = ['Season 1', 'Season 2', 'Season 3', 'Season 4', 
#                                                 'Season 5', 'Season 6', 'Season 7', 'Season 8',
#                                                 'Season 9', 'Season 10']))
#    
#    #p = figure(plot_width=1500, plot_height=800, tools=["pan,wheel_zoom,box_zoom,reset"])
#    p.vbar(x='x_positions', top='num_delim', width=0.2, color='purple', legend='', source=source_labels)   
#
#    #p.scatter(x='x_positions', y='num_delim', size=8, source=source_labels)
#    
#    labels = LabelSet(x='x_positions', y='num_delim', text='names', level='glyph',
#                  x_offset=-100, y_offset=-530, source=source_labels, render_mode='canvas')
#    
#    p.add_layout(labels)
    
    
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    p.legend.click_policy="mute"

    # Define axis labels and properties

    #p.xaxis.axis_label = 'Number of Lines of {0}'.format(x_corr.capitalize())
    p.xaxis.axis_label = 'Episode'
    p.yaxis.axis_label = 'Number of Lines'

    p.xaxis.axis_label_text_font_size = "15pt"
    p.yaxis.axis_label_text_font_size = "15pt"

    p.title.text_font_size = '18pt'
    p.xaxis.major_label_text_font_size = "15pt"
    p.yaxis.major_label_text_font_size = "15pt"
    p.legend.label_text_font_size = '20pt'
    #output_file("interactive_legend.html", title="interactive_legend.py example")

    show(p)



##################################################
########### Handle the functions #################
##################################################

season_delim = np.cumsum(num_episodes).tolist()
num_delim = [2.5]*10
num_delim_lines = [100]*10


if __name__ == "__main__":
    
    # Line bar plot
    #make_bokeh_bar_plot()
    
    # Number of lines
    make_bokeh_line_plot()
    
    # Normalized plot of self-oriented
    #make_bokeh_normalized_plot()
    
   # make_bokeh_correlation_numline_plot()
        