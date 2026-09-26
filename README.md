 # DevPulse 🚀

DevPulse is a modern, sleek, and lightweight desktop widget designed specifically for developers and power users. Built with Python and PyQt6, it brings real-time system monitoring, productivity tools, and quick note-taking directly to your desktop with a stunning glassmorphism interface.

 (Replace with actual screenshot)

✨ Features

🎨 Glassmorphism UI: Frameless, rounded, dark-themed user interface with subtle acrylic transparency.

📊 Real-time System Monitor: Live, animated tracking of CPU and RAM utilization powered by psutil.

⏱️ Focus / Pomodoro Timer: Keep your productivity high with customizable work/break timers.

📝 Quick Scratchpad: Instant sticky-notes area for quick commands, task lists, or reminders.

📌 Always-On-Top Toggle: Pin the widget over active windows or let it rest quietly on your desktop.

🔔 System Tray Integration: Easily minimize to the system tray for zero desktop clutter.

🛠️ Tech Stack

Language: Python 3.9+

GUI Framework: PyQt6

System Metrics: psutil

🚀 Quick Start

Prerequisites

Make sure you have Python installed on your system.

python --version


Installation

Clone the repository:

git clone https://github.com/your-username/devpulse.git
cd devpulse


Create a virtual environment (Optional but recommended):

# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt


Run the application:

python main.py


📂 Project Structure

devpulse/
│
├── assets/             # Icons, styling stylesheets, and images
├── widgets/            # Custom PyQt6 UI components
│   ├── system_monitor.py
│   ├── pomodoro.py
│   └── quick_notes.py
├── main.py             # Main entry point & window logic
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation


🤝 Contributing

Contributions are always welcome! If you'd like to report a bug or suggest a feature:

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📜 License

Distributed under the MIT License. See LICENSE for more information.
