# Camp details stored in a dictionary
CAMPS = {
    "Cultural immersion": {"days": 5, "difficulty": "easy", "cost": 800},
    "Kayaking and pancakes": {"days": 3, "difficulty": "moderate", "cost": 400},
    "Mountain biking": {"days": 4, "difficulty": "difficult", "cost": 900}
}
SHUTTLE_COST = 80

# Function to get valid age input

# DEBUG:
# Test: Test if its updating code --- User entered letters instead of a number
# Issue: Program crashed with ValueError
# Fix: Wrapped input in try/except block

try:
    age = int(input("Enter your age: "))
except ValueError:
    print("Please enter a number")
def get_valid_age():
    while True:
        try:
            age = int(input("Enter your age (5-17): "))
            if 5 <= age <= 17:
                return age
            else:
                print("Invalid age. Must be between 5 and 17.")
        except ValueError:
            print("Please enter a valid number.")

# Function to get valid camp choice
def get_valid_camp():
    print("Available camps:")
    for camp in CAMPS:
        print(f"- {camp} ({CAMPS[camp]['days']} days, {CAMPS[camp]['difficulty']}, ${CAMPS[camp]['cost']})")
    while True:
        camp_choice = input("Choose a camp: ")
        if camp_choice in CAMPS:
            return camp_choice
        print("Invalid choice. Please select from the list.")

# Function to get valid meal choice
def get_valid_meal():
    MEAL_OPTIONS = ["standard", "vegetarian", "vegan"]
    while True:
        meal_choice = input("Choose a meal (standard, vegetarian, vegan): ").lower()
        if meal_choice in MEAL_OPTIONS:
            return meal_choice
        print("Invalid choice. Please select a valid meal option.")

# Function to check if shuttle is needed

# DEBUG TEST: Entered "yes" as shuttle choice
# DEBUG ISSUE: Shuttle is "no" accepted
# DEBUG FIX: Changed condition to shuttle in ["yes", "no"]
# DEBUG FIX VERIFIED: Re-tested with yes and no – correctly accepted both inputs

def get_shuttle_choice():
    while True:
        shuttle = input("Do you need a shuttle bus? (yes/no): ").lower()
        if shuttle in ["yes", "no"]:
            return shuttle == "yes"
        print("Please answer 'yes' or 'no'.")

# Function to confirm attendance
def confirm_attendance():
    while True:
        confirm = input("Confirm your attendance? (yes/no): ").lower()
        if confirm in ["yes", "no"]:
            return confirm == "yes"
        print("Please answer 'yes' or 'no'.")

# Main program execution
print("Welcome to the Holiday Camp Registration!")
name = input("Enter your first and last name: ")
age = get_valid_age()
camp_choice = get_valid_camp()
meal_choice = get_valid_meal()
shuttle = get_shuttle_choice()
total_cost = CAMPS[camp_choice]['cost'] + (SHUTTLE_COST if shuttle else 0)

# Print formatted summary
print(f"\n{name}, age {age}, has chosen the {camp_choice} camp which is  {CAMPS[camp_choice]['days']} days.")
print(f"Difficulty level: {CAMPS[camp_choice]['difficulty']}, Meal choice: {meal_choice}.")
print(f"Total cost: ${total_cost}")

# Confirm attendance
if confirm_attendance():
    print("You are successfully registered for the camp")
else:
    print("Registration cancelled.")