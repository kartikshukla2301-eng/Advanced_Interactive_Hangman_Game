# Technical Documentation - Advanced Interactive Hangman Game

**Project Name**: Advanced Interactive Hangman Game  
**Track**: InternGrow Python Programming Track – Task 1  
**Author**: Kartik Shukla  

---

## 1. Introduction

The **Advanced Interactive Hangman Game** is a modern terminal-based software application written in Python. It reimagines the traditional word-guessing game by integrating cloud-based REST APIs, robust offline failovers, custom difficulty levels, player performance analytics, and dynamic ANSI terminal graphics.

---

## 2. Objective

The primary objective of this project is to develop a complete, production-ready, object-oriented Python application that demonstrates clean software architecture, exception handling, data persistence, and professional documentation practices required in modern software development.

---

## 3. Problem Statement

Classic terminal-based Hangman games often suffer from several limitations:
1. Static and repetitive hardcoded word lists.
2. Fragile user input handling leading to unexpected crashes on invalid entries.
3. Lack of progress persistence across game sessions.
4. Monolithic single-file implementations that violate basic Clean Code principles.

This project addresses these challenges by delivering a modular, fault-tolerant system with dynamic word fetching, input sanitization, and structured JSON database storage.

---

## 4. Functional Requirements

- **FR-1 Player Profile Management**: Prompt player for display name and track personal stats across games.
- **FR-2 Dynamic Word Fetching**: Retrieve random words from an external REST API with fallback to internal dictionary.
- **FR-3 Difficulty Selection**: Offer Easy (8 attempts), Medium (6 attempts), and Hard (5 attempts) game modes.
- **FR-4 Real-Time Word Progress**: Display current guessed letters and masked un-guessed letters (`_`).
- **FR-5 Input Sanitization**: Validate single alphabetic characters and reject duplicate inputs gracefully.
- **FR-6 Hint Mechanism**: Provide optional letter hints bounded by difficulty rules.
- **FR-7 Real-Time Timer**: Record round completion time to calculate performance bonuses.
- **FR-8 Score & Leaderboard System**: Calculate scores, record streaks, and persist high scores in `scores.json`.
- **FR-9 Colored Terminal Graphics**: Render ASCII art and color-coded status messages using `colorama`.

---

## 5. Non-Functional Requirements

- **NFR-1 Reliability**: 100% uptime through automatic fallback if API endpoints fail or time out.
- **NFR-2 Code Quality**: Strict adherence to Python PEP8 styling, type hint annotations, and docstrings.
- **NFR-3 Modularity**: Decoupled OOP components (`HangmanGame`, `WordAPI`, `WordBank`, `ScoreManager`).
- **NFR-4 Performance**: Zero input latency with optimized JSON reading/writing operations.

---

## 6. Modules Explanation

### 6.1 `main.py`
Serves as the main CLI entry point. Orchestrates user menu navigation, difficulty selection, game execution loop, and leaderboard displays.

### 6.2 `game.py`
Defines the `HangmanGame` class. Holds transient round state including secret word, guessed set, wrong list, remaining attempts, hints remaining, and timer metrics.

### 6.3 `api.py`
Defines `WordAPI`. Manages HTTP GET requests to `https://random-word-api.herokuapp.com/word` with a 3-second timeout and exception catching.

### 6.4 `words.py`
Defines `WordBank`. Stores categorized static fallback word arrays (`EASY_WORDS`, `MEDIUM_WORDS`, `HARD_WORDS`).

### 6.5 `score.py`
Defines `ScoreManager`. Manages reads/writes to `scores.json`, calculates scores based on time/difficulty/attempts, and ranks players on a global leaderboard.

### 6.6 `utils.py`
Provides utility routines: screen clearing (`clear_screen`), terminal color wrappers (`Fore`, `Style`), time formatters, and ASCII stage loader (`load_ascii_stages`).

---

## 7. Key Algorithms

### 7.1 Dynamic Score Calculation Formula
$$\text{Score} = \Big( (\text{Word Length} \times 20) + (\text{Attempts Left} \times 30) + \max(0, 150 - 2 \times \text{Time Seconds}) \Big) \times \text{Difficulty Multiplier}$$

*Multipliers*: Easy = 1.0, Medium = 1.5, Hard = 2.2.

### 7.2 API Fallback Decision Tree Algorithm
1. Send HTTP request to Heroku API with timeout = 3.0s.
2. If HTTP status == 200 and payload is valid non-empty string list:
   - Check if word length matches requested difficulty bounds.
   - If matched, return word and API source flag.
3. If timeout, connection error, or mismatch occurs:
   - Query `WordBank.get_word_by_difficulty(difficulty)`.
   - Return local word and Fallback source flag.

---

## 8. Flow of Execution

```
[Start App main.py]
        │
        ▼
[Prompt Player Name]
        │
        ▼
┌─► [Main Menu Loop]
│       │
│       ├──► Option 1: Play Game
│       │       │
│       │       ▼
│       │   [Select Difficulty] ──► [Fetch Word (API/Local)]
│       │                                │
│       │                                ▼
│       │                        [Interactive Round Loop]
│       │                                │
│       │                                ▼
│       │                        [Calculate Score & Update JSON]
│       │                                │
│       │                                ▼
│       │                        [Replay Prompt? (Y/N)]
│       │
│       ├──► Option 2: View Leaderboard & Player Stats
│       ├──► Option 3: View Instructions
│       └──► Option 4: Exit Application
```

---

## 9. API Information

- **Endpoint**: `https://random-word-api.herokuapp.com/word`
- **Method**: `GET`
- **Response**: `["example"]`
- **Timeout Handling**: Built-in 3.0s threshold prevents terminal freeze on slow networks.

---

## 10. Folder Structure

```
Advanced_Hangman/
├── main.py
├── game.py
├── api.py
├── words.py
├── score.py
├── utils.py
├── requirements.txt
├── README.md
├── documentation.md
├── internship_report.md
├── LICENSE
├── .gitignore
├── scores.json
├── assets/
│   └── hangman_ascii.txt
└── screenshots/
    └── .gitkeep
```

---

## 11. Challenges & Solutions

| Challenge | Solution Implemented |
| :--- | :--- |
| Terminal layout flickering on refresh | Standardized `clear_screen()` calls with formatted ANSI banners |
| Network latency hanging CLI | Set 3-second `urllib` timeout with silent exception handling |
| Data corruption in JSON storage | Safe `try-except` JSON parsing with automatic recovery structure |
| Cross-platform clear screen | Checked `os.name` to execute `cls` (Windows) or `clear` (Linux/macOS) |

---

## 12. Future Improvements

1. Add multiplayer web-socket networking.
2. Incorporate custom word category packs (Geographic, Technical, Pop Culture).
3. Build a graphical user interface (GUI) using PySide6/PyQt6.

---

## 13. Conclusion

The Advanced Interactive Hangman Game successfully demonstrates modern Python practices, clean OOP architecture, resilience, and user-centric design suitable for production open-source software.
