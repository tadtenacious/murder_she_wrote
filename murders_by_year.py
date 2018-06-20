import pandas as pd

from bokeh.plotting import figure
from bokeh.layouts import row, widgetbox
from bokeh.models import Range1d
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.models.widgets import Select
from bokeh.io import output_file
from bokeh.io import curdoc

df = pd.read_csv('UCR65_16.csv')

def select_state():
    if states.value == 'All':
        selected = df[['YEAR','CLR','MRD']]
    else:
        selected = df[df['State']== states.value][['YEAR','CLR','MRD']]
    return selected

def create_figure():
    p = figure(plot_width=600, plot_height=400)
    use_df = select_state()
    agg = use_df.groupby('YEAR').sum()
    p.y_range=Range1d(0,agg['MRD'].max() * 1.05)
    p.yaxis[0].formatter = NumeralTickFormatter(format='0,0')
    p.line(agg.index,agg['MRD'], line_width=3,)
    p.line(agg.index,agg['CLR'], line_width=3, color='orange')
    p.title.text = '{} Murders by Year'.format(states.value)

    return p

def update(attr, old, new):
    layout.children[1] = create_figure()

states = Select(title='State', value='All',
               options= ['All']+df.State.unique().tolist())
states.on_change('value', update)

inputs = widgetbox(states, width=200)
layout = row( inputs, create_figure())

# update()
curdoc().add_root(layout)
curdoc().title = "Murders by Year"
