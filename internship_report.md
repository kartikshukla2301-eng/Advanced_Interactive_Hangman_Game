# INTERNSHIP PROJECT REPORT

**Task Title**: Advanced Interactive Hangman Game  
**Track**: InternGrow Python Programming Track – Task 1  
**Student Name**: Kartik Shukla  
**Submission Date**: July 2026  
**Status**: Completed & Production-Ready  

---

## Cover Page

**Project Title**: Advanced Interactive Hangman Game CLI  
**Submitted To**: InternGrow Evaluation Committee  
**Track**: Python Programming Track  
**Task ID**: Task 1  
**Developer**: Kartik Shukla  

---

## Abstract

This project report documents the design, architectural development, testing, and deployment of the **Advanced Interactive Hangman Game**. Built as part of Task 1 for the InternGrow Python Programming Track, the system presents an enhanced Command Line Interface application written in Python. Key highlights include dynamic external word fetching via REST API, fallback local dictionary management, player session statistics persistence in JSON format, ANSI terminal visualization with ASCII art, and comprehensive input validation.

---

## 1. Introduction

Command-line applications remain a fundamental building block for evaluating software engineering competencies. The Hangman game project evaluates core proficiency in Python syntax, Object-Oriented Design (OOD), API interaction, exception handling, and modular project structure.

---

## 2. Project Objectives

1. Design a clean, production-grade Python project following PEP8 standards.
2. Implement real-time remote word fetching with automatic offline fallback.
3. Incorporate interactive difficulty settings (Easy, Medium, Hard) impacting word choice, hints, and attempt limits.
4. Establish score calculations based on difficulty multipliers, remaining lives, and time speed bonuses.
5. Provide persistent score storage using local JSON files.

---

## 3. Technology Stack

- **Primary Language**: Python 3.8+
- **Terminal Formatting**: Colorama 0.4.6+
- **Network Requests**: Standard `urllib.request` / `requests`
- **Data Serialization**: JSON (`json` module)
- **Version Control**: Git & GitHub

---

## 4. Software & System Requirements

### Hardware Requirements
- **Processor**: Intel Core i3 / AMD Ryzen 3 or equivalent.
- **RAM**: 2 GB Minimum.
- **Disk Space**: 10 MB available space.

### Software Requirements
- **Operating System**: Windows 10/11, macOS, or Linux.
- **Interpreter**: Python 3.8 or higher.
- **Package Manager**: `pip`.

---

## 5. Methodology

The software was developed following the **Modular Object-Oriented Software Engineering Methodology**:
1. **Requirement Analysis**: Identifying core functionality, API endpoints, and fallback logic.
2. **Architectural Design**: Decoupling game engine (`game.py`), API logic (`api.py`), word data (`words.py`), scoring (`score.py`), and CLI presentation (`main.py` & `utils.py`).
3. **Implementation**: Writing clean, type-annotated code with docstrings.
4. **Verification & Testing**: Manual execution testing across network scenarios and invalid input edge cases.

---

## 6. Implementation Highlights

### 6.1 Modular Structure
The project separates concerns cleanly across dedicated Python files:
- `api.py`: Connects to `https://random-word-api.herokuapp.com/word`.
- `words.py`: Categorized local word dictionary by difficulty.
- `game.py`: Manages game loop, letter validation, hints, timer, and win/loss states.
- `score.py`: Handles file IO for `scores.json` and updates player statistics.
- `utils.py`: Contains terminal visualizers and Colorama styling.

### 6.2 Resilient API Fallback Mechanism
```python
try:
    with urllib.request.urlopen(req, timeout=3.0) as response:
        # Process API response
except Exception:
    # Graceful fallback to local WordBank
    return self.word_bank.get_word_by_difficulty(difficulty)
```

---

## 7. Testing & Verification

| Test Case ID | Test Scenario | Expected Outcome | Pass / Fail |
| :--- | :--- | :--- | :--- |
| **TC-01** | Valid letter guess | Letter revealed in word mask, no attempt lost | **PASS** |
| **TC-02** | Incorrect letter guess | Attempt decremented, letter added to wrong list, ASCII stage updated | **PASS** |
| **TC-03** | Repeated letter guess | Warning displayed, no penalty applied | **PASS** |
| **TC-04** | Invalid input (numbers/symbols) | Error message shown, no attempt deducted | **PASS** |
| **TC-05** | API Offline Simulation | System automatically loads word from `WordBank` | **PASS** |
| **TC-06** | Score persistence | Player high score and game stats updated in `scores.json` | **PASS** |

---

## 8. Results & Output

The application successfully met all technical requirements:
- Delivered vibrant, color-coded CLI gameplay.
- Demonstrated zero crashes across edge-case input testing.
- Maintained responsive performance with automatic fallback during simulated API dropouts.

---

## 9. Conclusion

The Advanced Interactive Hangman Game project fulfills all requirements of InternGrow Python Programming Track – Task 1. It showcases mastery of clean Python software engineering, API resilience, data persistence, and interactive user interface design.

---

## 10. References

1. Python Software Foundation. *Python 3 Documentation*. https://docs.python.org/3/
2. Colorama PyPI Package. https://pypi.org/project/colorama/
3. Random Word API. https://random-word-api.herokuapp.com/
4. PEP 8 -- Style Guide for Python Code. https://peps.python.org/pep-0008/
