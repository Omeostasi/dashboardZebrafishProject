from dash import html, dcc
import dash_bootstrap_components as dbc
DEFAULT_STYLE = "bg-white rounded shadow-sm p-3"

def firstRow():
    return dbc.Row(
        dbc.Col(
            html.H1("Zebrafish Embryo Cell Type Visualization Dashboard",
                    className="text-center text-primary mb-4"),
            width=12
        ), className=DEFAULT_STYLE
    )