from database.db import get_attendance_report
import pandas as pd

def get_report_df(date_str=None):
    """
    Fetch attendance data and return as a pandas DataFrame.
    """
    rows = get_attendance_report(date_str)
    
    if not rows:
        return pd.DataFrame(columns=['Date', 'Time', 'Name', 'Roll Number', 'Confidence (%)'])
        
    df = pd.DataFrame(rows, columns=['Date', 'Time', 'Name', 'Roll Number', 'Confidence (%)'])
    return df
