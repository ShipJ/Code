import psycopg2 as ps
import pandas as pd
pd.set_option('display.width', 320)
from pylab import *

def read_redshift(pwd, query):
    conn = ps.connect(
        host='redshift-clustor.cndr1rlsl2px.eu-west-1.redshift.amazonaws.com',
        user='root',
        port=5439,
        password=pwd,
        dbname='autumnfair')
    return pd.read_sql_query(query, conn).dropna()


def cleaned(path, df):
    # Remove unwanted columns
    df = df.drop(['clientmac', 'type', 'probetime_gmt', 'probetime'], axis=1)
    # Rename column headers
    df.columns = ['id', 'datetime', 'sensor', 'proximity', 'power', 'rssi', 'accuracy']

    # Merge with stand locations
    sensor_stand_loc = pd.merge(
        pd.DataFrame(pd.read_csv(path.replace('BLE', 'Location', 1) + '/stand_locations.txt',
                                 sep='\t')),
        pd.DataFrame(pd.read_csv(path.replace('BLE', 'Location', 1) + '/sensor_locations.txt',
                                 sep='\t')),
        left_on='id', right_on='id_location').drop('id', axis=1)

    # Merge with location data
    df = pd.DataFrame(pd.merge(df,
                               sensor_stand_loc,
                               left_on='sensor',
                               right_on='name',
                               how='inner').drop(['name', 'type', 'id_sensor'], axis=1))

    # Enumerate IDs
    map_id = {id: i for i, id in enumerate(set(df['id']))}
    df['id'] = df['id'].map(map_id)
    # Enumerate Sensors
    map_sensors = {sensor: i for i, sensor in enumerate(set(df['sensor']))}
    df['sensor'] = df['sensor'].map(map_sensors)
    # Map datetime strings to datetime type
    df['datetime'] = pd.to_datetime(df['datetime'])
    # Convert floats to ints
    df['id_location'] = df['id_location'].astype(int)
    return df


def rssi_to_metres(df):
    """
    This non-linear function takes an RSSI (relative signal strength) reading, and converts it to a distance (in metres)
    :param df: 
    :return: 
    """
    df['ratio'] = np.where(df['rssi'] >= 0, None, df.rssi * (np.divide(1.0, df.power)))
    df['metres'] = pd.to_numeric(np.where(df['ratio'] < 1,
                                          np.power(df['ratio'], 10),
                                          np.multiply(0.89976, np.power(df['ratio'], 7.7095) + 0.111)))
    df = pd.DataFrame(df.drop(['ratio', 'power', 'accuracy', 'proximity', 'rssi'], axis=1))
    return df


def timestamped(df):
    df = df.sort_values('datetime').reset_index(drop=True)
    start_time = min(df.datetime)
    df['timestamp'] = df.groupby('id')['datetime'].apply(lambda x: (x - start_time).dt.total_seconds() / 60).astype(int)
    return df


def time_to_next(df):
    df = df.sort_values(['id', 'datetime']).reset_index(drop=True)
    df['time_diff'] = df['datetime'].diff().dt.total_seconds().fillna(0)
    journeys, journ = [], 0
    for index, row in df.iterrows():
        if row.time_diff > 600:
            journ += 1
        journeys.append(journ)
    df['journey'] = journeys
    df.loc[df['time_diff'] > 600, 'time_diff'] = 0
    return df


def get_sensor_coords(PATH, data):
    sensor_coords = pd.DataFrame(pd.read_csv(PATH.replace('BLE', 'Location/', 1) + '/sensor_coords.txt',
                                             sep='\t',
                                             usecols=['id_location', 'x', 'y']))
    name_loc = data[['sensor', 'id_location']].drop_duplicates().sort_values('sensor').reset_index(drop=True)
    return name_loc.merge(sensor_coords, on='id_location', how='inner')


def engineered(data):
    print '1. Converting RSSI to metres'
    rssi = rssi_to_metres(data)
    print '3. Filling missing minutes'
    timestamp = timestamped(rssi)
    print '4. Computing time difference\n'
    time_diff = time_to_next(timestamp)
    activity = np.zeros(len(time_diff))
    start = time_diff['sensor'].ix[0]
    j = 0
    for i in range(len(time_diff)):
        next = time_diff['sensor'].ix[i]
        if start == next:
            activity[i] = j
        else:
            j += 1
            activity[i] = j
        start = next
    time_diff['activity'] = activity
    b = time_diff.groupby(['id', 'sensor', 'id_location', 'activity', 'journey']).agg(
        {'metres': np.mean, 'time_diff': sum}).reset_index().sort_values(['journey', 'activity']).reset_index(drop=True)
    return b
