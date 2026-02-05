import random

# This function gets the computer's choice
def get_computer_choice():
    return random.choice(["rock", "paper", "scissors"])


# This function gets and validates player input
def get_player_choice():
    choice = input("Choose rock, paper, or scissors: ").lower()
    while choice not in ["rock", "paper", "scissors"]:
        choice = input("Invalid choice. Try again: ").lower()
    return choice


# This function determines the winner
def determine_winner(player, computer):
    if player == computer:
        return "tie"
    elif (
        (player == "rock" and computer == "scissors") or
        (player == "paper" and computer == "rock") or
        (player == "scissors" and computer == "paper")
    ):
        return "player"
    else:
        return "computer"


# This function plays one round
def play_round():
    player = get_player_choice()
    computer = get_computer_choice()

    print(f"Computer chose: {computer}")

    result = determine_winner(player, computer)
    return result


# This function controls the whole game
def play_game():
    player_score = 0
    computer_score = 0

    for _ in range(3):  # play 3 rounds
        result = play_round()
        if result == "player":
            player_score += 1
            print("You win this round!")
        elif result == "computer":
            computer_score += 1
            print("Computer wins this round!")
        else:
            print("It's a tie!")

    print("\nFinal Score:")
    print("Player:", player_score)
    print("Computer:", computer_score)


# Main program
if __name__ == "__main__":
    play_game()
