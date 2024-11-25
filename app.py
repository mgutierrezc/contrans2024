import numpy as np
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from contrans import contrans
import plotly.figure_factory as ff
ct = contrans()
server, engine = ct.connect_to_postgres(ct.POSTGRES_PASSWORD, host='postgres')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Create fixed variables for use in the dashboard

myquery = '''
SELECT *
FROM members
ORDER BY lastname
'''
members = pd.read_sql_query(myquery, con=engine)  

bioguides = members['bioguideid']
displayname = members['firstname'] + ' ' + members['lastname'] + ' (' + members['partyletter'] + ', ' + members['state'] + '-' + members['district'] + ')'

dropdown_options = [{'label': y, 'value': x} for x, y in zip(bioguides, displayname)]

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Populate the layout
app.layout = html.Div([
    html.H1("Know Your Representatives in Elected Offices", style={'text-align': 'center'}),
    html.Div([
        dcc.Markdown('To find your representative and Senators, go here: [https://www.congress.gov/members/find-your-member](https://www.congress.gov/members/find-your-member)'),
        dcc.Markdown('Select your representative or Senator here:'),
        dcc.Dropdown(id='dropdown', options=dropdown_options, value='N000188')
        ], style={'width': '25%', 'float': 'left'}),
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Bio and Contact Info', children=[
                html.Div([
                    html.Img(id = 'bioimage', style={'height':'100%', 'width':'100%'})
                ], style={'width': '28%', 'float': 'left'}),
                html.Div([
                    dcc.Graph(id='biotable')
                ], style={'width': '68%', 'float': 'right'}),
            ]),
            dcc.Tab(label='Ideology and Votes', children=[
                dcc.Graph(id = 'ideograph'),
                dcc.Markdown('This person votes very similarly to the following people:'),
                dcc.Graph(id = 'agreetable'),
                dcc.Markdown('This person rarely votes the same was as the following people:'),
                dcc.Graph(id = 'disagreetable')
            ]),
            dcc.Tab(label='Bills', children=[

            ]),
            dcc.Tab(label='News', children=[
                
            ]),
            dcc.Tab(label='Financial Contributors', children=[
                
            ])
        ])
    ], style={'width':'72%', 'float': 'right'}),    
])

# Define the callbacks

@app.callback([Output(component_id = 'biotable', component_property = 'figure')],
             [Input(component_id = 'dropdown', component_property = 'value')])

def biotable(b):
    myquery = f'''
    SELECT name AS Name,
        partyname AS Party,
        state AS State,
        district AS District,
        CAST((2024 - born) AS INT) AS Age
    FROM members
    WHERE bioguideid='{b}'
    '''
    mydf = pd.read_sql_query(myquery, con=engine)
    mydf.columns = [x.capitalize() for x in mydf.columns]
    mydf = mydf.T.reset_index()
    mydf = mydf.rename({'index':'', 0:''}, axis=1)
    return [ff.create_table(mydf)]

@app.callback([Output(component_id = 'bioimage', component_property = 'src')],
             [Input(component_id = 'dropdown', component_property = 'value')])

def bioimage(b):
    myquery = f'''
    SELECT depiction_imageurl
    FROM members
    WHERE bioguideid='{b}'
    '''
    mydf = pd.read_sql_query(myquery, con=engine)
    return [mydf['depiction_imageurl'][0]]

@app.callback([Output(component_id = 'ideograph', component_property = 'figure')],
             [Input(component_id = 'dropdown', component_property = 'value')])

def ideograph(b):
    return [ct.plot_ideology(b, host='postgres')]

@app.callback([Output(component_id = 'agreetable', component_property = 'figure')],
             [Input(component_id = 'dropdown', component_property = 'value')])

def agreetable(b):
    agreedf, disagreedf = ct.make_agreement_df(b, host='postgres')
    return [ff.create_table(agreedf)]

@app.callback([Output(component_id = 'disagreetable', component_property = 'figure')],
             [Input(component_id = 'dropdown', component_property = 'value')])

def disagreetable(b):
    agreedf, disagreedf = ct.make_agreement_df(b, host='postgres')
    return [ff.create_table(disagreedf)]


# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)