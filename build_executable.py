#!/usr/bin/env python3
"""
Build script for creating a standalone executable of the Therapist Companion application.
This script uses PyInstaller to bundle the Python application into a single executable.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Build the executable using PyInstaller"""
    
    print("🚀 Building Therapist Companion Executable...")
    
    # Ensure we're in the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Clean previous builds
    if os.path.exists("dist"):
        print("🧹 Cleaning previous build...")
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # PyInstaller command
    cmd = [
        "C:/Users/subha/ai_assist/venv/Scripts/pyinstaller.exe",
        "--onefile",  # Create a single executable file
        "--windowed",  # Hide console window (for GUI apps)
        "--name=TherapistCompanion",  # Name of the executable
        "--add-data=assets;assets",  # Include assets folder
        "--add-data=.env;.",  # Include .env file
        "--hidden-import=pyttsx3.drivers",  # Ensure speech drivers are included
        "--hidden-import=pyttsx3.drivers.sapi5",  # Windows TTS
        "--hidden-import=google.genai",
        "--hidden-import=pygame",
        "main.py"
    ]
    
    try:
        print("🔨 Running PyInstaller...")
        subprocess.run(cmd, check=True)
        print("✅ Build completed successfully!")
        print(f"📦 Executable created at: {script_dir}/dist/TherapistCompanion.exe")
        
        # Instructions for distribution
        print("\n📋 Distribution Instructions:")
        print("1. Copy the entire 'dist' folder to the target machine")
        print("2. Ensure the target machine has:")
        print("   - Visual C++ Redistributable (for Windows)")
        print("   - Internet connection (for AI features)")
        print("3. Run TherapistCompanion.exe")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller not found. Please install it with: pip install pyinstaller")
        return False
    
    return True

def create_installer_script():
    """Create a simple batch script for easy installation"""
    
    installer_content = """@echo off
echo Installing Therapist Companion...

REM Create installation directory
if not exist "C:\\Program Files\\TherapistCompanion" (
    mkdir "C:\\Program Files\\TherapistCompanion"
)

REM Copy files
copy "TherapistCompanion.exe" "C:\\Program Files\\TherapistCompanion\\"
copy "assets\\*" "C:\\Program Files\\TherapistCompanion\\assets\\" /Y

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%userprofile%\\Desktop\\Therapist Companion.lnk');$s.TargetPath='C:\\Program Files\\TherapistCompanion\\TherapistCompanion.exe';$s.Save()"

echo Installation complete!
echo You can now run Therapist Companion from your desktop.
pause
"""
    
    with open("dist/install.bat", "w") as f:
        f.write(installer_content)
    
    print("📦 Created installer script: dist/install.bat")

if __name__ == "__main__":
    if build_executable():
        create_installer_script()
        print("\n🎉 Build process completed!")
        print("Your application is ready for distribution in the 'dist' folder.")