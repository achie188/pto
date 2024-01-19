import pandas as pd
import numpy as np
import sys

sys.path.append('/Users/achie188/Library/CloudStorage/GitHub/4CC/gkl')

from inputs.pull_sheets import import_gsheet, send_to_gsheet


def format_mmss(seconds):
    if np.isnan(seconds):
        return '0:00'
    elif seconds < 600:  # Less than 10 minutes
        return '{:01d}:{:02d}'.format(int(seconds // 60), int(seconds % 60), int((seconds % 60) * 1000)) 
    else:
        return '{:02d}:{:02d}'.format(int(seconds // 60), int(seconds % 60), int((seconds % 60) * 1000))

    

def process_row(row):
    if row['Lap'] != 'Finished':
        
        row['RandomTime'] = np.random.uniform(-5, 5)
        row['AdjustedTime'] = row['Time_secs'] + row['RandomTime']

        # Add 10 seconds to the adjusted times
        row['Time_secs'] = row['AdjustedTime'] + 30

    return row


def race_sim():

    df = import_gsheet("Live_race")

    df['Name'] = df['Name'].replace('', np.nan)
    df['Time_secs'] = df['Time_secs'].replace('', np.nan)
    df = df.dropna(subset=['Name'])
    df['Time_secs'] = df['Time_secs'].fillna(0)
    df['Lap'] = pd.to_numeric(df['Lap'], errors='coerce')

    df = df.apply(process_row, axis=1)

    df['Rank'] = df['Time_secs'].rank()
    df['Rank'] = round(df['Rank'])

    df['Time'] = df['Time_secs'].apply(format_mmss)

    df['Distance'] = df['Time_secs'] * 3.5
    df['Distance'] = df['Distance'].iloc[::-1].values
    df['Distance'] = df['Distance'].round(0)
    
    df['Lap'] = df['Distance'] / 500
    df['Lap'] = round(df['Lap'])

    if (df['Lap'] > 0).all(): 
        df['Last Lap'] = df['Time_secs'] / df['Lap']
        df['Last Lap'] = round(df['Last Lap'], 1)
        df['Last Lap'] = df['Last Lap'].apply(format_mmss)

    df.loc[df['Distance'] > 5000, 'Lap'] = 'Finished'

    if (df['Lap'] == 'Finished').all():
        df['Lap'] = 0
        df['Distance'] = 0
        df['Time'] = 0
        df['Time_secs'] = 0
        df['Last Lap'] = 0

    df = df.drop(columns=['RandomTime', 'AdjustedTime'])

    df = df.sort_values(by='Rank')
    df['Pts'] = df['Rank'].iloc[::-1].values

    send_to_gsheet(df, "Live_race")

    return df