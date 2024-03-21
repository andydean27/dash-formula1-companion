import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, dash_table, callback_context, callback, long_callback

def position_component(position: pd.DataFrame):
    """
    Takes a row of position data and returns dash layout to display data

    position is a combination of current position, driver, current interval data
    """
    team_colour = position['team_colour']

    div_style = {
        'border-color': f'#{team_colour}'
    }

    return html.Div(
        [
            html.H3(position['position'], style={'flex': 0.2}),
            html.H3("|||", style={'flex': 0.1}),
            html.H3(position['name_acronym'], style={'flex': 0.5}),
            html.H3(position['gap_to_leader'], style={'flex': 1}),
            html.H3(position['interval'], style={'flex': 1}),
            html.H3(position['compound'], style={'flex': 1}),
            html.H3(position['stint_number'], style={'flex': 1})
        ],
        className='position-container',
        style=div_style
    )

def position_header():
    """
    Takes a row of position data and returns dash layout to display data

    position is a combination of current position, driver, current interval data
    """

    # div_style = {
    #     'border-color': f'#{team_colour}'
    # }

    return html.Div(
        [
            html.H3("POS", style={'flex': 0.2}),
            html.H3("|||", style={'flex': 0.1}),
            html.H3("DRIVER", style={'flex': 0.5}),
            html.H3("GAP", style={'flex': 1}),
            html.H3("INTERVAL", style={'flex': 1}),
            html.H3("TYRE", style={'flex': 1}),
            html.H3("STINT", style={'flex': 1})
        ],
        className='position-container',
        # style=div_style
    )