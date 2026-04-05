#!/usr/bin/env python3
"""
Posture & Fall Detection System - Verification & Diagnostic Tool
Tests all dependencies and system readiness
"""

import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50)

def check_python_version():
    """Check Python version compatibility"""
    print_header("1. Python Version Check")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"Current Python: {version_str}")
    
    if version.major >= 3 and version.minor >= 13:
        print("✓ Python 3.13+ detected - COMPATIBLE")
        return True
    else:
        print(f"⚠ WARNING: Python 3.13+ required. You have {version.major}.{version.minor}")
        print("  Install from: https://www.python.org/downloads/")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name.lower().replace("-", "_")
    
    try:
        __import__(import_name)
        return True
    except ImportError:
        return False

def check_dependencies():
    """Check all required dependencies"""
    print_header("2. Dependency Check")
    
    dependencies = {
        "streamlit": "streamlit",
        "opencv-python": "cv2",
        "mediapipe": "mediapipe",
        "numpy": "numpy",
        "twilio": "twilio"
    }
    
    all_installed = True
    
    for package, import_name in dependencies.items():
        if check_package(package, import_name):
            print(f"✓ {package:20} installed")
        else:
            print(f"✗ {package:20} NOT installed")
            all_installed = False
    
    if not all_installed:
        print("\n⚠ Missing packages. Install with:")
        print("  pip install -r requirements.txt")
    
    return all_installed

def check_versions():
    """Check package versions"""
    print_header("3. Package Version Check")
    
    packages = {
        "streamlit": "streamlit",
        "cv2": "opencv_python",
        "mediapipe": "mediapipe",
        "numpy": "numpy",
        "twilio": "twilio"
    }
    
    for module_name, package_name in packages.items():
        try:
            module = __import__(module_name)
            version = getattr(module, "__version__", "unknown")
            print(f"{package_name:20} v{version}")
        except ImportError:
            print(f"{package_name:20} NOT INSTALLED")

def check_webcam():
    """Check webcam availability"""
    print_header("4. Webcam Check")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("✓ Webcam detected and accessible")
            
            # Get camera properties
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            print(f"  Resolution: {int(width)}x{int(height)}")
            print(f"  FPS: {fps}")
            
            if width >= 640 and height >= 480:
                print("  ✓ Resolution suitable for detection")
            else:
                print(f"  ⚠ Recommended: 640x480 or higher")
            
            cap.release()
            return True
        else:
            print("✗ Webcam not found or not accessible")
            print("  Check:")
            print("  - Webcam is connected")
            print("  - Camera permissions are granted")
            print("  - No other app is using the camera")
            return False
            
    except ImportError:
        print("✗ OpenCV not installed - cannot test webcam")
        return False
    except Exception as e:
        print(f"✗ Error checking webcam: {e}")
        return False

def check_mediapipe():
    """Test MediaPipe functionality"""
    print_header("5. MediaPipe Functionality Check")
    
    try:
        import mediapipe as mp
        print("✓ MediaPipe imported successfully")
        
        # Try to initialize pose model
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.7
        )
        print("✓ Pose model initialized successfully")
        
        pose.close()
        return True
        
    except ImportError:
        print("✗ MediaPipe not installed")
        return False
    except Exception as e:
        print(f"✗ Error initializing MediaPipe: {e}")
        return False

def check_twilio():
    """Check Twilio optional dependency"""
    print_header("6. Twilio SMS Support Check")
    
    try:
        from twilio.rest import Client
        print("✓ Twilio installed and ready")
        print("  Note: Credentials needed for SMS alerts")
        print("  Get free account: https://www.twilio.com/console")
        return True
    except ImportError:
        print("⚠ Twilio not installed (OPTIONAL)")
        print("  SMS alerts will be disabled")
        print("  To enable: pip install twilio")
        return False

def check_streamlit():
    """Test Streamlit functionality"""
    print_header("7. Streamlit Configuration Check")
    
    try:
        import streamlit
        print("✓ Streamlit installed successfully")
        print(f"  Version: {streamlit.__version__}")
        
        # Check streamlit config
        streamlit_dir = Path.home() / ".streamlit"
        if streamlit_dir.exists():
            print("✓ Streamlit config directory exists")
        else:
            print("⚠ Streamlit config directory not found")
            print("  Will be created on first run")
        
        return True
    except ImportError:
        print("✗ Streamlit not installed")
        return False

def check_system_resources():
    """Check system resources"""
    print_header("8. System Resources Check")
    
    try:
        import psutil
        
        # CPU
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"CPU: {cpu_count} cores @ {cpu_percent}% usage")
        
        # RAM
        ram = psutil.virtual_memory()
        ram_available = ram.available / (1024**3)
        ram_total = ram.total / (1024**3)
        print(f"RAM: {ram_available:.1f}GB / {ram_total:.1f}GB available")
        
        if ram_available >= 2:
            print("✓ Sufficient RAM available")
        else:
            print("⚠ WARNING: Low RAM available. Recommend 4GB minimum")
        
        return True
    except ImportError:
        print("⚠ psutil not installed - skipping resource check")
        print("  (Optional: pip install psutil)")
        return False

def check_network():
    """Check network connectivity"""
    print_header("9. Network Connectivity Check")
    
    try:
        import socket
        
        # Test internet connectivity
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        print("✓ Internet connection available")
        print("  Twilio SMS alerts will work")
        return True
    except (socket.timeout, socket.error):
        print("⚠ No internet connection detected")
        print("  SMS alerts will not work")
        print("  Other features will work locally")
        return False

def run_diagnostics():
    """Run all diagnostic checks"""
    
    print("\n")
    print("╔" + "="*48 + "╗")
    print("║  Posture & Fall Detection - System Check  ║")
    print("║         All Diagnostics v1.0              ║")
    print("╚" + "="*48 + "╝")
    
    checks = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
    }
    
    # Additional checks
    check_versions()
    check_webcam()
    check_mediapipe()
    check_twilio()
    check_streamlit()
    check_system_resources()
    check_network()
    
    # Summary
    print_header("Summary")
    
    if checks["Python Version"] and checks["Dependencies"]:
        print("✓ System is READY to run Posture & Fall Detection!")
        print("\n  Start with: streamlit run posture_fall_detection.py")
        return True
    else:
        print("✗ System is NOT ready. Please fix above issues.")
        print("\nTroubleshooting:")
        print("1. Install Python 3.13+")
        print("2. Run: pip install -r requirements.txt")
        print("3. Check webcam access permissions")
        print("\nFor help: See SETUP_GUIDE.md")
        return False

def create_system_info_file():
    """Create system info file for reference"""
    import platform
    
    info_file = Path("system_info.txt")
    
    with open(info_file, "w") as f:
        f.write("System Information\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Python: {sys.version}\n")
        f.write(f"Platform: {platform.platform()}\n")
        f.write(f"Machine: {platform.machine()}\n")
        f.write(f"Processor: {platform.processor()}\n\n")
        
        f.write("Installed Packages:\n")
        f.write("-" * 50 + "\n")
        
        packages = ["streamlit", "opencv-python", "mediapipe", 
                   "numpy", "twilio", "psutil"]
        for pkg in packages:
            try:
                result = subprocess.check_output(
                    [sys.executable, "-m", "pip", "show", pkg],
                    text=True
                )
                version = [line for line in result.split("\n") 
                          if line.startswith("Version:")][0]
                f.write(f"{pkg}: {version}\n")
            except:
                f.write(f"{pkg}: NOT INSTALLED\n")
    
    print(f"\nSystem info saved to: {info_file}")

if __name__ == "__main__":
    print("\n🔍 Running system diagnostics...\n")
    
    success = run_diagnostics()
    
    try:
        create_system_info_file()
    except Exception as e:
        print(f"\nCouldn't create system info file: {e}")
    
    print("\n" + "="*50)
    
    if success:
        print("Status: ✓ READY TO START")
        sys.exit(0)
    else:
        print("Status: ✗ NEEDS SETUP")
        sys.exit(1)