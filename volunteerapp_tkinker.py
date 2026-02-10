import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

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
SAVED = {}

# ================= FUNCTIONS =================
def signup_window(root):
    def signup_action():
        global CURRENT_USER
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Fill in all fields!")
            return
        if username in USERS:
            messagebox.showerror("Error", "User already exists!")
            return
        USERS[username] = password
        CURRENT_USER = username
        APPLICATIONS[username] = {}
        SAVED[username] = []
        messagebox.showinfo("Success", f"Account created for {username}")
        root.destroy()
        main_menu()

    win = tk.Toplevel()
    win.title("Sign Up")
    tk.Label(win, text="Username:").pack()
    username_entry = tk.Entry(win)
    username_entry.pack()
    tk.Label(win, text="Password:").pack()
    password_entry = tk.Entry(win, show="*")
    password_entry.pack()
    tk.Button(win, text="Sign Up", command=signup_action).pack(pady=5)

def login_window(root):
    def login_action():
        global CURRENT_USER
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if USERS.get(username) != password:
            messagebox.showerror("Error", "Invalid credentials!")
            return
        CURRENT_USER = username
        messagebox.showinfo("Success", f"Logged in as {username}")
        root.destroy()
        main_menu()

    win = tk.Toplevel()
    win.title("Login")
    tk.Label(win, text="Username:").pack()
    username_entry = tk.Entry(win)
    username_entry.pack()
    tk.Label(win, text="Password:").pack()
    password_entry = tk.Entry(win, show="*")
    password_entry.pack()
    tk.Button(win, text="Login", command=login_action).pack(pady=5)

# ================= EVENTS =================
def events_window():
    def apply_event(event):
        apply_win = tk.Toplevel()
        apply_win.title(f"Apply for {event}")

        entries = {}
        labels = ["Full Name", "Phone Number", "Email", "Experience (required)", "Profile Link (optional)", "Bio (optional)"]
        for lbl in labels:
            tk.Label(apply_win, text=lbl + ":").pack()
            entry = tk.Entry(apply_win, width=50)
            entry.pack(pady=2)
            entries[lbl] = entry

        def submit():
            experience = entries["Experience (required)"].get().strip()
            if not experience:
                messagebox.showerror("Error", "Experience is required!")
                return
            data = {
                "status": "Pending",
                "name": entries["Full Name"].get().strip(),
                "phone": entries["Phone Number"].get().strip(),
                "email": entries["Email"].get().strip(),
                "experience": experience,
                "link": entries["Profile Link (optional)"].get().strip(),
                "bio": entries["Bio (optional)"].get().strip()
            }
            APPLICATIONS.setdefault(CURRENT_USER, {})[event] = data
            messagebox.showinfo("Success", "Application sent!")
            apply_win.destroy()

        tk.Button(apply_win, text="Submit Application", command=submit).pack(pady=5)

    win = tk.Toplevel()
    win.title("Events")

    tk.Label(win, text="Available Events:", font=("Arial", 14)).pack(pady=5)
    for event in EVENTS:
        frame = tk.Frame(win)
        frame.pack(fill="x", pady=2)
        tk.Label(frame, text=event).pack(side="left")
        tk.Button(frame, text="Apply", command=lambda e=event: apply_event(e)).pack(side="right")
        tk.Button(frame, text="Save", command=lambda e=event: (SAVED.setdefault(CURRENT_USER, []).append(e),
                                                                 messagebox.showinfo("Saved", f"{e} saved!"))).pack(side="right")

# ================= PROFILE =================
def profile_window():
    win = tk.Toplevel()
    win.title("Profile")
    tk.Label(win, text=f"User: {CURRENT_USER}", font=("Arial", 14)).pack(pady=5)

    apps = APPLICATIONS.get(CURRENT_USER, {})
    if not apps:
        tk.Label(win, text="No applications yet").pack()
    else:
        for event, d in apps.items():
            text = f"Event: {event}\nStatus: {d['status']}\nName: {d['name']}\nEmail: {d['email']}\nPhone: {d['phone']}\nExperience: {d['experience']}"
            if d.get("link"):
                text += f"\nLink: {d['link']}"
            if d.get("bio"):
                text += f"\nBio: {d['bio']}"
            tk.Label(win, text=text, justify="left", relief="groove", padx=5, pady=5).pack(fill="x", pady=2)

# ================= SETTINGS =================
def settings_window():
    win = tk.Toplevel()
    win.title("Settings")

    def show_info(title, text):
        info_win = tk.Toplevel()
        info_win.title(title)
        tk.Label(info_win, text=text, wraplength=400, justify="left").pack(padx=10, pady=10)

    tk.Button(win, text="About Us", width=20, command=lambda: show_info("About Us", "We connect volunteers with community events around the world.")).pack(pady=2)
    tk.Button(win, text="Contacts", width=20, command=lambda: show_info("Contacts", "Email: soylishkamerdanova@gmail.com\nPhone: +99362760495")).pack(pady=2)
    tk.Button(win, text="Help Center", width=20, command=lambda: show_info("Help Center", "Ask questions about volunteering by contacting our email or checking our FAQ.")).pack(pady=2)
    tk.Button(win, text="Privacy Policy", width=20, command=lambda: show_info("Privacy Policy", "We respect your privacy and will never share your information without consent.")).pack(pady=2)

# ================= MAIN MENU =================
def main_menu():
    root = tk.Tk()
    root.title("Volunteering App - Main Menu")

    tk.Label(root, text=f"Welcome, {CURRENT_USER}", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Events", width=25, command=events_window).pack(pady=5)
    tk.Button(root, text="Profile", width=25, command=profile_window).pack(pady=5)
    tk.Button(root, text="Settings", width=25, command=settings_window).pack(pady=5)
    tk.Button(root, text="Logout", width=25, command=root.destroy).pack(pady=5)

    root.mainloop()

# ================= START APP =================
def start_app():
    root = tk.Tk()
    root.title("Volunteering App")

    tk.Label(root, text="Welcome to Volunteering App", font=("Arial", 16)).pack(pady=10)
    tk.Button(root, text="Login", width=20, command=lambda: login_window(root)).pack(pady=5)
    tk.Button(root, text="Sign Up", width=20, command=lambda: signup_window(root)).pack(pady=5)
    tk.Button(root, text="Exit", width=20, command=root.destroy).pack(pady=5)

    root.mainloop()

start_app()
