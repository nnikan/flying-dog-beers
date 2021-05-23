import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ---------- Import and clean data (importing csv into pandas)
df = pd.read_csv("https://raw.githubusercontent.com/Coding-with-Adam/Dash-by-Plotly/master/Other/Dash_Introduction/intro_bees.csv")
df1 = df.groupby(['State', 'Year'])[['Pct of Colonies Impacted']].sum()
df1.reset_index(inplace=True)
df1 = df1.pivot(index = 'State', columns = 'Year', values = 'Pct of Colonies Impacted')
print(df)


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018}],
                 multi=False,
                 value=2015,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    df2 = df["Year"] == option_slctd
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Express
    fig = px.imshow(df1, color_continuous_scale=px.colors.sequential.YlOrBr,
                title="test")
    fig.update_layout(title_font={'size':27}, title_x=0.5)
    fig.update_traces(hoverongaps=False,
                  hovertemplate="State: %{y}"
                                "<br>Year: %{x}"
                                "<br>Affected by Sum %: %{z}<extra></extra>"
                  )

   
    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)
