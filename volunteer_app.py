
# volunteering_cli_api.py
import requests
import json
import random
import os

# ================= FILE STORAGE =================
EVENTS_FILE = "saved_events.txt"

# ================= DATA =================
USERS = {}
CURRENT_USER = None
EVENTS = []
APPLICATIONS = {}
SAVED = {}

# ================= API FUNCTIONS =================
API_URL = "https://randomuser.me/api/?results=10"  # simulate events with random names

def fetch_events_from_api():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        events = [f"Volunteer Event: {user['name']['first']} {user['name']['last']}" for user in data['results']]
        print("\nFetched events from API successfully!")
        save_events_to_file(events)
        return events
    except Exception as e:
        print("\nCould not fetch events from API. Using saved events.")
        return load_events_from_file()

def save_events_to_file(events):
    existing = set(load_events_from_file())
    with open(EVENTS_FILE, "a", encoding="utf-8") as f:
        for e in events:
            if e not in existing:
                f.write(e + "\n")

def load_events_from_file():
    if not os.path.exists(EVENTS_FILE):
        return []
    with open(EVENTS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# ================= USER FUNCTIONS =================
def signup():
    global CURRENT_USER
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    if not username or not password:
        print("Fill in all fields!")
        return
    if username in USERS:
        print("User already exists!")
        return
    USERS[username] = password
    CURRENT_USER = username
    APPLICATIONS[username] = {}
    SAVED[username] = []
    print(f"Account created for {username}")

def login():
    global CURRENT_USER
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    if USERS.get(username) != password:
        print("Invalid credentials!")
        return
    CURRENT_USER = username
    print(f"Logged in as {username}")

# ================= EVENTS =================
def list_events():
    global EVENTS
    if not EVENTS:
        EVENTS.extend(fetch_events_from_api())
    print("\nAvailable Events:")
    for idx, event in enumerate(EVENTS, 1):
        print(f"{idx}. {event}")

def apply_event():
    list_events()
    if not EVENTS:
        print("No events available.")
        return
    try:
        idx = int(input("Enter event number to apply: ").strip()) - 1
        if idx < 0 or idx >= len(EVENTS):
            print("Invalid choice.")
            return
        event = EVENTS[idx]
        name = input("Full Name: ").strip()
        phone = input("Phone Number: ").strip()
        email = input("Email: ").strip()
        experience = input("Experience: ").strip()
        if not experience:
            print("Experience is required!")
            return
        APPLICATIONS.setdefault(CURRENT_USER, {})[event] = {
            "status": "Pending",
            "name": name,
            "phone": phone,
            "email": email,
            "experience": experience
        }
        print(f"Application for '{event}' submitted!")
    except ValueError:
        print("Invalid input.")

def save_event():
    list_events()
    if not EVENTS:
        return
    try:
        idx = int(input("Enter event number to save: ").strip()) - 1
        if idx < 0 or idx >= len(EVENTS):
            print("Invalid choice.")
            return
        event = EVENTS[idx]
        SAVED.setdefault(CURRENT_USER, []).append(event)
        print(f"'{event}' saved!")
    except ValueError:
        print("Invalid input.")

def view_profile():
    print(f"\nUser: {CURRENT_USER}")
    apps = APPLICATIONS.get(CURRENT_USER, {})
    if not apps:
        print("No applications yet.")
    else:
        for event, info in apps.items():
            print(f"\nEvent: {event}")
            for key, val in info.items():
                print(f"{key.capitalize()}: {val}")
    saved = SAVED.get(CURRENT_USER, [])
    if saved:
        print(f"\nSaved Events: {', '.join(saved)}")

# ================= MAIN MENU =================
def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. List Events")
        print("2. Apply for Event")
        print("3. Save Event")
        print("4. View Profile")
        print("5. Logout")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            list_events()
        elif choice == "2":
            apply_event()
        elif choice == "3":
            save_event()
        elif choice == "4":
            view_profile()
        elif choice == "5":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")

# ================= START APP =================
def start_cli():
    while True:
        print("\n=== Volunteering App ===")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            signup()
            if CURRENT_USER:
                main_menu()
        elif choice == "2":
            login()
            if CURRENT_USER:
                main_menu()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

# ================= RUN =================
if __name__ == "__main__":
    EVENTS.extend(fetch_events_from_api())
    start_cli()

