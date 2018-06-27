import pandas as pd

from bokeh.plotting import figure
from bokeh.layouts import layout, row, widgetbox
from bokeh.models import ColumnDataSource, Div, HoverTool, Range1d, ResetTool
from bokeh.models.formatters import NumeralTickFormatter
from bokeh.models.widgets import Select, Button
from bokeh.io import curdoc

df = pd.read_csv('SHR76_16.csv')

def add_all(column):
    return ['All'] + column.unique().tolist()

states = Select(title='State', value='All', options = add_all(df.fstate))
weapons = Select(title='Weapon', value='All', options = add_all(df.Weapon))
situations = Select(title='Situation', value='All',
              options= add_all(df.Situation))
circumstances = Select(title='Circumstance', value='All',
                options=add_all(df.Circumstance))
sources = Select(title='Source', value='All', options=['All','FBI','MAP'])
homicides = Select(title='Homicide', value='All', options=add_all(df.Homicide))
sexes = Select(title='Victim Sex', value='All', options=add_all(df.VicSex))
races = Select(title='Victim Race', value='All', options=add_all(df.VicRace))
controls = [
            states, weapons, situations, circumstances, sources, homicides,
            sexes, races,
]

refresh_button = Button(label='Clear Filters', button_type='primary')

def refresh():
    for i in controls:
        i.value = 'All'


inputs = widgetbox(refresh_button,*controls, sizing_mode='fixed', width=350)

def select_data():
    selected = df[['Year','Solved','fstate','Weapon','Situation','Circumstance',
                'Source','Homicide','VicSex','VicRace','ID']]
    state = states.value
    weapon = weapons.value
    situation = situations.value
    circumstance = circumstances.value
    source = sources.value
    sex = sexes.value
    homicide = homicides.value
    race = races.value
    if state != 'All':
        selected = selected[selected['fstate']==state]
    if weapon != 'All':
        selected = selected[selected['Weapon']==weapon]
    if situation != 'All':
        selected = selected[selected['Situation']==situation]
    if circumstance != 'All':
        selected = selected[selected['Circumstance']==circumstance]
    if source != 'All':
        selected = selected[selected['Source'] ==source]
    if sex != 'All':
        selected = selected[selected['VicSex']==sex]
    if homicide != 'All':
        selected = selected[selected['Homicide']==homicide]
    if race != 'All':
        selected = selected[selected['VicRace']==race]
    return selected

def pivot_data(selected):
    pvt = pd.pivot_table(selected[['Year','ID','Solved']],values='ID',
          index='Year',columns='Solved',aggfunc='count').reset_index()
    pvt.fillna(0,inplace=True)
    pvt['MRD'] = pvt['No'] + pvt['Yes']
    pvt['Clearance_Rate'] = pvt['Yes'] / pvt['MRD']
    return pvt

def create_figure():
    '''
    The main function to aggregate the data and create the figure.
    '''
    use_df = select_data() # Get the filtered dataframe
    agg = pivot_data(use_df) # aggregate the dataframe
    source = ColumnDataSource(agg) # put into a bokeh data structure
    hover = HoverTool( # Set the hover tools, ('Title', '@Column{formatting}'')
        tooltips = [
        ('Year', '@Year'),
        ('Total Murders','@MRD{0,0}'),
        ('Solved Murders','@Yes{0,0}'),
        ('Clearance Rate','@Clearance_Rate{0%}')
        ]
    )
    tools=[hover, ResetTool()]
    p = figure(plot_width=700, plot_height=500,tools=tools) # Create figure
    p.xaxis.axis_label = 'Year'
    p.yaxis.axis_label = 'Murders'
    # Set the range for the yaxis dynamically. Requires bokeh Rand1d object
    ymx = max(agg['MRD'].max(), agg['Yes'].max()) * 1.05
    p.y_range=Range1d(0,ymx)
    p.yaxis[0].formatter = NumeralTickFormatter(format='0,0')
    # Actually plot the lines now.
    p.line('Year','MRD',source=source, line_width=3,)
    p.line('Year','Yes',source=source, line_width=3, color='orange')
    p.title.text = '{} Murders by Year'.format(states.value) # dynamic title

    return p

lay_out = layout([
            [inputs,create_figure()]
], sizing_mode='fixed')

def update(attr, old, new):
    '''
    A function to update an element (the chart) within the layout.
    '''
    lay_out.children[0].children[1] = create_figure()

for i in controls:
    i.on_change('value', update)

curdoc().add_root(lay_out)
curdoc().title = 'Supplemental Crime Report' # sets the title of the tab in your browser
