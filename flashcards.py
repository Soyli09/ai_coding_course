# flashcards_cli.py
import random

# ================= FLASHCARDS DATA =================
FLASHCARDS = []

# ================= FUNCTIONS =================
def add_flashcard():
    front = input("Enter front text: ").strip()
    back = input("Enter back text: ").strip()
    if front and back:
        FLASHCARDS.append({"front": front, "back": back})
        print("Flashcard added!")
    else:
        print("Both front and back are required.")

def edit_flashcard():
    if not FLASHCARDS:
        print("No flashcards to edit.")
        return
    list_flashcards()
    try:
        idx = int(input("Enter flashcard number to edit: ")) - 1
        if idx < 0 or idx >= len(FLASHCARDS):
            print("Invalid number.")
            return
        front = input("New front text: ").strip()
        back = input("New back text: ").strip()
        if front and back:
            FLASHCARDS[idx] = {"front": front, "back": back}
            print("Flashcard updated!")
        else:
            print("Both front and back are required.")
    except ValueError:
        print("Invalid input.")

def delete_flashcard():
    if not FLASHCARDS:
        print("No flashcards to delete.")
        return
    list_flashcards()
    try:
        idx = int(input("Enter flashcard number to delete: ")) - 1
        if idx < 0 or idx >= len(FLASHCARDS):
            print("Invalid number.")
            return
        removed = FLASHCARDS.pop(idx)
        print(f"Deleted flashcard: {removed['front']}")
    except ValueError:
        print("Invalid input.")

def list_flashcards():
    if not FLASHCARDS:
        print("No flashcards available.")
        return
    print("\nFlashcards:")
    for i, card in enumerate(FLASHCARDS, 1):
        print(f"{i}. {card['front']} -> {card['back']}")

def study_flashcards():
    if not FLASHCARDS:
        print("No flashcards to study.")
        return
    print("\nStudy Mode (press Enter to flip card, type 'q' to quit):")
    for card in FLASHCARDS:
        user = input(f"Front: {card['front']} (Enter to see back): ")
        if user.lower() == 'q':
            break
        print(f"Back: {card['back']}\n")

def quiz_flashcards():
    if not FLASHCARDS:
        print("No flashcards to quiz.")
        return
    cards = FLASHCARDS[:]
    random.shuffle(cards)
    score = 0
    print("\nQuiz Mode (type your answer, type 'q' to quit):")
    for card in cards:
        answer = input(f"Front: {card['front']}\nYour answer: ").strip()
        if answer.lower() == 'q':
            break
        if answer.lower() == card['back'].lower():
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! Back: {card['back']}\n")
    print(f"Quiz finished! Score: {score}/{len(cards)}")

# ================= MAIN MENU =================
def main_menu():
    while True:
        print("\n=== Flashcards Terminal App ===")
        print("1. Add Flashcard")
        print("2. Edit Flashcard")
        print("3. Delete Flashcard")
        print("4. List Flashcards")
        print("5. Study Flashcards")
        print("6. Quiz Mode")
        print("7. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_flashcard()
        elif choice == "2":
            edit_flashcard()
        elif choice == "3":
            delete_flashcard()
        elif choice == "4":
            list_flashcards()
        elif choice == "5":
            study_flashcards()
        elif choice == "6":
            quiz_flashcards()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

# ================= START APP =================
if __name__ == "__main__":
    main_menu()
