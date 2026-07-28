"""
API Service module for Advanced Interactive Hangman Game.

Handles fetching random words from remote HTTP APIs with automatic fallback
to local WordBank on failure, network timeouts, or invalid payloads.
"""

import json
import urllib.request
import urllib.error
from typing import Tuple, Optional
from words import WordBank


class WordAPI:
    """Manages external API requests for random word generation with fallback logic."""

    PRIMARY_API_URL: str = "https://random-word-api.herokuapp.com/word"

    def __init__(self, timeout: float = 3.0) -> None:
        """
        Initialize the WordAPI client.

        Args:
            timeout: Network request timeout in seconds.
        """
        self.timeout: float = timeout
        self.word_bank: WordBank = WordBank()

    def fetch_word(self, difficulty: str = "medium") -> Tuple[str, str]:
        """
        Attempts to fetch a random word from the external API.
        If the API call fails or yields invalid data, automatically falls back to local WordBank.

        Args:
            difficulty: Desired difficulty level ('easy', 'medium', 'hard').

        Returns:
            Tuple of (word: str, source_description: str).
        """
        api_word = self._fetch_from_remote_api()

        if api_word and self.word_bank.is_valid_word(api_word):
            # Check length matches approximate difficulty
            clean_word = api_word.strip().upper()
            length = len(clean_word)

            if difficulty.lower() == "easy" and length > 6:
                # Filter remote word to match easy length if needed, else fallback
                return self.word_bank.get_word_by_difficulty("easy"), "Local WordBank (Difficulty Match)"
            elif difficulty.lower() == "hard" and length < 7:
                return self.word_bank.get_word_by_difficulty("hard"), "Local WordBank (Difficulty Match)"

            return clean_word, "Random Word API (herokuapp.com)"

        # Fallback to local WordBank
        fallback_word = self.word_bank.get_word_by_difficulty(difficulty)
        return fallback_word, "Local WordBank (Offline Fallback)"

    def _fetch_from_remote_api(self) -> Optional[str]:
        """
        Internal helper to execute HTTP GET request to external API.

        Returns:
            Extracted word string if successful, None otherwise.
        """
        try:
            req = urllib.request.Request(
                self.PRIMARY_API_URL,
                headers={"User-Agent": "HangmanGamePython/1.0"}
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                if response.status == 200:
                    data = response.read().decode('utf-8')
                    parsed_json = json.loads(data)
                    if isinstance(parsed_json, list) and len(parsed_json) > 0:
                        return str(parsed_json[0])
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, Exception):
            # Graceful silent catch to trigger fallback
            return None

        return None
