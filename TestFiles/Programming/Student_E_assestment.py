# Introduction message 
print("Welcome to the Adventure Camp Activity Selection! You will choose your preferred activities, meals, and shuttle options")

# Get user information (name and age)
name = input("What is your name? =")
print("Hello", name)
age = "15"
print("What is your Age?=", age)
#print("What is your Age? 15")
#https://www.w3schools.com/python/trypython.asp?filename=demo_for

# Displaying avaliable activities
print("Available Activities:")
Activities = ["Cultural Immersion", "Kayaking & pancakes", "Mountain Biking "]
for x in Activities:
  print(x) 

# Displaying activity options with details 
print("Available Activities:")
print("0:Cultural Immersion (Difficulty: Easy, Cost: $800)")
print("1:Kayaking & pancakes (Difficulty: Moderate, cost: $400)")
print("2:Mountain Biking (Difficulty: Difficult, cost: $900)")

# Activity choice from user
activity_choice = int(input("What activity would you be interested in? (0-2):")) 
if activity_choice == 0:
 print("Great choice! You picked Cultural Immersion, this activity explores different cultures!")
elif activity_choice == 1:
 print("Amazing decision! Kayaking & pancakes are my favorite!")
elif activity_choice == 2:
 print("Brave choice! You must be a risk taker!") 
    

# Meal preference 
meal = "vegan"
print("What meal do you want? Meal Variety is: Standard, vegetarian or vegan: =", meal)
#print("What meal do you want? Meal Variety is: Standard, vegetarian or vegan: vegan ")

# Shuttle bus
shuttle_bus = "Yes" 
print("Do you need the shuttle bus? if so -Extra $80 (Yes/No): =", shuttle_bus)
#print("Do you need the shuttle bus? if so -Extra $80 (Yes/No): Yes ")

# Summary of choices
print("Your Adventure Camp Summary")
print("Hello, Lara! Thank you for choosing our adventure camp.")

name = "Lara"
print("Name: =", name)
#print("Name: Lara")

age = "15"
print("Age: =", age)
#print("Age: 15")

print("Selected Activity:")
print(" Kayaking & pancakes (Difficulty: Moderate)")

meal = "vegan"
print("Meal preference: =", meal)
#print("Meal preference: vegan")

shuttle_bus = "Yes"
print("shuttle_bus - extra $80 =", shuttle_bus)
#print("Shuttle bus: Yes")


Total_cost = "$480"
print("Total cost: =", Total_cost)
#print("Total cost: $480")


#Confirmation and payment message 

print("Please confirm your selection. Do you want to proceed with payment? (yes/no): yes")
print("Payment processed. Thank you for booking your adventure with us, Lara!")
print("Your total cost of $480 has been successfully paid. ")
