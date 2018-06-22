import pandas as pd

from bokeh.plotting import figure
from bokeh.layouts import layout, row, widgetbox
from bokeh.models import ColumnDataSource, Div, HoverTool, Range1d
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.models.widgets import Select
from bokeh.io import curdoc

df = pd.read_csv('UCR65_16.csv')

def select_state():
    '''
    A function to filter the dataframe by  the selected state. Default value is
    "All".
    '''
    if states.value == 'All':
        selected = df[['YEAR','CLR','MRD']]
    else:
        selected = df[df['State']== states.value][['YEAR','CLR','MRD']]
    return selected

def create_figure():
    '''
    The main function to aggregate the data and create the figure.
    '''
    use_df = select_state() # Get the filtered dataframe
    agg = use_df.groupby('YEAR',as_index=False).sum() # aggregate the dataframe
    agg['Clearance_Rate'] = agg['CLR'] / agg['MRD'] # Set Clearance Rate column
    source = ColumnDataSource(agg) # put into a bokeh data structure
    hover = HoverTool( # Set the hover tools, ('Title', '@Column{formatting}'')
        tooltips = [
        ('Year', '@YEAR'),
        ('Total Murders','@MRD{0,0}'),
        ('Solved Murders','@CLR{0,0}'),
        ('Clearance Rate','@Clearance_Rate{0%}')
        ]
    )
    tools=[hover]
    p = figure(plot_width=600, plot_height=400,tools=tools) # Create figure
    p.xaxis.axis_label = 'Year'
    p.yaxis.axis_label = 'Murders'
    # Set the range for the yaxis dynamically. Requires bokeh Rand1d object
    p.y_range=Range1d(0,agg['MRD'].max() * 1.05)
    p.yaxis[0].formatter = NumeralTickFormatter(format='0,0')
    # Actually plot the lines now.
    p.line('YEAR','MRD',source=source, line_width=3,)
    p.line('YEAR','CLR',source=source, line_width=3, color='orange')
    p.title.text = '{} Murders by Year'.format(states.value) # dynamic title

    return p

def update(attr, old, new):
    '''
    A function to update an element (the chart) within the layout.
    '''
    lay_out.children[0].children[1] = create_figure()

# Select creates the dropdown menu that we put the states into for filtering.
states = Select(title='State', value='All',
               options= ['All']+df.State.unique().tolist())
states.on_change('value', update) # specify what to do when state value changes

# This is some crude html to put below the chart. It Requires bokeh Div object.
with open('description.html','r') as f:
    desc = Div(text=f.read(),width=1000)

inputs = widgetbox(states, width=200) # set up the input widgets
# comlpex bokeh applications require use of a layout object, (or row or column)
# layout is a list of lists, each list is a row, each element in the row is
# a column, or that is how I understand it
lay_out = layout([
    [inputs, create_figure()],
    [desc,]
])

# set up the html document
curdoc().add_root(lay_out)
curdoc().title = "Murders by Year" # sets the title of the tab in your browser
