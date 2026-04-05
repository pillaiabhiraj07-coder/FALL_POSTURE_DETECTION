#!/usr/bin/env python3
"""
Posture & Fall Detection - Quick Demo Script
Test pose detection without Streamlit (useful for debugging)
"""

import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import sys

class SimplePostureDemo:
    """Simple posture detection demo for testing"""
    
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Landmark indices
        self.NOSE = 0
        self.LEFT_SHOULDER = 11
        self.RIGHT_SHOULDER = 12
        self.LEFT_HIP = 23
        self.RIGHT_HIP = 24
        self.LEFT_EAR = 7
        self.RIGHT_EAR = 8
        self.LEFT_KNEE = 25
        self.RIGHT_KNEE = 26
        
        self.fall_history = deque(maxlen=15)
        self.frame_count = 0
        self.fall_count = 0
    
    def calculate_angle(self, p1, p2, p3):
        """Calculate angle between three points"""
        try:
            a = np.array([p1.x, p1.y])
            b = np.array([p2.x, p2.y])
            c = np.array([p3.x, p3.y])
            
            ba = a - b
            bc = c - b
            
            cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
            cos_angle = np.clip(cos_angle, -1, 1)
            angle = np.arccos(cos_angle)
            return np.degrees(angle)
        except:
            return 0
    
    def analyze_posture(self, landmarks):
        """Simple posture analysis"""
        if not landmarks:
            return 50, "No person detected"
        
        try:
            nose = landmarks[self.NOSE]
            left_ear = landmarks[self.LEFT_EAR]
            right_ear = landmarks[self.RIGHT_EAR]
            left_shoulder = landmarks[self.LEFT_SHOULDER]
            right_shoulder = landmarks[self.RIGHT_SHOULDER]
            left_hip = landmarks[self.LEFT_HIP]
            right_hip = landmarks[self.RIGHT_HIP]
            
            score = 100
            
            # Head tilt
            head_tilt = abs(left_ear.y - right_ear.y)
            if head_tilt > 0.05:
                score -= 15
            
            # Shoulder alignment
            shoulder_diff = abs(left_shoulder.y - right_shoulder.y)
            if shoulder_diff > 0.08:
                score -= 20
            
            # Spine alignment
            nose_to_shoulder_x = abs(nose.x - (left_shoulder.x + right_shoulder.x) / 2)
            if nose_to_shoulder_x > 0.15:
                score -= 25
            
            # Hip alignment
            hip_diff = abs(left_hip.y - right_hip.y)
            if hip_diff > 0.1:
                score -= 15
            
            # Forward head
            forward_head = right_ear.x - nose.x
            if forward_head > 0.1:
                score -= 20
            
            score = max(0, min(100, score))
            
            if score >= 75:
                status = "GOOD"
            elif score >= 50:
                status = "FAIR"
            else:
                status = "POOR"
            
            return score, status
        except:
            return 50, "ERROR"
    
    def detect_fall(self, landmarks):
        """Simple fall detection"""
        if not landmarks:
            return False
        
        try:
            nose = landmarks[self.NOSE]
            left_knee = landmarks[self.LEFT_KNEE]
            right_knee = landmarks[self.RIGHT_KNEE]
            left_shoulder = landmarks[self.LEFT_SHOULDER]
            right_shoulder = landmarks[self.RIGHT_SHOULDER]
            
            avg_shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
            avg_knee_y = (left_knee.y + right_knee.y) / 2
            
            vertical_distance = avg_knee_y - avg_shoulder_y
            nose_height = nose.y
            
            is_fallen = (vertical_distance < -0.2 and nose_height > 0.6) or \
                       (nose_height > 0.75 and avg_shoulder_y > 0.7)
            
            self.fall_history.append(is_fallen)
            fall_confirmed = sum(self.fall_history) >= 5
            
            return fall_confirmed
        except:
            return False
    
    def run(self):
        """Run demo"""
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("\n" + "="*60)
        print("  Posture & Fall Detection - DEMO MODE")
        print("="*60)
        print("\nInstructions:")
        print("  - Good Posture: Sit straight, shoulders back")
        print("  - Poor Posture: Slouch or bend forward")
        print("  - Fall: Bend down significantly")
        print("  - Press 'q' to quit")
        print("\n" + "="*60 + "\n")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            h, w, c = frame.shape
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_frame)
            
            self.frame_count += 1
            
            if results.pose_landmarks:
                # Draw pose
                self.mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing.DrawingSpec(
                        color=(0, 255, 0), thickness=2, circle_radius=2
                    ),
                    connection_drawing_spec=self.mp_drawing.DrawingSpec(
                        color=(0, 200, 0), thickness=2
                    )
                )
                
                landmarks = results.pose_landmarks.landmark
                
                # Analyze posture
                score, status = self.analyze_posture(landmarks)
                
                # Detect fall
                fall_detected = self.detect_fall(landmarks)
                if fall_detected:
                    self.fall_count += 1
                
                # Display info
                color = (0, 255, 0) if status == "GOOD" else \
                       (0, 165, 255) if status == "FAIR" else (0, 0, 255)
                
                cv2.putText(frame, f"Posture Score: {score}%",
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                cv2.putText(frame, f"Status: {status}",
                           (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                
                if fall_detected:
                    cv2.putText(frame, "!!! FALL DETECTED !!!",
                               (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                    print(f"\n⚠️  FALL #{self.fall_count} detected at frame {self.frame_count}")
            
            else:
                cv2.putText(frame, "No person detected", (50, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
            
            # Display stats
            cv2.putText(frame, f"Frame: {self.frame_count}",
                       (w-250, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)
            cv2.putText(frame, f"Falls: {self.fall_count}",
                       (w-250, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)
            
            # Show frame
            cv2.imshow("Posture & Fall Detection Demo", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        print("\n" + "="*60)
        print(f"  Demo Complete!")
        print(f"  Total Frames: {self.frame_count}")
        print(f"  Falls Detected: {self.fall_count}")
        print("="*60 + "\n")


def test_imports():
    """Test if all required packages are available"""
    print("\nChecking imports...")
    
    packages = {
        "cv2": "OpenCV",
        "mediapipe": "MediaPipe",
        "numpy": "NumPy"
    }
    
    all_ok = True
    for module, name in packages.items():
        try:
            __import__(module)
            print(f"  ✓ {name} imported successfully")
        except ImportError:
            print(f"  ✗ {name} NOT installed")
            all_ok = False
    
    return all_ok


def main():
    """Main entry point"""
    
    if not test_imports():
        print("\n⚠️  ERROR: Missing required packages")
        print("Install with: pip install -r requirements.txt")
        return 1
    
    try:
        demo = SimplePostureDemo()
        demo.run()
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())