import random
import json
import os
from datetime import datetime

# Constants
SAVE_FILE = "guessing_game_stats.json"
DIFFICULTY_LEVELS = {
    "1": {"name": "Easy", "range": 10, "attempts": 5},
    "2": {"name": "Medium", "range": 50, "attempts": 7},
    "3": {"name": "Hard", "range": 100, "attempts": 10}
}

def load_stats():
    """Load game statistics from file"""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"games": [], "total_wins": 0, "total_games": 0}

def save_stats(stats):
    """Save statistics to file"""
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=4)

def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("       GUESS THE NUMBER GAME")
    print("=" * 50)
    print("1. New Game")
    print("2. Statistics")
    print("3. Game Rules")
    print("4. Exit")
    print("-" * 50)

def show_rules():
    """Show game rules"""
    print("\nGAME RULES:")
    print("- The computer picks a secret number within a range.")
    print("- You have a limited number of attempts to guess it.")
    print("- After each guess, you get a hint: 'higher' or 'lower'.")
    print("- Higher difficulty means wider range and fewer attempts.")
    print("- Your stats are saved between sessions.")
    input("\nPress Enter to continue...")

def select_difficulty():
    """Let user select difficulty level"""
    print("\nSelect difficulty level:")
    for key, value in DIFFICULTY_LEVELS.items():
        print(f"{key}. {value['name']} (1–{value['range']}, attempts: {value['attempts']})")
    while True:
        choice = input("Your choice (1–3): ").strip()
        if choice in DIFFICULTY_LEVELS:
            return DIFFICULTY_LEVELS[choice]
        print("Invalid choice. Please enter 1, 2, or 3.")

def play_game(difficulty):
    """Main game logic"""
    secret_number = random.randint(1, difficulty["range"])
    max_attempts = difficulty["attempts"]
    attempts = 0
    guessed = False

    print(f"\nI’ve picked a number between 1 and {difficulty['range']}.")
    print(f"You have {max_attempts} attempts.")

    while attempts < max_attempts and not guessed:
        try:
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts}. Your guess: "))
            attempts += 1

            if guess == secret_number:
                print(f"🎉 Congratulations! You guessed {secret_number} in {attempts} attempts!")
                guessed = True
            elif guess < secret_number:
                print("The secret number is higher.")
            else:
                print("The secret number is lower.")
        except ValueError:
            print("Please enter a valid integer.")
            attempts -= 1  # Don’t count invalid input as an attempt

    if not guessed:
        print(f"❌ Out of attempts! The secret number was: {secret_number}")

    return guessed, attempts

def update_stats(stats, won, attempts, difficulty):
    """Update and save game statistics"""
    game_record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "difficulty": difficulty["name"],
        "won": won,
        "attempts_used": attempts,
        "max_attempts": difficulty["attempts"],
        "range": difficulty["range"]
    }
    stats["games"].append(game_record)
    stats["total_games"] += 1
    if won:
        stats["total_wins"] += 1
    save_stats(stats)

def show_stats(stats):
    """Display game statistics"""
    if not stats["games"]:
        print("\nNo games played yet. Play a few rounds first!")
        return

    print("\n" + "-" * 50)
    print("GAME STATISTICS")
    print("-" * 50)
    print(f"Total games: {stats['total_games']}")
    print(f"Wins: {stats['total_wins']}")
    win_rate = (stats['total_wins'] / stats['total_games']) * 100 if stats['total_games'] > 0 else 0
    print(f"Win rate: {win_rate:.1f}%")
    print("\nRecent 5 games:")
    recent_games = stats["games"][-5:]
    for i, game in enumerate(recent_games, 1):
        result = "Win" if game["won"] else "Loss"
        print(f"{i}. {game['date']} | {game['difficulty']} | {result} ({game['attempts_used']}/{game['max_attempts']})")

def main():
    """Main program loop"""
    stats = load_stats()
    print("Welcome to Guess the Number!")

    while True:
        displaymenu()
        choice = input("Choose an option (1–4): ").strip()

        if choice == "1":
            difficulty = select_difficulty()
            won, attempts = play_game(difficulty)
            update_stats(stats, won, attempts, difficulty)
        elif choice == "2":
            show_stats(stats)
            input("\nPress Enter to return to menu...")
        elif choice == "3":
            show_rules()
        elif choice == "4":
            print("Thanks for playing! See you next time!")
            break
        else:
            print("Invalid input. Please choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
