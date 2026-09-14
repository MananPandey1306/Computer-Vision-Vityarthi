# Architecture

## System Architecture
The system follows a modular 3-tier architecture:
1. **Presentation Layer (Frontend)**: A Streamlit-based web application providing a UI for Enrollment, Live Attendance, and Reports.
2. **Logic Layer (Backend)**: Python modules handling computer vision tasks (OpenCV for capturing, `face_recognition` for embedding extraction and matching, and liveness checks).
3. **Data Layer**: An SQLite database (`attendance.db`) storing student profiles, face embeddings (serialized), and attendance logs.

## Data Flow Workflow
1. **Enrollment**: 
   Streamlit UI → Capture Photo → `enrollment.py` extracts 128-d embedding → `db.py` saves to `students` table.
2. **Live Attendance**: 
   Streamlit UI Stream → `recognition.py` detects face and extracts embedding → Matches against embeddings in DB → `liveness.py` verifies liveness → `attendance_logger.py` logs entry if no duplicate exists for the day.
3. **Reporting**:
   Streamlit UI → `reports.py` queries `db.py` → Formats and displays data as DataFrames.

## Database Schema

### `students` Table
- `id` (INTEGER, Primary Key, Auto Increment)
- `name` (TEXT, Not Null)
- `roll_no` (TEXT, Not Null, Unique)
- `embedding` (BLOB, Not Null) - Serialized numpy array of the 128-d face embedding
- `enrolled_on` (TIMESTAMP, Default CURRENT_TIMESTAMP)

### `attendance` Table
- `id` (INTEGER, Primary Key, Auto Increment)
- `student_id` (INTEGER, Foreign Key referencing `students.id`)
- `date` (DATE, Not Null)
- `time` (TIME, Not Null)
- `confidence` (REAL)
