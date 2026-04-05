@echo off
REM Posture & Fall Detection - Python 3.11 Run Script

echo =============================================
echo  Posture & Fall Detection System
echo  Python 3.11 Launcher
echo =============================================
echo.

REM Check if venv exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Install dependencies
echo Installing dependencies from requirements_python311.txt...
pip install -r requirements_python311.txt
echo.

REM Run the app
echo.
echo =============================================
echo  Starting Streamlit App...
echo =============================================
echo.
echo Browser will open at: http://localhost:8501
echo.
echo Press Ctrl+C to stop the app
echo.
streamlit run app.py

pause