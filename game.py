"""
Game engine module for Advanced Interactive Hangman Game.

Encapsulates complete game state, round execution logic, letter validation,
hint processing, timer calculation, and victory/defeat evaluation.
"""

import time
import random
from typing import Set, List, Tuple, Optional
from api import WordAPI
from utils import load_ascii_stages


class HangmanGame:
    """Manages an individual game session of Hangman."""

    DIFFICULTY_SETTINGS = {
        "easy": {"max_attempts": 8, "hints": 2},
        "medium": {"max_attempts": 6, "hints": 1},
        "hard": {"max_attempts": 5, "hints": 0}
    }

    def __init__(self, player_name: str = "Player", difficulty: str = "medium") -> None:
        """
        Initialize a new Hangman game instance.

        Args:
            player_name: The playing user's display name.
            difficulty: Choice of 'easy', 'medium', or 'hard'.
        """
        self.player_name: str = player_name.strip() or "Player"
        self.difficulty: str = difficulty.lower() if difficulty.lower() in self.DIFFICULTY_SETTINGS else "medium"

        # Load difficulty parameters
        settings = self.DIFFICULTY_SETTINGS[self.difficulty]
        self.max_attempts: int = settings["max_attempts"]
        self.attempts_left: int = self.max_attempts
        self.hints_remaining: int = settings["hints"]

        # Fetch secret word from API or fallback WordBank
        self.api_service: WordAPI = WordAPI()
        self.secret_word, self.word_source = self.api_service.fetch_word(self.difficulty)

        self.guessed_letters: Set[str] = set()
        self.wrong_letters: List[str] = []
        self.ascii_stages: List[str] = load_ascii_stages()

        # Timing tracking
        self.start_time: float = time.time()
        self.end_time: Optional[float] = None

    def guess_letter(self, input_str: str) -> Tuple[bool, str]:
        """
        Processes a player's letter guess.

        Args:
            input_str: Raw input string entered by the user.

        Returns:
            Tuple of (is_valid_guess: bool, status_message: str).
        """
        clean_input = input_str.strip().upper()

        # Input validation
        if not clean_input or len(clean_input) != 1 or not clean_input.isalpha():
            return False, "Please enter a single valid alphabetic letter (A-Z)."

        if clean_input in self.guessed_letters or clean_input in self.wrong_letters:
            return False, f"You have already guessed the letter '{clean_input}'. Try another letter!"

        # Process guess
        if clean_input in self.secret_word:
            self.guessed_letters.add(clean_input)
            if self.is_won():
                self.end_time = time.time()
            return True, f"Great guess! '{clean_input}' is in the word."
        else:
            self.wrong_letters.append(clean_input)
            self.attempts_left -= 1
            if self.is_lost():
                self.end_time = time.time()
            return True, f"Sorry! '{clean_input}' is not in the word."

    def request_hint(self) -> Tuple[bool, str]:
        """
        Provides a hint by revealing one un-guessed letter if hints are available.

        Returns:
            Tuple of (success: bool, message: str).
        """
        if self.hints_remaining <= 0:
            return False, "No hints remaining for this difficulty mode!"

        unrevealed = [ch for ch in self.secret_word if ch not in self.guessed_letters]

        if not unrevealed:
            return False, "All letters are already revealed!"

        hint_letter = random.choice(unrevealed)
        self.guessed_letters.add(hint_letter)
        self.hints_remaining -= 1

        if self.is_won():
            self.end_time = time.time()

        return True, f"HINT: The letter '{hint_letter}' has been revealed for you!"

    def get_display_word(self) -> str:
        """
        Constructs masked string representation of the word (e.g. 'P Y _ H O N').

        Returns:
            Formatted masked word string.
        """
        return " ".join([ch if ch in self.guessed_letters else "_" for ch in self.secret_word])

    def get_ascii_stage(self) -> str:
        """
        Returns the ASCII hangman art corresponding to current wrong attempts.

        Returns:
            ASCII drawing string.
        """
        wrong_count = len(self.wrong_letters)
        # Map wrong count to stage index
        if not self.ascii_stages:
            return ""

        max_stage_idx = len(self.ascii_stages) - 1
        stage_idx = min(wrong_count, max_stage_idx)

        # Show final dead stage if out of attempts
        if self.attempts_left == 0 and max_stage_idx >= 7:
            stage_idx = 7

        return self.ascii_stages[stage_idx]

    def is_won(self) -> bool:
        """Checks if all letters in the secret word have been guessed."""
        return set(self.secret_word).issubset(self.guessed_letters)

    def is_lost(self) -> bool:
        """Checks if player has run out of attempts."""
        return self.attempts_left <= 0 and not self.is_won()

    def is_over(self) -> bool:
        """Checks if game has ended in win or loss."""
        return self.is_won() or self.is_lost()

    def get_elapsed_time(self) -> float:
        """
        Calculates time spent playing current game.

        Returns:
            Elapsed time in seconds.
        """
        end = self.end_time if self.end_time is not None else time.time()
        return max(0.0, end - self.start_time)
