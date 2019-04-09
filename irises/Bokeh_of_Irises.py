# -*- coding: utf-8 -*-

# Bokeh_of_Irises.py
# comand line use: bokeh serve --show Bokeh_of_Irises.py to render
#
from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column
from bokeh.models.widgets import Select
from bokeh.sampledata.iris import flowers


"""
Creates a Bokeh doc with three selection widgets on the iris data.
"""
    
title0 = "Iris Morphology"

p = figure(title = title0)

colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
colors = [colormap[x] for x in flowers.species]

# lists for populating selection widgets:
spec = ['All'] + flowers.species.unique().tolist()
# remove species:
axis_features = flowers.columns.tolist()[:-1]  

# Selection tools
sel_species = Select(title="Species:",
                     value="All",
                     options=spec)
sel_xfeature = Select(title="x Feature:",
                      value="sepal_length",
                      options=axis_features)
sel_yfeature = Select(title="y Feature:",
                      value="sepal_width",
                      options=axis_features)

# Initial, on-load setup of data and labels:
# Setup ColumnDataSource (cds):
data0 = {'x_val': flowers[sel_xfeature.value],
        'y_val': flowers[sel_yfeature.value],
        'color': colors}
source = ColumnDataSource(data=data0)

p.xaxis.axis_label = sel_xfeature.value
p.yaxis.axis_label = sel_yfeature.value

# Note: when using a ColumnDataSource (cds), the color 
# attribute must be part of the data dict, else need
# to use partial function:
p.circle(x='x_val', y='y_val', color='color',
         source=source,
         fill_alpha=0.2,
         size=10)

# Set up sliders callbacks
def update_plot(attrname, old, new):
    # Get the current selection boxes values
    vx = sel_xfeature.value
    vy = sel_yfeature.value
    s = sel_species.value
    if s == 'All':
        x = flowers[vx]
        y = flowers[vy]
        color = colors
        title = title0
    else:
        x = flowers[flowers.species==s][vx]
        y = flowers[flowers.species==s][vy]
        color = [colormap[x] for x in flowers.species
                if x == s]
        title = title0 + ': ' + sel_species.value.title()

    p.title.text = title
    p.xaxis.axis_label = vx
    p.yaxis.axis_label = vy
    source.data = dict(x_val=x, y_val=y, color=color)

# Bind the widgets with the sole callback function:
sel_species.on_change('value', update_plot)
sel_xfeature.on_change('value', update_plot)
sel_yfeature.on_change('value', update_plot)

# Set up layouts and add to document
inputs = row(sel_xfeature, sel_yfeature)
layout = column(inputs, sel_species, p, width=700)

curdoc().add_root(layout)
