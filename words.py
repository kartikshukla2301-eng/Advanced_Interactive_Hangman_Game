"""
Word Bank module for Advanced Interactive Hangman Game.

Provides offline local word dictionary categorized by difficulty levels
(Easy, Medium, Hard) as a reliable fallback when API requests are unavailable.
"""

import random
from typing import Dict, List


class WordBank:
    """Manages categorized local word lists for offline hangman gameplay."""

    EASY_WORDS: List[str] = [
        "APPLE", "BIRD", "CAT", "DOG", "FISH", "FROG", "LION", "MOON", "PARK",
        "STAR", "TREE", "DUCK", "BOAT", "BEAR", "CAKE", "DOOR", "FIRE", "GOLD",
        "HAND", "KING", "MILK", "NEST", "RAIN", "SHIP", "SNOW", "WIND", "BOOK",
        "GAME", "DESK", "BALL", "LAMP", "RING", "ROSE", "SONG", "TIME", "WAVE"
    ]

    MEDIUM_WORDS: List[str] = [
        "PLANET", "SILVER", "CASTLE", "GUITAR", "DRAGON", "BRIDGE", "ROCKET",
        "PENGUIN", "ORANGE", "MONKEY", "FOREST", "FLOWER", "SUMMER", "WINTER",
        "SPRING", "YELLOW", "PURPLE", "WINDOW", "SHADOW", "MIRROR", "CANDLE",
        "BOTTLE", "CAMERA", "PLANET", "SECRET", "TIGER", "PENCIL", "DOCTOR",
        "FLIGHT", "CIRCUS", "MARKET", "HAMMER", "DESERT", "ISLAND", "CANYON"
    ]

    HARD_WORDS: List[str] = [
        "ASTRONAUT", "BUTTERFLY", "CHOCOLATE", "DIAMOND", "ELEPHANT",
        "FIREWORKS", "KANGAROO", "LIGHTNING", "MOUNTAIN", "ORCHESTRA",
        "PYRAMID", "QUESTION", "RESTAURANT", "TELESCOPE", "UNIVERSE",
        "VOLCANO", "WATERFALL", "XYLOPHONE", "ALGORITHM", "ARCHITECT",
        "BICYCLE", "CHAMPION", "EXPLORER", "HERITAGE", "NAVIGATOR",
        "PARACHUTE", "REVOLUTION", "SPECTRUM", "SYMPHONY", "TRIUMPH"
    ]

    def __init__(self) -> None:
        """Initialize the WordBank with difficulty mappings."""
        self._words_by_difficulty: Dict[str, List[str]] = {
            "easy": self.EASY_WORDS,
            "medium": self.MEDIUM_WORDS,
            "hard": self.HARD_WORDS
        }

    def get_word_by_difficulty(self, difficulty: str) -> str:
        """
        Retrieves a random word matching the requested difficulty level.

        Args:
            difficulty: String specifying difficulty ('easy', 'medium', 'hard').

        Returns:
            Uppercase word string.
        """
        diff_key = difficulty.strip().lower()
        word_list = self._words_by_difficulty.get(diff_key, self.MEDIUM_WORDS)
        return random.choice(word_list).upper()

    def get_random_word(self) -> str:
        """
        Retrieves a random word across all difficulty categories.

        Returns:
            Uppercase word string.
        """
        all_words = self.EASY_WORDS + self.MEDIUM_WORDS + self.HARD_WORDS
        return random.choice(all_words).upper()

    @staticmethod
    def is_valid_word(word: str) -> bool:
        """
        Validates if a word is suitable for Hangman (letters only, min length 3).

        Args:
            word: The candidate word to validate.

        Returns:
            True if word consists only of alphabetic characters and length >= 3.
        """
        clean_word = word.strip()
        return len(clean_word) >= 3 and clean_word.isalpha()
