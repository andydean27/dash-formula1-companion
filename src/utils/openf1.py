from urllib.request import urlopen
import json
from datetime import datetime, timedelta, timezone
from dateutil import parser 

import pandas as pd

def get_session_key_by_name(year: int, country_name: str, session_name: str):
    response = urlopen(f'https://api.openf1.org/v1/sessions?year={year}&country_name={country_name}&session_name={session_name}')
    data = json.loads(response.read().decode('utf-8'))
    
    return data[0]['session_key']

def get_all_sessions():
    response = urlopen(f'https://api.openf1.org/v1/sessions')
    data = json.loads(response.read().decode('utf-8'))
    df_data = pd.DataFrame(data)
    return df_data

def get_session_details(session_key):
    response = urlopen(f'https://api.openf1.org/v1/sessions?session_key={session_key}')
    data = json.loads(response.read().decode('utf-8'))
    df_data = pd.DataFrame(data)
    return df_data

def fetch_drivers(session_key):
    
    response = urlopen(f'https://api.openf1.org/v1/drivers?session_key={session_key}')
    
    data = json.loads(response.read().decode('utf-8'))
   
    df_data = pd.DataFrame(data)
    
    return df_data

def fetch_laps(session_key):
    response = urlopen(f'https://api.openf1.org/v1/laps?session_key={session_key}')
    data = json.loads(response.read().decode('utf-8'))
    df_data = pd.DataFrame(data)
    return df_data

def fetch_stints(session_key):
    response = urlopen(f'https://api.openf1.org/v1/stints?session_key={session_key}')
    data = json.loads(response.read().decode('utf-8'))
    df_data = pd.DataFrame(data)
    return df_data

def fetch_positions(session_key):
    response = urlopen(f'https://api.openf1.org/v1/position?session_key={session_key}')
    data = json.loads(response.read().decode('utf-8'))
    df_data = pd.DataFrame(data)
    return df_data

def fetch_debug_locations(session_key, start_time):
    # Fetches the latest location data, within 5s of now
    end_time = (start_time + timedelta(seconds = 1)).isoformat()
    query = f'https://api.openf1.org/v1/location?session_key={session_key}&date>{start_time.isoformat()}&date<{end_time}'
    response = urlopen(query)
    data = json.loads(response.read().decode('utf-8'))
    df_data = pd.DataFrame(data)

    if not df_data.empty:
        return df_data.groupby('driver_number').last().reset_index()

    
    return pd.DataFrame(columns = ['date', 'driver_number','meeting_key', 'session_key','x','y','z'])

def fetch_current_locations(session_key):
    # Fetches the latest location data, within 0.5s of now
    time = (datetime.now(timezone.utc) - timedelta(seconds = 0.5)).isoformat()

    response = urlopen(f'https://api.openf1.org/v1/location?session_key={session_key}&date>{time}')
    data = json.loads(response.read().decode('utf-8'))
    df_data = pd.DataFrame(data)

    if not df_data.empty:
        df_data = df_data.groupby('driver_number').last()
    
    return pd.DataFrame(columns = ['date', 'driver_number','meeting_key', 'session_key','x','y','z'])

def fetch_first_lap_locations(session_key, driver_number):
    df_laps = fetch_laps(session_key)
    
    
    # Parse start date
    start_time = parser.parse(
        df_laps.loc[(df_laps['driver_number']==driver_number) & (df_laps['lap_number']==2), 'date_start'].values[0]
    )
    lap_time = df_laps.loc[(df_laps['driver_number']==driver_number) & (df_laps['lap_number']==2), 'lap_duration'].values[0]
    # Calculate end date
    end_time = start_time + timedelta(seconds = lap_time)

    query = f'https://api.openf1.org/v1/location?session_key={session_key}&date>={start_time.isoformat()}&date<={end_time.isoformat()}&driver_number={driver_number}'
    print(query)
    response = urlopen(query)
    data = json.loads(response.read().decode('utf-8'))
    df_data = pd.DataFrame(data)

    return df_data

def fetch_current_intervals(session_key):
    
    # Fetches the latest location data, within 5s of now
    time = (datetime.now(timezone.utc) - timedelta(seconds = 5)).isoformat()

    response = urlopen(f'https://api.openf1.org/v1/intervals?session_key={session_key}&date>{time}')
    data = json.loads(response.read().decode('utf-8'))
    df_data = pd.DataFrame(data)

    if not df_data.empty:
        return df_data.groupby('driver_number').last()
    
    return pd.DataFrame(columns = ['date', 'driver_number', 'gap_to_leader', 'interval', 'meeting_key', 'session_key'])


if __name__ == "__main__":
    df_positions = fetch_current_locations('latest')
    print(df_positions)
    # print(df_positions.groupby('driver_number').last())