# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                ],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                            min=0, max=10000, step=1000,
                                            marks={
                                                0: '0',
                                                2500: '2500',
                                                5000: '5000',
                                                7500: '7500',
                                                10000: '10000'},
                                            tooltip={'placement':'top', "always_visible": True},
                                            value=[min_payload, max_payload])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        All_LS = filtered_df.groupby('Launch Site')['class'].mean().reset_index()
        fig =px.pie(All_LS,
            values='class',
            names='Launch Site',
            title="Total Success Launches By Site"
        )
        return fig

    elif entered_site == 'CCAFS LC-40':
        entered_site_data = filtered_df[filtered_df['Launch Site'] == 'CCAFS LC-40']
        CCAFSLC_LS = entered_site_data.groupby('class')['Launch Site'].count().reset_index()
        fig =px.pie(CCAFSLC_LS,
            values='Launch Site',
            names='class',
            title="Total Success Launches for Site CCAFSLC LS-40"
        )
        return fig
    elif entered_site == 'VAFB SLC-4E':
        entered_site_data = filtered_df[filtered_df['Launch Site'] == 'VAFB SLC-4E']
        VAFBSLC_LS = entered_site_data.groupby('class')['Launch Site'].count().reset_index()
        fig =px.pie(VAFBSLC_LS,
            values='Launch Site',
            names='class',
            title="Total Success Launches for Site VAFB SLC-4E"
        )
        return fig
    elif entered_site == 'KSC LC-39A':
        entered_site_data = filtered_df[filtered_df['Launch Site'] == 'KSC LC-39A']
        KSCLC_LS = entered_site_data.groupby('class')['Launch Site'].count().reset_index()
        fig =px.pie(KSCLC_LS,
            values='Launch Site',
            names='class',
            title="Total Success Launches for Site KSC LC-39A"
        )
        return fig
    elif entered_site == 'CCAFS SLC-40':
        entered_site_data = filtered_df[filtered_df['Launch Site'] == 'CCAFS SLC-40']
        CCAFSSLC_LS = entered_site_data.groupby('class')['Launch Site'].count().reset_index()
        fig =px.pie(CCAFSSLC_LS,
            values='Launch Site',
            names='class',
            title="Total Success Launches for Site CCAFS SLC-40"
        )
        return fig
    return None
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site,payload_mass):
    filtered_df_cat = spacex_df
    if entered_site == 'ALL':
        cat_All = filtered_df_cat[(filtered_df_cat['Payload Mass (kg)'] >= payload_mass[0])]
        cat_All = cat_All[(filtered_df_cat['Payload Mass (kg)'] <= payload_mass[1])]
        fig =px.scatter(cat_All,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title="Correlation between Payload and Success for all Sites"
        )
        return fig
    elif entered_site == 'VAFB SLC-4E':
        entered_site_data_cat = filtered_df_cat[filtered_df_cat['Launch Site'] == 'VAFB SLC-4E']
        cat_VAFBSLC = entered_site_data_cat[(filtered_df_cat['Payload Mass (kg)'] >= payload_mass[0])]
        cat_VAFBSLC = cat_VAFBSLC[(filtered_df_cat['Payload Mass (kg)'] <= payload_mass[1])]
        fig =px.scatter(cat_VAFBSLC,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title="Correlation between Payload and Success for Site VAFB SLC-4E"
        )
        return fig
    elif entered_site == 'KSC LC-39A':
        entered_site_data_cat = filtered_df_cat[filtered_df_cat['Launch Site'] == 'KSC LC-39A']
        cat_KSCLC = entered_site_data_cat[(filtered_df_cat['Payload Mass (kg)'] >= payload_mass[0])]
        cat_KSCLC = cat_KSCLC[(filtered_df_cat['Payload Mass (kg)'] <= payload_mass[1])]
        fig =px.scatter(cat_KSCLC,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title="Correlation between Payload and Success for Site KSC LC-39A"
        )
        return fig
    elif entered_site == 'CCAFS LC-40':
        entered_site_data_cat = filtered_df_cat[filtered_df_cat['Launch Site'] == 'CCAFS LC-40']
        cat_CCAFSLC = entered_site_data_cat[(filtered_df_cat['Payload Mass (kg)'] >= payload_mass[0])]
        cat_CCAFSLC = cat_CCAFSLC[(filtered_df_cat['Payload Mass (kg)'] <= payload_mass[1])]
        fig =px.scatter(cat_CCAFSLC,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title="Correlation between Payload and Success for Site CCAFS LC-40"
        )
        return fig
    elif entered_site == 'CCAFS SLC-40':
        entered_site_data_cat = filtered_df_cat[filtered_df_cat['Launch Site'] == 'CCAFS SLC-40']
        cat_CCAFSSLC = entered_site_data_cat[(filtered_df_cat['Payload Mass (kg)'] >= payload_mass[0])]
        cat_CCAFSSLC = cat_CCAFSSLC[(filtered_df_cat['Payload Mass (kg)'] <= payload_mass[1])]
        fig =px.scatter(cat_CCAFSSLC,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title="Correlation between Payload and Success for Site CCAFS SLC-40"
        )
        return fig
    return None
# Run the app
if __name__ == '__main__':
    app.run_server()
