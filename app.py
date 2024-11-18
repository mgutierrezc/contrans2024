import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from contrans import contrans

ct = contrans()

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# create the dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# populate the layout
app.layout = html.Div([
    html.H1("Know Your Representatives in Elected Offices", style={"textAlign": "center"}),
    html.Div([dcc.Markdown("To find your representatives and senators, go here: [https://www.congress.gov/members/find-your-member](https://www.congress.gov/members/find-your-member)")
              ], style={"width": "25%", "float": "left"}),
    html.Div([
        dcc.Tabs([
            dcc.Tab(label="Bio and Contact Info", children=[

                ]),
            dcc.Tab(label="Ideology and Votes", children=[

                ]),
            dcc.Tab(label="Bills", children=[

                ]),
            dcc.Tab(label="News", children=[

                ]),
            dcc.Tab(label="Financial Contributors", children=[

                ])

        ])
    ], style={"width": "72%", "float": "right"})
])

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)