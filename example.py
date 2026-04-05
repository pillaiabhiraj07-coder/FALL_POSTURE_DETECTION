# Posture & Fall Detection - Configuration Example
# Copy this file and customize with your values

# ============================================
# TWILIO CONFIGURATION
# ============================================

TWILIO_CONFIG = {
    # Get these from https://www.twilio.com/console
    "account_sid": "AC6bb8caad6dda161d9b251f0a0d985365",
    "auth_token": "91498089ae6a7732b9f0ae1a31407a89",
    "from_number": "+141552388886",  # Twilio phone number
    "to_number": "+919326182564",    # Your phone number
    "enable_sms": False              # Set to True to enable
}

# ============================================
# CAMERA CONFIGURATION
# ============================================

CAMERA_CONFIG = {
    "camera_index": 0,              # 0 for default camera
    "width": 640,                   # Frame width
    "height": 480,                  # Frame height
    "fps": 30                       # Target frames per second
}

# ============================================
# DETECTION CONFIGURATION
# ============================================

DETECTION_CONFIG = {
    "confidence_threshold": 0.7,    # 0.5 to 1.0
    "tracking_confidence": 0.7,     # 0.5 to 1.0
    "model_complexity": 1,          # 0, 1, or 2 (higher = slower but more accurate)
    "smooth_landmarks": True,       # Smooth pose landmarks
}

# ============================================
# POSTURE DETECTION THRESHOLDS
# ============================================

POSTURE_THRESHOLDS = {
    "head_tilt_threshold": 0.05,    # Maximum head tilt allowed
    "shoulder_diff_threshold": 0.08, # Max shoulder height difference
    "spine_alignment_threshold": 0.15, # Max spine offset
    "hip_diff_threshold": 0.1,      # Max hip height difference
    "forward_head_threshold": 0.1   # Max forward head distance
}

# ============================================
# FALL DETECTION CONFIGURATION
# ============================================

FALL_CONFIG = {
    "fall_sensitivity": 0.5,        # 0.3 to 0.8 (higher = more sensitive)
    "confirmation_frames": 5,       # Frames needed to confirm fall
    "vertical_distance_threshold": -0.2,  # Knee-shoulder distance
    "nose_height_threshold": 0.75,  # Nose position from bottom
}

# ============================================
# ALERT CONFIGURATION
# ============================================

ALERT_CONFIG = {
    "alert_cooldown": 30,           # Seconds between alerts
    "sms_message": "ALERT: Fall detected at {time}. Please check on the person.",
    "enable_audio_alarm": True,     # Play beep sound
    "beep_frequency": 1000,         # Hz
    "beep_duration": 500,           # ms
    "beep_count": 3                 # Number of beeps
}

# ============================================
# LOGGING CONFIGURATION
# ============================================

LOGGING_CONFIG = {
    "log_level": "INFO",            # DEBUG, INFO, WARNING, ERROR
    "log_file": "posture_detection.log",
    "log_format": "%(asctime)s - %(levelname)s - %(message)s"
}

# ============================================
# UI CONFIGURATION
# ============================================

UI_CONFIG = {
    "page_title": "Posture & Fall Detection System",
    "layout": "wide",
    "theme": "dark",                # dark or light
    "show_landmarks": True,         # Show pose landmarks on video
    "show_angles": False,           # Show angle measurements
    "refresh_rate": 30              # UI refresh rate in FPS
}

# ============================================
# USAGE EXAMPLE
# ============================================

if __name__ == "__main__":
    print("Configuration Example Loaded")
    print(f"Twilio Enabled: {TWILIO_CONFIG['enable_sms']}")
    print(f"Camera Resolution: {CAMERA_CONFIG['width']}x{CAMERA_CONFIG['height']}")
    print(f"Detection Confidence: {DETECTION_CONFIG['confidence_threshold']}")