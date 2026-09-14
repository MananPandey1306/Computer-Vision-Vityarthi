from database.db import log_attendance, has_marked_attendance_today
import logging

# Set up logging for error handling
logging.basicConfig(filename='attendance_errors.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def mark_attendance(student_id, confidence):
    """
    Log attendance for a student if not already logged today.
    """
    try:
        if has_marked_attendance_today(student_id):
            return False, "Already marked today"
            
        success, msg = log_attendance(student_id, confidence)
        return success, msg
    except Exception as e:
        logging.error(f"Error marking attendance for student {student_id}: {e}")
        return False, "An error occurred while logging attendance"
