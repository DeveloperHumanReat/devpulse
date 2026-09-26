# DevPulse 🚀

DevPulse is a modern, lightweight, and customizable desktop widget designed for real-time system monitoring and developer productivity. Built with Python 3.14 and PyQt6, it features a frameless dark glassmorphism interface, smooth window animations, system tray integration, and an automated Windows installer setup.

✨ Key Features

🎨 Glassmorphism UI: Frameless, dark-mode floating widget with smooth entrance animations and drag support.

📊 Live Metrics: Real-time CPU and RAM monitoring powered by psutil.

🔔 System Tray Control: Runs quietly in the background with full system tray control.

📦 Complete Windows Packaging: Includes Inno Setup configuration (DevPulse.iss) to compile a single setup.exe installer.

📂 Project Structure

devpulse/
│
├── .venv/                  # Python 3.14 Virtual Environment
├── assets/                 # Application icons and asset creation tools
│   ├── create_icon.py      # Python script to generate application icons
│   ├── devpulse.ico        # Main application executable icon
│   └── devpulse.png        # High-resolution PNG logo
│
├── build/                  # PyInstaller compilation cache
│   └── DevPulse/           # Intermediate build artifacts (.toc, .pyz, pkg)
│
├── dist/                   # Compiled distribution packages
│   └── setup.exe           # Standalone Windows Installer setup
│
├── installer/              # Inno Setup compiler scripts
│   └── DevPulse.iss        # Inno Setup script for building setup.exe
│
├── widgets/                # Modular PyQt6 UI components & custom widgets
│   └── main_window.py      # Primary window controller and layout logic
│
├── .gitignore              # Version control ignore file
├── DevPulse.spec           # PyInstaller build specification
├── main.py                 # Application entry point and system tray logic
├── requirements.txt        # Core runtime dependencies (PyQt6, psutil)
└── requirements-build.txt  # Build dependencies (PyInstaller, Pillow)


🚀 Getting Started

Prerequisites

Python 3.14 (or Python 3.9+)

Windows 10 / 11

🔧 Local Setup & Run

Clone the repository:

git clone https://github.com/DeveloperHumanReat/devpulse.git
cd devpulse


Activate the virtual environment:

# On Windows
.venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Launch DevPulse:

python main.py


🛠️ Building & Packaging

1. Build Binary Executable (PyInstaller)

Install build tools and compile the executable using the spec file:

pip install -r requirements-build.txt
pyinstaller DevPulse.spec


2. Compile Windows Installer (Inno Setup)

Use Inno Setup Compiler to compile installer/DevPulse.iss. This produces the final setup executable in dist/setup.exe.

🛠️ Tech Stack

Language: Python 3.14

GUI Framework: PyQt6

System Metrics: psutil

Packaging: PyInstaller

Installer Engine: Inno Setup

👤 Author & Contact

Developer: DeveloperHumanReat

Email: developerhumanreat@gmail.com

GitHub: @DeveloperHumanReat

📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
