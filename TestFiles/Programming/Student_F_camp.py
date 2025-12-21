def camp_registration():
    activities = {
        0: ("Cultural immersion", "easy", 800),
        1: ("Kayaking & pancakes", "moderate", 400),
        2: ("Mountain biking", "difficult", 900)
    }
    # DEBUG TEST: Entered "yes" as shuttle choice
# DEBUG ISSUE: Shuttle is "no" accepted
# DEBUG FIX: Changed condition to shuttle in ["yes", "no"]
# DEBUG FIX VERIFIED: Re-tested with yes and no – correctly accepted both inputs
    name = input("What is your name? ")
    age = input("What is your age? ")
    camp_choice = int(input("What number camp do you want to go to? (0 - Cultural immersion, 1 - Kayaking & pancakes, 2 - Mountain biking): "))
    meal_choice = input("What meal do you want: standard, vegetarian, or vegan? ")
    shuttle = input("Do you need the shuttle bus - extra $80? (yes/no) ")
    
    activity, difficulty, cost = activities.get(camp_choice, ("Unknown", "Unknown", 0))
    total_cost = cost + (80 if shuttle.lower() == "yes" else 0)
    
    print(f"\nHello {name}, you are {age}, it lasts 3 days, going to {activity} which is {difficulty}, your meal is {meal_choice}.")
    print(f"Please confirm you want to go with the cost of {total_cost}")
    confirmation = input("Type 'yes' to confirm: ")
    
    if confirmation.lower() == "yes":
        print("Enjoy the camp!")
    else:
        print("Registration not confirmed.")

camp_registration()
