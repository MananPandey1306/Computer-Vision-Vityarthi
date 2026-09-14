import sqlite3
import numpy as np
import io
import os
import datetime

# Adapt numpy array to sqlite
def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

# Convert sqlite to numpy array
def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

# Register the adapters
sqlite3.register_adapter(np.ndarray, adapt_array)
sqlite3.register_converter("ARRAY", convert_array)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'attendance.db')

def get_connection():
    # detect_types allows sqlite to parse our custom ARRAY type
    return sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            embedding ARRAY NOT NULL,
            enrolled_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            confidence REAL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_student(name, roll_no, embedding):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (name, roll_no, embedding) VALUES (?, ?, ?)", 
                       (name, roll_no, embedding))
        conn.commit()
        return True, "Success"
    except sqlite3.IntegrityError:
        return False, "Roll number already exists."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, roll_no, embedding FROM students")
    rows = cursor.fetchall()
    conn.close()
    return rows

def has_marked_attendance_today(student_id, date_str=None):
    if date_str is None:
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM attendance WHERE student_id = ? AND date = ?", (student_id, date_str))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def log_attendance(student_id, confidence):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    if has_marked_attendance_today(student_id, date_str):
        return False, "Attendance already marked today."
        
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO attendance (student_id, date, time, confidence) VALUES (?, ?, ?, ?)",
                       (student_id, date_str, time_str, confidence))
        conn.commit()
        return True, "Attendance logged."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def get_attendance_report(date_str=None):
    conn = get_connection()
    query = '''
        SELECT a.date, a.time, s.name, s.roll_no, a.confidence
        FROM attendance a
        JOIN students s ON a.student_id = s.id
    '''
    params = ()
    if date_str:
        query += " WHERE a.date = ?"
        params = (date_str,)
        
    query += " ORDER BY a.date DESC, a.time DESC"
    
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

# Initialize DB on module import
init_db()
