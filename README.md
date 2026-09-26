# DevPulse 🚀

DevPulse is a modern, lightweight, and customizable desktop widget designed for real-time system monitoring and productivity. Built with Python 3.14 and PyQt6, it features a frameless dark glassmorphism interface, smooth window animations, and system tray integration.

✨ Key Features

🎨 Modern Glassmorphism UI: Frameless, dark-mode window with custom title bar interactions and smooth entry animations (show_animated()).

📊 Live System Monitoring: Real-time tracking of CPU and RAM usage powered by psutil.

🔔 System Tray Integration: Runs quietly in the background without cluttering your taskbar.

📦 Executable Ready: Configured with PyInstaller for single-click .exe standalone distribution.

📂 Project Structure

devpulse/
│
├── assets/                 # Icons (devpulse.ico), styles, and UI resources
├── build/                  # PyInstaller build artifacts
├── dist/                   # Compiled standalone binaries (DevPulse.exe)
├── installer/              # Installer payload & packaging scripts
├── widgets/                # Modular PyQt6 UI components & main window logic
│   └── main_window.py      # Core window controller and animations
├── .gitignore              # Git ignore rules for venv, build, and Python artifacts
├── DevPulse.spec           # PyInstaller build specification
├── main.py                 # Application entry point & tray setup
├── pyvenv.cfg              # Python virtual environment configuration
├── requirements.txt        # Runtime dependencies (PyQt6, psutil)
├── requirements-build.txt  # Build & packaging dependencies (PyInstaller, Pillow)
└── README.md               # Project documentation


🚀 Getting Started

Prerequisites

Python 3.9+ (Tested on Python 3.14)

Windows 10/11 (or Linux/macOS with PyQt6 support)

🔧 Local Setup & Execution

Clone the repository:

git clone https://github.com/DeveloperHumanReat/devpulse.git
cd devpulse


Create and activate a virtual environment:

# Windows (Command Prompt / PowerShell)
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate


Install runtime dependencies:

pip install -r requirements.txt


Run the application:

python main.py


🛠️ Building Standalone Executable (.exe)

To build a windowed, standalone .exe using PyInstaller:

Install build requirements:

pip install -r requirements-build.txt


Run PyInstaller with the spec file:

pyinstaller DevPulse.spec


Locate your executable:
Find your standalone binary in the dist/ directory:

dist/DevPulse.exe


🛠️ Tech Stack

Language: Python 3.14

GUI Framework: PyQt6

System Metrics: psutil

Executable Packaging: PyInstaller

Image Utilities: Pillow

👤 Author & Contact

Developed by DeveloperHumanReat.

Developer: DeveloperHumanReat

Email: developerhumanreat@gmail.com

GitHub: @DeveloperHumanReat

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
