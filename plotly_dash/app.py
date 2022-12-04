from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
# Note you need to create a config.py file 
from config import db_username, db_password

# Database Setup using SQLAlchmy ORM
engine = create_engine(f"postgresql://{db_username}:{db_password}@localhost:5432/covid_modality_db")
conn = engine.connect()

app = Dash(__name__)

df1 = pd.read_sql("""SELECT state, round(cases_per_10k, 2) AS cases_per_10k
        FROM covid_df
        WHERE year = 2021;""",conn)

df2 = pd.read_sql("""SELECT state, round(cases_per_10k, 2) AS cases_per_10k
        FROM covid_df
        WHERE year = 2022;""",conn)

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
mytitle = dcc.Markdown(children='# App that Analyzes Covid Data for the Year 2021/2022')
mygraph = dcc.Graph(figure={})
dropdownGraph = dcc.Dropdown(options=['Bar Plot1', 'Scatter Plot'],
                        value='Bar Plot1',  # initial value displayed when page first loads
                        clearable=False)

dropdownYear = dcc.Dropdown(options=['2021', '2022'],
                        value='2021',  # initial value displayed when page first loads
                        clearable=False)

# Customize your own Layout
app.layout = dbc.Container([mytitle, mygraph, dropdownGraph, dropdownYear])

# Callback allows components to interact
@app.callback(
    Output(mygraph, component_property='figure'),
    Input(dropdownGraph, component_property='value'),
    Input(dropdownYear, component_property='value')
)
def update_graph(user_input_graph, user_input_year):  # function arguments come from the component property of the Input
    if user_input_year == '2021':
        if user_input_graph == 'Bar Plot1':
            fig = px.bar(df1, x="cases_per_10k", y="state", color="state")

        elif user_input_graph == 'Scatter Plot':
            fig = px.scatter(df1, x="cases_per_10k", y="state",
                    size="cases_per_10k", color="state", hover_name="cases_per_10k",
                    log_x=True, size_max=60)

    elif user_input_year == '2022':
        if user_input_graph == 'Bar Plot1':
            fig = px.bar(df2, x="cases_per_10k", y="state", color="state")

        elif user_input_graph == 'Scatter Plot':
            fig = px.scatter(df2, x="cases_per_10k", y="state",
                    size="cases_per_10k", color="state", hover_name="cases_per_10k",
                    log_x=True, size_max=60)
       
    return fig  # returned objects are assigned to the component property of the Output


# Run app
if __name__=='__main__':
    app.run_server(debug=True)