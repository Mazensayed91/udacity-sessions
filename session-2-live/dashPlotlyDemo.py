import pandas as pd

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

import plotly.express as px

df_activities = pd.read_csv("datasets/cardioActivities.csv", index_col='Date', parse_dates=True)
df_activities.Duration = df_activities.Duration.apply(lambda x: int(x.split(":")[0]) * 60 + int(x.split(":")[1]
                                                                                                if len(x) <= 5
                                                                                                else int(
    x.split(":")[0]) * 60 * 60 + int(x.split(":")[1]) * 60 + int(x.split(":")[2])))

df_activities['Year'] = df_activities.index.year

app = dash.Dash(__name__)
# years_dictionary = {}
# options_list = []
# for year in len(df_activities['Year'].value_counts.index):
#     years_dictionary["label"] = str(year)
#     years_dictionary["value"] = year
#     options_list.append(years_dictionary)

# Layout

app.layout = html.Div(
    [
        html.H1("Dash plotly demo"),
        dcc.Dropdown(id="select_year",
                     options=[
                         {"label": "2013", "value": 2013},
                         {"label": "2014", "value": 2014},
                         {"label": "2015", "value": 2015},
                         {"label": "2016", "value": 2016},
                         {"label": "2017", "value": 2017},
                         {"label": "2018", "value": 2018},
                     ],
                     multi=False,
                     value=2013,
                     style={'width': "40%"}),
        html.Div(id='output_year', children=[]),
        dcc.Graph(id="sports_graph", figure={})

    ]
)


# Logic


@app.callback([
    Output(component_id='output_year', component_property='children'),
    Output(component_id='sports_graph', component_property='figure'),
    Input(component_id='select_year', component_property='value')
])
def update(selected_year):
    container = "Chosen Year is : {}".format(selected_year)

    df_copy = df_activities.copy()
    df_copy = df_copy[df_copy['Year'] == selected_year]

    fig = px.scatter(df_copy, x='Duration', y='Distance (km)', size_max=55)

    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)
