import os
import pandas as pd
from datetime import datetime, timedelta

def mark_attendance_io(name):
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')

    folder_path = os.path.join('Attendance', date_str)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, 'attendance.csv')

    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=["Name", "IN", "OUT"])
    else:
        df = pd.read_csv(file_path)

    if name in df['Name'].values:
        row_index = df[df['Name'] == name].index[0]
        in_time = datetime.strptime(df.at[row_index, 'IN'], '%H:%M:%S')
        out_time = df.at[row_index, 'OUT']

        if (pd.isna(out_time) or out_time == '') and (datetime.strptime(time_str, '%H:%M:%S') - in_time > timedelta(seconds=30)):
            df.at[row_index, 'OUT'] = time_str
    else:
        df.loc[len(df)] = [name, time_str, '']

    df.to_csv(file_path, index=False)

