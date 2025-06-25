from flask import Flask, render_template
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    today = datetime.now().strftime('%Y-%m-%d')
    file_path = os.path.join('Attendance', today, 'attendance.csv')

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=["Name", "IN", "OUT"])

    return render_template('attendance.html', table=df.to_dict(orient='records'), date=today)

if __name__ == '__main__':
    app.run(debug=True)



