#import libraries
import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback

#loading the gapminder data
df = pd.read_csv("gdp_pcap.csv")

#checking data 
print(df.head())

melted_df = pd.melt(df, id_vars=['country'], var_name='year', value_name='gdp')

#check and displays df that has all the countries within a year --> year has separate col
melted_df.head(70)

min_year = int(melted_df["year"].min())
print(min_year)

max_year = int(melted_df["year"].max())
print(max_year)

print(type(max_year))

#getting rid of the Ks in the value column

def val_float(x):
    if type(x) == float or type(x)== int:
        return x #if it is a float or int, then keep as is
    if 'k' in x:
        if len(x) > 1 :
            return float(x.replace('k', '')) * 1000
        return 1000.0


melted_df['gdp'] = melted_df['gdp'].apply(val_float)

df = melted_df  # Assuming this contains the melted data

#import style sheets 
externalstylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # load the CSS stylesheet

app = Dash(__name__, external_stylesheets = externalstylesheets)

server = app.server

# Define layout
app.layout = html.Div([

    # Title and description
    html.Div([
        html.H1('App for GDP in Countries from Year 1800 - 2100'),
        html.P('Description: This is a dashboard that displays the GDP per capita of each country from the year 1800 to 2100. '
               'The data tracks 195 countries throughout the years and their respective GDPs.'
               'There is a dropdown and slider bar to select the country and years that you are interested in investigating.'
               'The data does include years past the current date, which are meant to serve as estimations of future GDP.')
    ]),

    # Dropdown for countries
    html.Div([
            dcc.Dropdown(
                options=[{'label': country, 'value': country} for country in df['country'].unique()],
                value= ['Afghanistan', 'Angola', 'Albania'],
                id='country-dropdown',
                multi=True
            ),
    ]),

    # Slider for years
    html.Div([
            dcc.RangeSlider(
                min = min_year, 
                max = max_year, 
                step = 1, 
                value = [1800,1950], #default, note array notation
                id = 'year-slider',
                marks = {year: str(year) for year in range(1800, 2101, 10)} 
                    #marks is a dict that represents the numerical values and the labels
                    #need to have a mark for everything from 1800 to 2100, thus make a for loop for each mark 
                ),
    ], style={'width': '90%', 'margin': 'auto'}),  # Center the slider

    # Graph
    dcc.Graph(id='country-graph')
])


@app.callback(
    Output('country-graph', 'figure'),
    [Input('country-dropdown', 'value'),
    Input('year-slider', 'value')]
)
def update_graph(selected_countries, selected_year):

    #initialize the selected df from choices
    selected_df = df

    #if countries selected then filter for those rows
    if selected_countries:
        selected_df = selected_df[selected_df['country'].isin(selected_countries)]
    #if year selected then filter --> need to convert to make year col all int so can compare against min&max
    if selected_year:
        min_year = selected_year[0]
        max_year = selected_year[1]
        selected_df = selected_df[(selected_df['year'].astype(int) >= min_year) & (selected_df['year'].astype(int) <= max_year)]

    fig = px.line(selected_df, x='year', y='gdp', color='country')

#update the layout
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='GDP per capita',
        legend_title='Country'
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


