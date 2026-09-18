# AttendAI - Real-time Face Recognition Attendance System

AttendAI is a submission-ready mini project for a Computer Vision course. It uses real-time face recognition to automate classroom attendance, eliminating proxy attendance and saving time.

## Features
- **Enrollment**: Add new students with their roll number and face photo.
- **Live Recognition**: Real-time webcam processing to identify students and log their attendance.
- **Liveness Detection**: Simple spoofing protection to prevent the use of static photos.
- **Reporting**: View daily and historical attendance logs with export capabilities.

## Tech Stack
- **Language**: Python 3.10+
- **Computer Vision**: OpenCV, `face_recognition` (dlib)
- **Database**: SQLite3
- **Frontend**: Streamlit
- **Testing**: pytest

## Installation & Setup

1. **Clone the repository** (if not already done)
   ```bash
   git clone <repo_url>
   cd attendai
   ```

2. **Set up a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: `face_recognition` requires `dlib`, which in turn requires CMake and a C++ compiler to be installed on your system. If you face installation issues, install CMake and Visual Studio Build Tools (on Windows).*

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## Testing
Run the automated tests using `pytest`:
```bash
pytest
```

## Screenshots
*(Add screenshots of the Enroll, Live Attendance, and Reports tabs here)*

## Author
- **Name**: Manan Pandey
- **Registration Number**: 24BAI10033
