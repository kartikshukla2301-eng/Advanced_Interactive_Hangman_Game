"""
Utilities module for Advanced Interactive Hangman Game.

Provides Colorama terminal styling, screen clearing, ASCII art loading,
and text formatting helper functions.
"""

import os
import sys
from typing import List
try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback dummy class if colorama is not installed
    class DummyColor:
        def __getattr__(self, name):
            return ""
    Fore = Style = Back = DummyColor()


def clear_screen() -> None:
    """Clears the terminal screen across Windows, Linux, and macOS."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner() -> None:
    """Prints styled header banner for the Hangman CLI application."""
    banner_text = f"""
{Fore.CYAN}{Style.BRIGHT}====================================================================
{Fore.YELLOW}{Style.BRIGHT}                ADVANCED INTERACTIVE HANGMAN GAME
{Fore.CYAN}{Style.BRIGHT}               InternGrow Python Track — Task 1
===================================================================={Style.RESET_ALL}
"""
    print(banner_text)


def print_success(message: str) -> None:
    """Prints a green success message."""
    print(f"{Fore.GREEN}{Style.BRIGHT}✔ {message}{Style.RESET_ALL}")


def print_error(message: str) -> None:
    """Prints a red error message."""
    print(f"{Fore.RED}{Style.BRIGHT}✖ {message}{Style.RESET_ALL}")


def print_warning(message: str) -> None:
    """Prints a yellow warning message."""
    print(f"{Fore.YELLOW}{Style.BRIGHT}⚠ {message}{Style.RESET_ALL}")


def print_info(message: str) -> None:
    """Prints a cyan info message."""
    print(f"{Fore.CYAN}ℹ {message}{Style.RESET_ALL}")


def print_accent(message: str) -> None:
    """Prints a magenta styled accent message."""
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{message}{Style.RESET_ALL}")


def load_ascii_stages(filepath: str = "assets/hangman_ascii.txt") -> List[str]:
    """
    Parses and loads ASCII hangman stages from a text file.

    Args:
        filepath: Path to the hangman_ascii.txt asset file.

    Returns:
        List of ASCII stage strings indexable by stage index.
    """
    default_stages: List[str] = [
        r"  +---+" + "\n" + r"  |   |" + "\n" + r"      |" + "\n" + r"      |" + "\n" + r"      |" + "\n" + r"      |" + "\n" + r"=========",
        r"  +---+" + "\n" + r"  |   |" + "\n" + r"  O   |" + "\n" + r"      |" + "\n" + r"      |" + "\n" + r"      |" + "\n" + r"=========",
        r"  +---+" + "\n" + r"  |   |" + "\n" + r"  O   |" + "\n" + r"  |   |" + "\n" + r"      |" + "\n" + r"      |" + "\n" + r"=========",
        r"  +---+" + "\n" + r"  |   |" + "\n" + r"  O   |" + "\n" + r" /|   |" + "\n" + r"      |" + "\n" + r"      |" + "\n" + r"=========",
        r"  +---+" + "\n" + r"  |   |" + "\n" + r"  O   |" + "\n" + r" /|\  |" + "\n" + r"      |" + "\n" + r"      |" + "\n" + r"=========",
        r"  +---+" + "\n" + r"  |   |" + "\n" + r"  O   |" + "\n" + r" /|\  |" + "\n" + r" /    |" + "\n" + r"      |" + "\n" + r"=========",
        r"  +---+" + "\n" + r"  |   |" + "\n" + r"  O   |" + "\n" + r" /|\  |" + "\n" + r" / \  |" + "\n" + r"      |" + "\n" + r"=========",
        r"  +---+" + "\n" + r"  |   |" + "\n" + r"  X   |" + "\n" + r" /|\  |" + "\n" + r" / \  |" + "\n" + r"      |" + "\n" + r"========="
    ]

    if not os.path.exists(filepath):
        return default_stages

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        raw_stages = content.split("===STAGE")
        stages = []
        for section in raw_stages:
            if not section.strip():
                continue
            # Remove stage header line e.g., ' 0==='
            lines = section.strip().split("\n")
            if lines and ("===" in lines[0] or lines[0].strip().isdigit()):
                stage_body = "\n".join(lines[1:])
            else:
                stage_body = "\n".join(lines)
            stages.append(stage_body)

        return stages if len(stages) >= 7 else default_stages
    except Exception:
        return default_stages


def format_time(seconds: float) -> str:
    """
    Formats seconds into a human readable minute:second string.

    Args:
        seconds: Elapsed time in seconds.

    Returns:
        Formatted string (e.g. '01m 24s').
    """
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{mins:02d}m {secs:02d}s"
