# Advanced Interactive Hangman Game 🎯 ASCII Edition

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style: PEP8](https://img.shields.io/badge/code%20style-PEP8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

A feature-packed, production-ready Command Line Interface (CLI) Hangman Game built in Python. Designed for the **InternGrow Python Programming Track – Task 1**.

This application features dynamic remote word fetching via Heroku API, automatic offline word bank fallback, difficulty customization, rich ANSI terminal coloring via Colorama, live game timers, win streak tracking, hint systems, and persistent JSON statistics storage.

---

## 📌 GitHub Repository Information

### 📝 Repository Description
> A production-ready, interactive Python CLI Hangman Game featuring real-time API word fetching, automatic offline fallback, dynamic ANSI terminal graphics, hint mechanics, persistent scoreboards, and statistics tracking.

### 🏷️ GitHub Topics
`python`, `hangman-game`, `cli-game`, `object-oriented-programming`, `colorama`, `rest-api`, `python3`, `terminal-app`, `game-development`, `interngrow`

---

## ✨ Features

- **🌐 Live REST API Integration**: Fetches fresh words from `https://random-word-api.herokuapp.com/word`.
- **🔄 Robust Fallback Engine**: Seamlessly switches to local categorized word bank if network fails or API times out.
- **🎨 Vibrant Terminal UI**: Styled using `Colorama` with ASCII art, colored alerts, and dynamic screen clearing.
- **⚙️ 3 Difficulty Levels**:
  - **Easy**: 8 attempts, 4-6 letter words, 2 hints available.
  - **Medium**: 6 attempts, 6-8 letter words, 1 hint available.
  - **Hard**: 5 attempts, 8+ letter words, 0 hints available.
- **🧠 Interactive Hint System**: Reveal unrevealed letters when stuck.
- **⏱️ Real-Time Timer**: Tracks completion speed and calculates bonus points.
- **🔥 Win Streak Counter**: Measures continuous session victories.
- **📊 Persistent JSON Statistics & Leaderboard**: Stores player history, high scores, total games, win rate %, and fastest win times in `scores.json`.
- **🛡️ Complete Input Validation**: Prevents duplicate guesses, invalid special characters, and numbers without penalizing attempts.

---

## 📁 Project Structure

```
Advanced_Hangman/
│
├── main.py                # Main CLI entry point & user interface menu
├── game.py                # Core HangmanGame logic & round state manager
├── api.py                 # Remote REST API client with fallback mechanism
├── words.py               # Categorized offline WordBank
├── score.py               # JSON score persistence & leaderboard algorithm
├── utils.py               # Colorama styling, clear screen & ASCII parser
├── requirements.txt       # Dependencies manifest
├── README.md              # Project overview & guide
├── documentation.md       # Technical architectural documentation
├── internship_report.md   # Formal Internship Project Report
├── LICENSE                # MIT Open-Source License
├── .gitignore             # Standard Python gitignore rules
├── scores.json            # Local JSON database for persistent scores
│
├── assets/
│   └── hangman_ascii.txt  # Multi-stage ASCII hangman drawings
└── screenshots/
    └── .gitkeep           # Screenshot assets directory
```

---

## 🚀 Execution Guide & Installation

### 1. Prerequisites
Ensure you have Python 3.8 or higher installed on your system.
```bash
python --version
```

### 2. Clone / Download Project
```bash
git clone https://github.com/your-username/Advanced_Hangman.git
cd Advanced_Hangman
```

### 3. Install Dependencies
Install required packages using pip:
```bash
pip install -r requirements.txt
```

### 4. Run the Game
Execute `main.py` using Python:
```bash
python main.py
```

---

## 📡 API Information

The application utilizes **Random Word API** hosted on Heroku:
- **Endpoint**: `https://random-word-api.herokuapp.com/word`
- **Response Format**: JSON Array of strings e.g. `["apple"]`
- **Fallback Trigger**: Triggers if response time > 3 seconds, HTTP error occurs, or offline status is detected.

---

## 🖼️ Screenshots

*Screenshots of the CLI application interface can be placed inside the `screenshots/` directory.*

- **Main Menu**: Options for playing, viewing leaderboard, instructions, or exit.
- **In-Game Dashboard**: Real-time timer, colored ASCII hangman, word mask, and remaining attempt counters.
- **Victory Screen**: Score breakdown, speed bonus, streak counter, and personal record update.

---

## 🛠️ Technologies Used

- **Language**: Python 3.8+
- **Styling**: Colorama (ANSI escape sequences)
- **API Communication**: `urllib.request` / `requests` / JSON
- **Data Storage**: JSON (`scores.json`)
- **Architecture**: Object-Oriented Programming (OOP) & Clean Architecture

---

## 🔮 Future Scope

1. **Multiplayer Mode**: Pass-and-play or network socket-based 2-player match.
2. **Category Selection**: Choose word categories (e.g. Science, Animals, Movies, Tech).
3. **GUI Upgrade**: Build a PyQt / Tkinter graphical interface wrapper.
4. **Sound Effects**: Add optional sound effects for correct/wrong guesses.

---

## 👨‍💻 Author

**Kartik Shukla**  
Intern Grow Python Programming Track – Task 1  
GitHub:([Kartikshukla](https://github.com/kartikshukla2301-eng))
