# volunteering_app_terminal_api_with_settings.py
from flask import Flask, jsonify, request
import threading

# ================= MOCK DATABASE =================
USERS = {}
CURRENT_USER = None

EVENTS = [
    "Community Garden Build",
    "Beach Cleanup Day",
    "Tree Planting Drive",
    "Red Crescent Food Aid",
    "American Center Book Fair",
    "Community Tutoring",
    "Elderly Support Visit",
    "Animal Shelter Help",
    "Hospital Volunteer Program",
    "Recycling Awareness Event",
    "Charity Marathon",
    "Refugee Support Program",
    "WES Career Workshop",
    "EU Youth Conference",
    "Library Digitization"
]

APPLICATIONS = {}
SAVED = []

SETTINGS_INFO = {
    "About Us": "We connect volunteers with community events around the world.",
    "Contacts": "Email: soylishkamerdanova@gmail.com\nPhone: +99362760495",
    "Help Center": "Ask questions about volunteering by contacting our email or checking our FAQ.",
    "Privacy Policy": "We respect your privacy and will never share your information without consent."
}

# ================= CLI FUNCTIONS =================
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

def list_events():
    print("\nAvailable Events:")
    for idx, event in enumerate(EVENTS, 1):
        print(f"{idx}. {event}")
    print()

def apply_event():
    list_events()
    try:
        idx = int(input("Enter event number to apply: ").strip())
        if idx < 1 or idx > len(EVENTS):
            print("Invalid choice!")
            return
        choice = EVENTS[idx - 1]
    except ValueError:
        print("Please enter a valid number!")
        return

    experience = input("Experience (required): ").strip()
    if not experience:
        print("Experience is required!")
        return

    data = {
        "status": "Pending",
        "name": input("Full Name: ").strip(),
        "phone": input("Phone Number: ").strip(),
        "email": input("Email: ").strip(),
        "experience": experience,
        "link": input("Profile Link (optional): ").strip(),
        "bio": input("Bio (optional): ").strip()
    }
    APPLICATIONS.setdefault(CURRENT_USER, {})[choice] = data
    print(f"Application for '{choice}' sent!")

def save_event():
    list_events()
    try:
        idx = int(input("Enter event number to save: ").strip())
        if idx < 1 or idx > len(EVENTS):
            print("Invalid choice!")
            return
        choice = EVENTS[idx - 1]
    except ValueError:
        print("Please enter a valid number!")
        return

    SAVED.append(choice)
    print(f"'{choice}' saved!")

def view_profile():
    print(f"\nUser: {CURRENT_USER}")
    apps = APPLICATIONS.get(CURRENT_USER, {})
    if not apps:
        print("No applications yet")
    else:
        for event, d in apps.items():
            print(f"\nEvent: {event}\nStatus: {d['status']}\nName: {d['name']}\nEmail: {d['email']}\nPhone: {d['phone']}\nExperience: {d['experience']}")
            if d.get("link"):
                print(f"Link: {d['link']}")
            if d.get("bio"):
                print(f"Bio: {d['bio']}")
    if SAVED:
        print(f"\nSaved Events: {', '.join(SAVED)}")
    print()

def settings_menu():
    print("\n--- Settings ---")
    for idx, key in enumerate(SETTINGS_INFO.keys(), 1):
        print(f"{idx}. {key}")
    print(f"{len(SETTINGS_INFO) + 1}. Back")
    choice = input("Choose an option: ").strip()
    try:
        idx = int(choice)
        if idx == len(SETTINGS_INFO) + 1:
            return
        key = list(SETTINGS_INFO.keys())[idx - 1]
        print(f"\n{key}:\n{SETTINGS_INFO[key]}")
    except (ValueError, IndexError):
        print("Invalid choice!")

def main_menu_cli():
    global CURRENT_USER
    while True:
        print("\n--- Main Menu ---")
        print("1. List Events")
        print("2. Apply for Event")
        print("3. Save Event")
        print("4. View Profile")
        print("5. Settings")
        print("6. Logout")
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
            settings_menu()
        elif choice == "6":
            print("Logged out")
            CURRENT_USER = None
            break
        else:
            print("Invalid choice!")

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
                main_menu_cli()
        elif choice == "2":
            login()
            if CURRENT_USER:
                main_menu_cli()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

# ================= API =================
app = Flask(__name__)

@app.route("/api/events", methods=["GET"])
def api_events():
    return jsonify(EVENTS)

@app.route("/api/apply", methods=["POST"])
def api_apply():
    data = request.json
    username = data.get("username")
    event = data.get("event")
    experience = data.get("experience")
    if not username or not event or not experience:
        return jsonify({"error": "Missing required fields"}), 400
    if username not in USERS:
        return jsonify({"error": "User does not exist"}), 404
    if event not in EVENTS:
        return jsonify({"error": "Event does not exist"}), 404
    APPLICATIONS.setdefault(username, {})[event] = data
    return jsonify({"message": f"Application for {event} received"})

@app.route("/api/profile/<username>", methods=["GET"])
def api_profile(username):
    if username not in USERS:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "applications": APPLICATIONS.get(username, {}),
        "saved_events": SAVED
    })

@app.route("/api/settings/<key>", methods=["GET"])
def api_settings(key):
    info = SETTINGS_INFO.get(key)
    if not info:
        return jsonify({"error": "Invalid setting"}), 404
    return jsonify({key: info})

def run_api():
    app.run(port=5000)

# ================= START APP =================
if __name__ == "__main__":
    # Run API in a separate thread
    threading.Thread(target=run_api, daemon=True).start()
    # Start CLI
    start_cli()
