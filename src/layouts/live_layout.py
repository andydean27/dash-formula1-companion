import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, State, dash_table, callback_context, callback, long_callback
import plotly.express as px
import plotly.graph_objects as go
import datetime

from app import app

from src.utils import openf1

from src.components import position_component

from assets.plotly_template import f1_graph_template


from dash.long_callback import DiskcacheLongCallbackManager
## Diskcache
import diskcache
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

df_tracks = pd.read_csv('assets/tracks.csv')

layout = [
    dcc.Interval(interval = 2.5*1000, id = 'interval_3'), # Used to query api every second
    dcc.Interval(interval = 5*1000, id = 'interval_5'), # Used to query api every 5 seconds
    dcc.Interval(interval = 20*1000, id = 'interval_20'), # Used to query api every 20 seconds
    html.Div([
        html.Div([
            html.Div(children = [], id = 'container-live-positions', className='live-position'),
            dcc.Graph(figure = {}, id = 'graph-live-positions', className='graph')
        ], className='visualisations-container vis-vertical'), 
        dcc.Graph(figure = {}, id = 'graph-live-track', className='graph'),
    ], className='visualisations-container vis-horizontal'),
    html.Div([
        dcc.Graph(figure = {}, id = 'graph-live-pace', className='graph'),
        dcc.Graph(figure = {}, id = 'graph-live-laps', className='graph')
    ], className='visualisations-container vis-horizontal')
]

@app.callback(
    Output('graph-live-track', 'figure'),
    Input('interval_3', 'n_intervals'),
    State('dashboard-location', 'pathname')
)
def update_track(n, path):
    
    # Check if live tab is selected to stop api calls if not return empties
    if path != 'live':
        return {}
    # Drivers
    df_drivers = openf1.fetch_drivers('latest')

    #Locations
    df_location = openf1.fetch_current_locations('latest')
    df_location = df_location.merge(df_drivers[[
        'driver_number',
        'name_acronym',
        'team_colour'
    ]], on = 'driver_number', how = 'left')

    df_session = openf1.get_session_details('latest')
    track = df_tracks.loc[df_tracks['circuit_key'].values == df_session['circuit_key'].values]

    team_colour_map = {name: (f'#{c}' if len(str(c))==6 else '#000000') for name, c in zip(df_drivers['name_acronym'], df_drivers['team_colour'])}

    graph_location = px.scatter(
        df_location,
        x = 'x',
        y = 'y',
        color='name_acronym',
        color_discrete_map=team_colour_map
    )
    graph_location.update_traces(
        marker={'size': 15})

    graph_track = px.line(
        df_tracks.loc[df_tracks['circuit_key'].values == df_session['circuit_key'].values],
        x = 'x',
        y = 'y',
        line_shape='spline'
    )
    graph_track.update_traces(line = dict(width=8, color='darkgrey'))

    graph_all = go.Figure(data = graph_track.data+graph_location.data)
    graph_all.layout.yaxis.scaleanchor='x'
    graph_all.update_layout(
        uirevision = True, template = f1_graph_template,
        title = dict(text=df_session['circuit_short_name'].values[0]),
        legend_title=None)
    graph_all.update_xaxes(visible=False)
    graph_all.update_yaxes(visible=False)

    # graph_track.add_trace(go.Scatter(
    #     x = track['x'],
    #     y = track['y'],
    #     mode='lines',
    #     line_shape = 'spline',
    #     line = dict(width=1, color='darkgrey')
    # ))
    # graph_track.layout.yaxis.scaleanchor='x'
    # graph_track.update_layout(uirevision = True)
    

    

    return graph_all

@app.callback(
    [Output('container-live-positions', 'children'),
     Output('graph-live-positions', 'figure')],
    Input('interval_5', 'n_intervals'),
    State('dashboard-location', 'pathname')
)
def update_live_plots_positions(n, path):
    # Check if live tab is selected to stop api calls if not return empties
    if path != 'live':
        return None, {}
    
    # Gather Data

    # Drivers
    df_drivers = openf1.fetch_drivers('latest')
    # Intervals
    df_intervals = openf1.fetch_current_intervals('latest')
    # Stints
    df_stints = openf1.fetch_stints('latest')
    df_stints_current = df_stints.groupby('driver_number').last().reset_index()
    # Positions
    df_positions = openf1.fetch_positions('latest')
    df_positions_current = df_positions.groupby('driver_number').last()
    df_positions_current['date'] = df_positions_current['date'].max()

    # Merge for all positions
    df_positions = df_positions.merge(df_drivers[[
        'driver_number',
        'name_acronym',
        'team_colour'
    ]], on = 'driver_number', how = 'left')
    

    # Merge for current positions
    df_positions_current = df_positions_current.merge(df_drivers[[
        'driver_number',
        'name_acronym',
        'team_colour'
    ]], on = 'driver_number', how = 'left')

    # Add rows of current positions at the latest time for plot to extend to end
    df_positions = pd.concat([
        df_positions,
        df_positions_current
    ])

    # Merge for current positions
    df_positions_current = df_positions_current.merge(df_intervals[[
        'driver_number',
        'interval',
        'gap_to_leader'
    ]], on = 'driver_number', how = 'left')
    # Merge for current positions
    df_positions_current = df_positions_current.merge(df_stints_current[[
        'driver_number',
        'stint_number',
        'compound'
    ]], on = 'driver_number', how = 'left')
    df_positions_current.fillna('-', inplace=True)

    

    # Sort positions
    df_positions_current.sort_values('position', inplace=True)

    result_positions = [
        position_component.position_component(pos)
        for i, pos in df_positions_current.iterrows()
    ]
    result_positions = [position_component.position_header()] + result_positions

    team_colour_map = {name: (f'#{c}' if len(str(c))==6 else '#000000') for name, c in zip(df_drivers['name_acronym'], df_drivers['team_colour'])}

    # Plot Positions
    graph_positions = px.line(
        df_positions, 
        x = 'date', 
        y = 'position',
        color='name_acronym',
        color_discrete_map=team_colour_map,
        line_shape='hv')
    graph_positions.update_yaxes(autorange='reversed')
    graph_positions.update_layout(
        uirevision=True, template = f1_graph_template,
        title = dict(text="Position"),
        legend_title=None, yaxis_title=None, xaxis_title=None)

    return result_positions, graph_positions



@app.callback(
    [Output('graph-live-pace', 'figure'),
     Output('graph-live-laps', 'figure')],
    Input('interval_20', 'n_intervals'),
    State('dashboard-location', 'pathname')
)
def update_live_plots_positions(n, path):
    # Check if live tab is selected to stop api calls if not return empties
    if path != 'live':
        return {}, {}

    # Gather Data
    # Drivers
    df_drivers = openf1.fetch_drivers('latest')

    # Stints
    df_stints = openf1.fetch_stints('latest')

    # Positions
    df_positions_current = openf1.fetch_positions('latest').groupby('driver_number').last().reset_index()

    # Laps
    df_laps = openf1.fetch_laps('latest')

    # Merge for all laps
    df_laps = df_laps.merge(df_drivers[[
        'driver_number',
        'name_acronym',
        'team_colour'
    ]], on = 'driver_number', how = 'left').reset_index()

    # Merge for all laps
    df_laps = df_laps.merge(df_positions_current[[
        'driver_number',
        'position'
    ]], on = 'driver_number', how = 'left').reset_index()

    team_colour_map = {name: (f'#{c}' if len(str(c))==6 else '#000000') for name, c in zip(df_drivers['name_acronym'], df_drivers['team_colour'])}

    df_laps.sort_values('position', inplace=True)

    graph_pace = px.box(
        df_laps.loc[df_laps['is_pit_out_lap']==False],
        x = 'name_acronym',
        y = 'lap_duration',
        color='name_acronym',
        color_discrete_map=team_colour_map
    )
    graph_pace.update_layout(yaxis_range = [
        df_laps['lap_duration'].quantile(0.25)/1.02,
        df_laps['lap_duration'].quantile(0.75)*1.05,],
        uirevision=True, template = f1_graph_template,
        title = dict(text="Pace by Driver"),
        legend_title=None, yaxis_title=None, xaxis_title=None)
    
    graph_laps = px.scatter(
        df_laps,
        x = 'lap_number',
        y = 'lap_duration',
        color='name_acronym',
        color_discrete_map=team_colour_map
    )
    graph_laps.update_layout(yaxis_range = [
        df_laps['lap_duration'].quantile(0.25)/1.02,
        df_laps['lap_duration'].quantile(0.75)*1.05,],
        uirevision=True, template = f1_graph_template,
        title = dict(text="Pace by Lap"),
        legend_title=None, yaxis_title=None, xaxis_title=None)

    return graph_pace, graph_laps