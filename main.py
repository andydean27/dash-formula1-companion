import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, dash_table, callback_context, callback
from dash.exceptions import PreventUpdate

from app import app

from src.layouts import live_layout





def serve_layout():

    layout = html.Div([
        # Location
        dcc.Location(id = 'dashboard-location', pathname='home', refresh=False),
        # Header
        html.Div([
            html.Div([
                html.H1('F1 Dashboard', className='header-title')
            ]),
            # Navigation
            html.Div([
                html.Button('Live', id = 'nav-live', className='header-button'),
                html.Button('Historic', id = 'nav-historic', className='header-button')
            ]),
        ], className = 'header-container'),
        # Content
        html.Div([], id = 'div-content', className='content-container vis-vertical')
    ])

    return layout

@app.callback(
    Output('dashboard-location', 'pathname'),
    [Input('nav-live', 'n_clicks')]
)
def update_path(n1):
    button_id = callback_context.triggered_id if not None else "no clicks yet"

    if button_id == 'nav-live':
        return 'live'
    if button_id == 'nav-historic':
        return 'historic'

    return 'home'

@app.callback(
    Output('div-content', 'children'),
    Input('dashboard-location', 'pathname'),
)
def update_content(path):
    if path == 'live':
        return live_layout.layout
    if path == 'historic':
        pass
    else:
        raise PreventUpdate


if __name__ == "__main__":
    app.layout = serve_layout
    app.run_server(host="0.0.0.0", port=8050, debug=True)  