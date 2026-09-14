import streamlit as st
import cv2
import numpy as np
import datetime
import time
from database.db import get_all_students
from modules.enrollment import process_enrollment
from modules.recognition import recognize_faces
from modules.liveness import is_live
from modules.attendance_logger import mark_attendance
from modules.reports import get_report_df

st.set_page_config(page_title="AttendAI", layout="wide")

st.markdown("""
<style>
/* Base theme adjustments */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

/* Watermark */
.watermark {
    position: fixed;
    bottom: 20px;
    right: 20px;
    opacity: 0.7;
    z-index: 1000;
    font-size: 16px;
    color: #cbd5e1;
    text-align: right;
    pointer-events: none;
    font-weight: 700;
    letter-spacing: 1px;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.8);
}

/* Glassmorphism for inputs and forms */
div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: 2rem;
}

/* Button styling */
button[data-testid="baseButton-secondary"], button[data-testid="baseButton-primaryFormSubmit"] {
    background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
    color: white !important;
    border: none;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: bold;
}
button[data-testid="baseButton-secondary"]:hover, button[data-testid="baseButton-primaryFormSubmit"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px -10px rgba(139, 92, 246, 0.5);
    border: none;
    color: white !important;
}
</style>

<div class="watermark">
    Manan Pandey<br>24BAI10033
</div>
""", unsafe_allow_html=True)

st.title("AttendAI: Face Recognition Attendance System")

# Create tabs
tab_enroll, tab_live, tab_reports = st.tabs(["Enrollment", "Live Attendance", "Reports"])

# --- TAB 1: Enrollment ---
with tab_enroll:
    st.header("Enroll New Student")
    with st.form("enroll_form"):
        name = st.text_input("Full Name")
        roll_no = st.text_input("Roll Number")
        
        # User can either use webcam or upload photo
        st.write("Provide a clear photo for enrollment (webcam or upload)")
        capture_img = st.camera_input("Take a photo")
        upload_img = st.file_uploader("Or upload an image", type=['jpg', 'jpeg', 'png'])
        
        submit = st.form_submit_button("Enroll")
        
        if submit:
            img_data = None
            if capture_img:
                img_data = capture_img.getvalue()
            elif upload_img:
                img_data = upload_img.getvalue()
                
            if img_data is not None:
                # Convert image to numpy array
                nparr = np.frombuffer(img_data, np.uint8)
                img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                with st.spinner("Processing face embedding..."):
                    success, msg = process_enrollment(img_bgr, name, roll_no)
                
                if success:
                    st.success(f"Successfully enrolled {name} ({roll_no})!")
                else:
                    st.error(f"Enrollment failed: {msg}")
            else:
                st.warning("Please provide a photo for enrollment.")


# --- TAB 2: Live Attendance ---
with tab_live:
    st.header("Live Attendance")
    st.write("Stand in front of the camera to mark your attendance.")
    
    run_camera = st.checkbox("Start Camera")
    FRAME_WINDOW = st.image([])
    status_text = st.empty()
    
    # We maintain a set in session state to avoid spamming the DB in one session block if desired
    # But our DB layer handles duplicate rejection nicely anyway.
    if 'marked_this_session' not in st.session_state:
        st.session_state['marked_this_session'] = set()

    if run_camera:
        # Get known students from DB
        known_students = get_all_students()
        
        if not known_students:
            st.warning("No students enrolled yet. Please enroll first.")
        else:
            # OpenCV Video Capture
            cap = cv2.VideoCapture(0)
            
            while run_camera:
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to grab frame from camera.")
                    break
                
                # Recognition
                # To maintain high FPS, we might not want to process every single frame
                # but for this mini-project, we'll process every frame or use a small delay
                results = recognize_faces(frame, known_students, tolerance=0.5)
                
                for res in results:
                    student_id = res['student_id']
                    name = res['name']
                    conf = res['confidence']
                    (top, right, bottom, left) = res['box']
                    
                    if name != "Unknown":
                        # Check liveness on the cropped face to be more robust, 
                        # but simple approach: check the whole frame or the bounding box
                        face_crop = frame[top:bottom, left:right]
                        if face_crop.size != 0:
                            live, fm = is_live(face_crop, threshold=50.0) # threshold might need tuning
                            
                            color = (0, 255, 0) # Green for match
                            text = f"{name} ({conf}%)"
                            
                            if not live:
                                color = (0, 0, 255) # Red for spoof
                                text = f"SPOOF DETECTED"
                            else:
                                # Log attendance
                                if student_id not in st.session_state['marked_this_session']:
                                    success, msg = mark_attendance(student_id, conf)
                                    if success:
                                        status_text.success(f"Attendance marked for {name}!")
                                        st.session_state['marked_this_session'].add(student_id)
                                    elif "Already marked" in msg:
                                        # To avoid spamming warning, just color yellow
                                        color = (0, 255, 255)
                                        text += " (Already Marked)"
                    else:
                        color = (0, 0, 255)
                        text = "Unknown"
                        
                    # Draw box and label
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    cv2.putText(frame, text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
                
                # Convert BGR to RGB for Streamlit displaying
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FRAME_WINDOW.image(rgb_frame)
                
                # Small sleep to free up CPU
                time.sleep(0.05)
                
            cap.release()


# --- TAB 3: Reports ---
with tab_reports:
    st.header("Attendance Reports")
    
    # Filter by Date
    today = datetime.date.today()
    filter_date = st.date_input("Select Date", today)
    
    if st.button("Refresh Report"):
        df = get_report_df(filter_date.strftime("%Y-%m-%d"))
        if df.empty:
            st.info(f"No attendance records found for {filter_date}.")
        else:
            st.dataframe(df, use_container_width=True)
            
            # CSV Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name=f'attendance_{filter_date}.csv',
                mime='text/csv',
            )
