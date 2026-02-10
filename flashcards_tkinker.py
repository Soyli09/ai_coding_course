# flashcards_app.py
import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import threading

# ================= FLASHCARDS DATA =================
FLASHCARDS = []

# ================= COMMON FUNCTIONS =================
def add_flashcard(front, back):
    FLASHCARDS.append({"front": front, "back": back})

def edit_flashcard(index, front, back):
    if 0 <= index < len(FLASHCARDS):
        FLASHCARDS[index] = {"front": front, "back": back}

def delete_flashcard(index):
    if 0 <= index < len(FLASHCARDS):
        FLASHCARDS.pop(index)

# ================= CLI =================
def cli_menu():
    while True:
        print("\n=== Flashcards CLI ===")
        print("1. Add Flashcard")
        print("2. Edit Flashcard")
        print("3. Delete Flashcard")
        print("4. Study Flashcards")
        print("5. Quiz Mode")
        print("6. List Flashcards")
        print("7. Exit")
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            front = input("Front: ").strip()
            back = input("Back: ").strip()
            add_flashcard(front, back)
            print("Flashcard added!")
        elif choice == "2":
            for idx, card in enumerate(FLASHCARDS):
                print(f"{idx+1}. {card['front']} -> {card['back']}")
            try:
                i = int(input("Enter flashcard number to edit: ")) - 1
                front = input("New front: ").strip()
                back = input("New back: ").strip()
                edit_flashcard(i, front, back)
                print("Flashcard updated!")
            except:
                print("Invalid input.")
        elif choice == "3":
            for idx, card in enumerate(FLASHCARDS):
                print(f"{idx+1}. {card['front']} -> {card['back']}")
            try:
                i = int(input("Enter flashcard number to delete: ")) - 1
                delete_flashcard(i)
                print("Flashcard deleted!")
            except:
                print("Invalid input.")
        elif choice == "4":
            for card in FLASHCARDS:
                input(f"Front: {card['front']} (press Enter to see back)")
                print(f"Back: {card['back']}\n")
        elif choice == "5":
            cards = FLASHCARDS[:]
            random.shuffle(cards)
            score = 0
            for card in cards:
                answer = input(f"Front: {card['front']}\nYour answer: ").strip()
                if answer.lower() == card['back'].lower():
                    print("Correct!")
                    score += 1
                else:
                    print(f"Wrong! Back: {card['back']}")
            print(f"Quiz finished! Score: {score}/{len(cards)}")
        elif choice == "6":
            for idx, card in enumerate(FLASHCARDS):
                print(f"{idx+1}. {card['front']} -> {card['back']}")
        elif choice == "7":
            break
        else:
            print("Invalid choice!")

# ================= GUI =================
def gui_app():
    root = tk.Tk()
    root.title("Flashcards GUI")

    current_index = [0]

    front_label = tk.Label(root, text="", font=("Arial", 16), wraplength=400)
    front_label.pack(pady=20)

    back_label = tk.Label(root, text="", font=("Arial", 14), wraplength=400)
    back_label.pack(pady=10)

    def show_flashcard(idx):
        if FLASHCARDS:
            card = FLASHCARDS[idx]
            front_label.config(text=card['front'])
            back_label.config(text="")
        else:
            front_label.config(text="No flashcards!")
            back_label.config(text="")

    def flip_flashcard():
        idx = current_index[0]
        if FLASHCARDS:
            back_label.config(text=FLASHCARDS[idx]['back'])

    def next_flashcard():
        if FLASHCARDS:
            current_index[0] = (current_index[0] + 1) % len(FLASHCARDS)
            show_flashcard(current_index[0])

    def add_card():
        front = simpledialog.askstring("Front", "Enter front text:")
        back = simpledialog.askstring("Back", "Enter back text:")
        if front and back:
            add_flashcard(front, back)
            messagebox.showinfo("Success", "Flashcard added!")
            show_flashcard(current_index[0])

    tk.Button(root, text="Flip", command=flip_flashcard).pack(side="left", padx=5)
    tk.Button(root, text="Next", command=next_flashcard).pack(side="left", padx=5)
    tk.Button(root, text="Add Flashcard", command=add_card).pack(side="left", padx=5)

    show_flashcard(current_index[0])
    root.mainloop()

# ================= START BOTH =================
if __name__ == "__main__":
    # Run GUI in separate thread so CLI can run too
    threading.Thread(target=gui_app, daemon=True).start()
    cli_menu()
