# Decision Maker Program
# This program helps the user decide how to study
# It uses if / elif / else based on user answers

print("📚 Study Method Decision Maker")

# Ask at least 3 questions
subject = input("What subject are you studying? (math / reading / coding): ").lower()
time = input("How much time do you have? (short / long): ").lower()
style = input("How do you learn best? (visual / practice / listening): ").lower()

# Decision logic
# We check combinations of answers and give recommendations

if subject == "math" and time == "long":
    print("✅ You should do practice problems and review mistakes.")
elif subject == "reading" and style == "listening":
    print("🎧 Try an audiobook or reading out loud.")
elif subject == "coding" and style == "practice":
    print("💻 Build a small project or solve coding exercises.")
else:
    print("📖 Try reviewing notes and doing light practice.")
