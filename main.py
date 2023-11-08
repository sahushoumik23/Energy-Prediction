from dash import Dash, html, dcc, callback
from callbacks import get_callbacks
from datetime import datetime, date, timedelta
import plotly.graph_objs as go
import webbrowser

app = Dash()

app.layout = html.Div(
    [
        html.H1(children="Energy for Saram,Tamilnadu", style={"textAlign": "center"}),
        html.Div(
            id="graph_output",
            children=[
                html.Div(
                    id="hourly_date",
                    children=[
                        html.H3("Select a date"),
                        dcc.DatePickerSingle(
                            id="date-picker",
                            display_format="YYYY-MM-DD",
                            date=date.today(),
                            max_date_allowed=date.today() + timedelta(days=15),
                        ),
                    ],
                    style={
                        "textAlign": "center",
                    },
                )
            ],
        ),
        dcc.Loading(
            id="graph_loader",
            type="circle",
            children=[
                html.Div(
                    id="date-output",
                    style={"textAlign": "center", "marginTop": "10px"},
                ),
                html.Div(
                    id="process-output",
                    style={"textAlign": "center", "marginTop": "10px"},
                ),
                dcc.Graph(id="energy_output"),
            ],
        ),
    ]
)

get_callbacks(app)

webbrowser.open('http://localhost:8050')
app.run_server()
