import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback

df = pd.DataFrame({
    "hpf": ["0", "2", "1"],
    "gene0" : [0, 3, 6],
    "gene1" : [0, 1, 0],
    "Type": ["0", "1", "2"]
})


app = Dash()

app.layout = html.Div([
    html.H1("Zebrafish Gene Expression Dashboard"),

    # Dropdown menus
    html.Div([
        html.H3("Select hours post fertilization (hpf)"),
        # Choosing hpf
        dcc.Dropdown(id = 'hpf-dropdown-scatter',
                 options= [h for h in np.sort(df['hpf'].unique())],
                 value=np.sort(df['hpf'].unique())[0]),
    ],style={'width': '48%', 'display': 'inline-block'}),
    # Choosing type
    html.Div([
        html.H3('Select Type of tissue'),
        dcc.Dropdown(
            id= "type-dropdown-scatter",
            options=[t for t in np.sort(df["Type"].unique())],
            value=np.sort(df["Type"].unique())[0]
        )
    ],style={'width': '48%', 'display': 'inline-block', 'float':'right'}),

    # Basic scatter gene0 - gene 1
    html.Div([
        dcc.Graph(
            id= 'scatter-hpf-type-selected',
        )
    ]),

    # Facet version of scatter plot with multi choice dropdown
    # drop down multi choice
    html.Div([
        html.H3("Select hpf (multiple choices possible)"),
        dcc.Dropdown(
            id= "hpf-dropdown-scatter-facet",
            options=[h for h in np.sort(df['hpf'].unique())],
            value=[np.sort(df['hpf'].unique())[0]],
            multi=True)
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        html.H3('Select Type of tissue'),
        dcc.Dropdown(
            id= "type-dropdown-scatter-facet",
            options=[t for t in np.sort(df["Type"].unique())],
            value=[np.sort(df["Type"].unique())[0]],
            multi=True
        )
    ],style={'width': '48%', 'display': 'inline-block', 'float':'right'}),

    # Creating facet graph
    html.Div(
        dcc.Graph(
            id='facet-scatter',
        )
    )

                                 
 ])




# Defining callbacks
@callback(
    Output(component_id="scatter-hpf-type-selected", component_property='figure'),
    Input(component_id='hpf-dropdown-scatter', component_property= 'value'),
    Input(component_id='type-dropdown-scatter', component_property= 'value'),
)
def update_scatter_hpf_type_selected(hpf, type):
    df_filtered = df[(df['hpf'] == hpf) & (df['Type'] == type)] 
    fig = px.scatter(df_filtered, x="gene0", y="gene1", color="Type", custom_data=[df_filtered.index])
    fig.update_traces(hovertemplate="index= %{customdata}")
    return fig


@callback(
    Output(component_id="facet-scatter", component_property='figure'),
    Input(component_id='hpf-dropdown-scatter-facet', component_property= 'value'),
    Input(component_id='type-dropdown-scatter-facet', component_property= 'value')
)
def update_scatter_facet_hpf_type_selected(hpf, type):
    if hpf is None:
        hpf = [h for h in np.sort(df['hpf'].unique())]
    if type is None:
        type = [t for t in np.sort(df["Type"].unique())]
    df_filtered = df[(df['hpf'].isin(hpf)) & (df['Type'].isin(type))]
    fig = px.scatter(df_filtered, x="gene0", y="gene1", color="Type", facet_col="hpf", custom_data=[df_filtered.index])
    fig.update_traces(hovertemplate="index= %{customdata}")
    return fig






if __name__ == '__main__':
    app.run(debug=True)