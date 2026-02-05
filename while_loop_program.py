# While 
secret_number = 7
guess = 0

print("🎯 Number Guessing Game")

while guess != secret_number:
    guess = int(input("Guess a number between 1 and 10: "))

print("🎉 Correct! You guessed the number.")
