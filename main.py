"""
Main Application Entry Point for Advanced Interactive Hangman Game.

Provides full CLI interface, interactive menus, game loop orchestration,
statistics presentation, and player session management.
"""

import sys
import time
from game import HangmanGame
from score import ScoreManager
from utils import (
    clear_screen,
    print_banner,
    print_success,
    print_error,
    print_warning,
    print_info,
    print_accent,
    format_time,
    Fore,
    Style
)


class HangmanCLIApp:
    """Orchestrates the entire Hangman command-line interface application."""

    def __init__(self) -> None:
        """Initialize ScoreManager and session state."""
        self.score_manager: ScoreManager = ScoreManager()
        self.player_name: str = "Player 1"
        self.current_win_streak: int = 0

    def start(self) -> None:
        """Main application lifecycle controller."""
        clear_screen()
        print_banner()
        self._prompt_player_name()

        while True:
            clear_screen()
            print_banner()
            self._display_main_menu()
            choice = input(f"{Fore.YELLOW}Select an option (1-4): {Style.RESET_ALL}").strip()

            if choice == "1":
                self._play_game_session()
            elif choice == "2":
                self._show_leaderboard_and_stats()
            elif choice == "3":
                self._show_instructions()
            elif choice == "4":
                clear_screen()
                print_banner()
                print_accent("Thank you for playing Advanced Interactive Hangman Game!")
                print_info("Developed for InternGrow Python Programming Track - Task 1.")
                sys.exit(0)
            else:
                print_error("Invalid selection! Please choose 1, 2, 3, or 4.")
                time.sleep(1.2)

    def _prompt_player_name(self) -> None:
        """Prompts user to enter their player name."""
        print_accent("Welcome Player!")
        entered_name = input(f"{Fore.CYAN}Enter your player name (default 'Player 1'): {Style.RESET_ALL}").strip()
        if entered_name:
            self.player_name = entered_name
        print_success(f"Hello, {self.player_name}! Preparing your game environment...")
        time.sleep(1.2)

    def _display_main_menu(self) -> None:
        """Displays main menu options."""
        print(f"{Fore.CYAN}Active Player: {Fore.YELLOW}{Style.BRIGHT}{self.player_name}{Style.RESET_ALL} | "
              f"{Fore.CYAN}Current Session Streak: {Fore.GREEN}{Style.BRIGHT}{self.current_win_streak}{Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}{Style.BRIGHT}================ MAIN MENU ================{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[1]{Style.RESET_ALL} Play New Game")
        print(f"  {Fore.CYAN}[2]{Style.RESET_ALL} View High Scores & Player Statistics")
        print(f"  {Fore.YELLOW}[3]{Style.RESET_ALL} How to Play & Game Rules")
        print(f"  {Fore.RED}[4]{Style.RESET_ALL} Exit Application")
        print(f"{Fore.WHITE}{Style.BRIGHT}============================================{Style.RESET_ALL}\n")

    def _select_difficulty(self) -> str:
        """Prompts player to choose game difficulty level."""
        clear_screen()
        print_banner()
        print(f"{Fore.WHITE}{Style.BRIGHT}=========== SELECT DIFFICULTY ==========={Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[1] Easy{Style.RESET_ALL}   - 8 Attempts | Words 4-6 Letters | 2 Hints")
        print(f"  {Fore.YELLOW}[2] Medium{Style.RESET_ALL} - 6 Attempts | Words 6-8 Letters | 1 Hint")
        print(f"  {Fore.RED}[3] Hard{Style.RESET_ALL}   - 5 Attempts | Words 8+ Letters  | 0 Hints")
        print(f"{Fore.WHITE}{Style.BRIGHT}=========================================={Style.RESET_ALL}\n")

        while True:
            choice = input(f"{Fore.YELLOW}Choose difficulty (1-3) [Default 2]: {Style.RESET_ALL}").strip()
            if choice == "1":
                return "easy"
            elif choice in ("2", ""):
                return "medium"
            elif choice == "3":
                return "hard"
            else:
                print_error("Invalid choice. Please enter 1, 2, or 3.")

    def _play_game_session(self) -> None:
        """Runs single or continuous replay game sessions."""
        while True:
            difficulty = self._select_difficulty()
            game = HangmanGame(player_name=self.player_name, difficulty=difficulty)

            # Core game loop
            status_msg = f"Word fetched successfully via {game.word_source}!"

            while not game.is_over():
                clear_screen()
                print_banner()

                # Display Game Dashboard
                print(f"{Fore.CYAN}Player: {Fore.YELLOW}{self.player_name}{Style.RESET_ALL} | "
                      f"Difficulty: {Fore.MAGENTA}{game.difficulty.upper()}{Style.RESET_ALL} | "
                      f"Timer: {Fore.GREEN}{format_time(game.get_elapsed_time())}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Session Win Streak: {Fore.GREEN}{self.current_win_streak}{Style.RESET_ALL} | "
                      f"Hints Left: {Fore.YELLOW}{game.hints_remaining}{Style.RESET_ALL}\n")

                # ASCII Hangman Display
                print(f"{Fore.RED}{game.get_ascii_stage()}{Style.RESET_ALL}\n")

                # Current Word Display
                print(f"{Fore.WHITE}{Style.BRIGHT}Word Progress:  {Fore.YELLOW}{Style.BRIGHT}{game.get_display_word()}{Style.RESET_ALL}\n")

                # Wrong guesses list
                wrong_str = ", ".join(game.wrong_letters) if game.wrong_letters else "None"
                print(f"{Fore.CYAN}Wrong Guesses ({len(game.wrong_letters)}/{game.max_attempts}): {Fore.RED}{wrong_str}{Style.RESET_ALL}")

                if status_msg:
                    print(f"\n{Fore.LIGHTBLACK_EX}Status: {status_msg}{Style.RESET_ALL}")

                print(f"\n{Fore.WHITE}--------------------------------------------------{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Options: Enter a letter (A-Z) | Type '?' for hint | Type 'quit' to abandon{Style.RESET_ALL}")

                user_input = input(f"\n{Fore.GREEN}Your Guess: {Style.RESET_ALL}").strip()

                if user_input.lower() == "quit":
                    print_warning("Game abandoned by player.")
                    time.sleep(1)
                    return

                if user_input == "?":
                    success, hint_msg = game.request_hint()
                    if success:
                        status_msg = hint_msg
                    else:
                        status_msg = f"{Fore.RED}{hint_msg}{Style.RESET_ALL}"
                    continue

                valid, msg = game.guess_letter(user_input)
                status_msg = msg

            # Game End Processing
            clear_screen()
            print_banner()

            time_taken = game.get_elapsed_time()
            if game.is_won():
                self.current_win_streak += 1
                earned_score = self.score_manager.calculate_score(
                    difficulty=game.difficulty,
                    attempts_left=game.attempts_left,
                    max_attempts=game.max_attempts,
                    time_taken_seconds=time_taken,
                    word_length=len(game.secret_word)
                )

                # Record stats
                player_stats = self.score_manager.record_game(
                    player_name=self.player_name,
                    won=True,
                    score=earned_score,
                    difficulty=game.difficulty,
                    time_taken=time_taken
                )

                print_success("CONGRATULATIONS! YOU SOLVED THE WORD!")
                print(f"{Fore.GREEN}{Style.BRIGHT}The word was: {game.secret_word}{Style.RESET_ALL}\n")
                print(f"{Fore.CYAN}Points Earned: {Fore.YELLOW}+{earned_score} PTS{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Time Taken: {Fore.YELLOW}{format_time(time_taken)}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Attempts Remaining: {Fore.YELLOW}{game.attempts_left}/{game.max_attempts}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Current Streak: {Fore.GREEN}{self.current_win_streak} Wins in a Row!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Personal High Score: {Fore.MAGENTA}{player_stats['high_score']} PTS{Style.RESET_ALL}\n")

            else:
                self.current_win_streak = 0
                self.score_manager.record_game(
                    player_name=self.player_name,
                    won=False,
                    score=0,
                    difficulty=game.difficulty,
                    time_taken=time_taken
                )

                print(f"{Fore.RED}{game.get_ascii_stage()}{Style.RESET_ALL}\n")
                print_error("GAME OVER! YOU RAN OUT OF ATTEMPTS!")
                print(f"{Fore.RED}{Style.BRIGHT}The correct word was: {game.secret_word}{Style.RESET_ALL}\n")
                print(f"{Fore.CYAN}Time Spent: {format_time(time_taken)}{Style.RESET_ALL}")
                print_info("Don't give up! Practice makes perfect.\n")

            # Replay options
            print(f"{Fore.WHITE}--------------------------------------------------{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Would you like to play another round? (Y/N): {Style.RESET_ALL}", end="")
            ans = input().strip().lower()
            if ans not in ("y", "yes"):
                break

    def _show_leaderboard_and_stats(self) -> None:
        """Displays high scores leaderboard and player stats."""
        clear_screen()
        print_banner()
        print(f"{Fore.WHITE}{Style.BRIGHT}================ HALL OF FAME & LEADERBOARD ================{Style.RESET_ALL}\n")

        leaderboard = self.score_manager.get_leaderboard(limit=10)

        if not leaderboard:
            print_info("No score records found yet. Play a game to create history!")
        else:
            print(f"{'Rank':<6}{'Player Name':<18}{'High Score':<12}{'Total Pts':<12}{'Wins/Games':<14}{'Win Rate':<10}")
            print("-" * 72)
            for idx, entry in enumerate(leaderboard, start=1):
                rank_str = f"#{idx}"
                name = entry["name"][:16]
                h_score = entry["high_score"]
                tot_pts = entry["total_points"]
                record = f"{entry['wins']}/{entry['total_games']}"
                wr = f"{entry['win_rate']}%"
                print(f"{rank_str:<6}{name:<18}{h_score:<12}{tot_pts:<12}{record:<14}{wr:<10}")

        # Player specific stats
        current_stats = self.score_manager.get_player_stats(self.player_name)
        if current_stats:
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}--- Statistics for '{self.player_name}' ---{Style.RESET_ALL}")
            print(f"Total Games Played: {current_stats['total_games']} | Wins: {current_stats['wins']} | Losses: {current_stats['losses']}")
            print(f"Best Win Streak: {current_stats['best_streak']} | High Score: {current_stats['high_score']} PTS")
            if current_stats['fastest_win_seconds']:
                print(f"Fastest Win Time: {format_time(current_stats['fastest_win_seconds'])}")

        print(f"\n{Fore.WHITE}------------------------------------------------------------{Style.RESET_ALL}")
        input(f"{Fore.CYAN}Press ENTER to return to Main Menu...{Style.RESET_ALL}")

    def _show_instructions(self) -> None:
        """Displays instructions and rules of the game."""
        clear_screen()
        print_banner()
        print(f"{Fore.WHITE}{Style.BRIGHT}================ HOW TO PLAY HANGMAN ================{Style.RESET_ALL}\n")
        print("1. Objective: Guess the secret word one letter at a time before running out of attempts.")
        print("2. Word Sources: Words are fetched live from random-word-api.herokuapp.com.")
        print("   If network is unavailable, system seamlessly falls back to offline WordBank.")
        print("3. Difficulties:")
        print("   - Easy: 8 attempts, 4-6 letter words, 2 hints available.")
        print("   - Medium: 6 attempts, 6-8 letter words, 1 hint available.")
        print("   - Hard: 5 attempts, 8+ letter words, 0 hints available.")
        print("4. Scoring Formula:")
        print("   Score = (Word Length * 20 + Attempts Left * 30 + Speed Bonus) * Difficulty Multiplier")
        print("5. Controls:")
        print("   - Type any single letter (A-Z) and press Enter.")
        print("   - Type '?' during game to request an automatic letter hint (if allowed).")
        print("   - Type 'quit' to return to menu at any time.")
        print(f"\n{Fore.WHITE}------------------------------------------------------{Style.RESET_ALL}")
        input(f"{Fore.CYAN}Press ENTER to return to Main Menu...{Style.RESET_ALL}")


if __name__ == "__main__":
    app = HangmanCLIApp()
    app.start()
