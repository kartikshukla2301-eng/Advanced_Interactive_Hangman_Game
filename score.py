"""
Score Management module for Advanced Interactive Hangman Game.

Handles persistent storage of high scores, player statistics, leaderboard,
and points calculation algorithms using a local JSON database.
"""

import json
import os
from typing import Dict, List, Any, Optional


class ScoreManager:
    """Manages player scores, game statistics, and persistent JSON storage."""

    DEFAULT_FILE_PATH: str = "scores.json"

    def __init__(self, file_path: str = DEFAULT_FILE_PATH) -> None:
        """
        Initialize ScoreManager with the specified JSON file path.

        Args:
            file_path: Path to the JSON scores file.
        """
        self.file_path: str = file_path
        self.data: Dict[str, Any] = self.load_scores()

    def load_scores(self) -> Dict[str, Any]:
        """
        Loads score database from JSON file. Initializes structure if file doesn't exist.

        Returns:
            Dictionary containing players data and global leaderboard metadata.
        """
        if not os.path.exists(self.file_path):
            initial_structure: Dict[str, Any] = {"players": {}, "leaderboard": []}
            self._save_to_disk(initial_structure)
            return initial_structure

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = json.load(f)
                if isinstance(content, dict) and "players" in content:
                    return content
        except (json.JSONDecodeError, IOError):
            pass

        # Fallback if corrupted file
        fallback_data = {"players": {}, "leaderboard": []}
        self._save_to_disk(fallback_data)
        return fallback_data

    def _save_to_disk(self, data: Optional[Dict[str, Any]] = None) -> None:
        """Helper to save current data to disk."""
        data_to_save = data if data is not None else self.data
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, indent=4)
        except IOError as e:
            print(f"[Warning] Failed to save scores to disk: {e}")

    def save_scores(self) -> None:
        """Public method to flush scores to JSON file."""
        self._save_to_disk()

    @staticmethod
    def calculate_score(
        difficulty: str,
        attempts_left: int,
        max_attempts: int,
        time_taken_seconds: float,
        word_length: int
    ) -> int:
        """
        Calculates points earned for a winning game based on game parameters.

        Args:
            difficulty: 'easy', 'medium', or 'hard'.
            attempts_left: Remaining attempts at game end.
            max_attempts: Total allowed attempts.
            time_taken_seconds: Time taken to solve the word.
            word_length: Number of letters in secret word.

        Returns:
            Calculated score integer.
        """
        difficulty_multipliers = {
            "easy": 1.0,
            "medium": 1.5,
            "hard": 2.2
        }
        multiplier = difficulty_multipliers.get(difficulty.lower(), 1.0)

        base_points = word_length * 20
        attempts_bonus = attempts_left * 30

        # Time bonus: faster completion gives extra points (capped max 150 points bonus)
        time_bonus = max(0, int(150 - (time_taken_seconds * 2)))

        total = int((base_points + attempts_bonus + time_bonus) * multiplier)
        return max(total, 10)

    def record_game(
        self,
        player_name: str,
        won: bool,
        score: int,
        difficulty: str,
        time_taken: float
    ) -> Dict[str, Any]:
        """
        Updates statistics and score profile for a given player.

        Args:
            player_name: Name of the player.
            won: True if player won, False if lost.
            score: Points earned in this game.
            difficulty: Game difficulty played.
            time_taken: Seconds taken during game.

        Returns:
            Updated player stats dictionary.
        """
        clean_name = player_name.strip() or "Guest"
        players = self.data["players"]

        if clean_name not in players:
            players[clean_name] = {
                "name": clean_name,
                "high_score": 0,
                "total_games": 0,
                "wins": 0,
                "losses": 0,
                "current_streak": 0,
                "best_streak": 0,
                "total_points": 0,
                "fastest_win_seconds": None
            }

        stats = players[clean_name]
        stats["total_games"] += 1

        if won:
            stats["wins"] += 1
            stats["current_streak"] += 1
            stats["total_points"] += score
            if stats["current_streak"] > stats["best_streak"]:
                stats["best_streak"] = stats["current_streak"]
            if score > stats["high_score"]:
                stats["high_score"] = score

            if stats["fastest_win_seconds"] is None or time_taken < stats["fastest_win_seconds"]:
                stats["fastest_win_seconds"] = round(time_taken, 1)
        else:
            stats["losses"] += 1
            stats["current_streak"] = 0

        # Update leaderboard cache
        self._update_leaderboard()
        self.save_scores()
        return stats

    def _update_leaderboard(self) -> None:
        """Internal helper to refresh global leaderboard ranking."""
        leaderboard_list = []
        for name, stats in self.data["players"].items():
            win_rate = round((stats["wins"] / stats["total_games"]) * 100, 1) if stats["total_games"] > 0 else 0.0
            leaderboard_list.append({
                "name": name,
                "high_score": stats["high_score"],
                "total_points": stats["total_points"],
                "wins": stats["wins"],
                "total_games": stats["total_games"],
                "win_rate": win_rate,
                "best_streak": stats["best_streak"]
            })

        # Sort leaderboard by high score descending, then total_points
        leaderboard_list.sort(key=lambda x: (x["high_score"], x["total_points"]), reverse=True)
        self.data["leaderboard"] = leaderboard_list

    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieves top ranked players from leaderboard.

        Args:
            limit: Maximum number of top players to return.

        Returns:
            List of player leaderboard dictionaries.
        """
        self._update_leaderboard()
        return self.data["leaderboard"][:limit]

    def get_player_stats(self, player_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves statistics for a specific player name.

        Args:
            player_name: Player name to look up.

        Returns:
            Stats dictionary if found, None otherwise.
        """
        clean_name = player_name.strip()
        return self.data["players"].get(clean_name, None)
