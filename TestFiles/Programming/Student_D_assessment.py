#variables
curtural_immersion_cost = 800
kayaking_and_pancakes_cost = 400
mountain_biking_cost = 900
curtural_immersion = ("easy")
kayaking_and_pancakes = ("moderate")
mountain_biking = ("difficult")
name = input("What is your name?")
#loops
while name == "":
   print("You did not enter your name")
   name = input("What is your name?")
print("Hello {}".format(name))

age = int(input("How old are you {}?".format(name)))
while age < 5:
  print("you are too young for this camp")
  age = int(input("How old are you {}?".format(name)))
  if age > 17:
    print("you are too old for this camp")
    age = int(input("How old are you {}?".format(name)))
else:
  print("welcome!!")

shuttle_bus_cost = 80
#interface??
print("These are the activities and costs")
print("0 Cultural immersion 5 {} {}".format(curtural_immersion, curtural_immersion_cost))
print("1 Kayaking and pancakes 3 {} {}".format(kayaking_and_pancakes, kayaking_and_pancakes_cost))
print("2 Mountain biking 4 {} {}".format(mountain_biking, mountain_biking_cost))

#loops!!!
number_camp = int(input("What number camp do you want to go to?"))
while number_camp > 2:
  print("that is not an option")
  number_camp = int(input("What number camp do you want to go to?"))
  if number_camp == "":
    print("you did not enter a number")
    number_camp = int(input("What number camp do you want to go to?"))
else:
  print("Good choice")

meal_option = input("What meal do you want, standard, vegetarian or vegan?")
meal_option.lower()
if meal_option == "vegan":
  print("good")
elif meal_option == "vegetarian":
  print("nice")
elif meal_option == "standard":
  print("exellent")
else:
  print("We do not have some in stock")
  while meal_option == "":
    print("You have not entered anything")
    meal_option = input("What meal do you want, standard, vegetarian or vegan?")
  
shuttle_bus = input("Do you need the shuttle bus, it will cost an extra ${}".format(shuttle_bus_cost))
shuttle_bus.lower()
if shuttle_bus == "yes":
  print("That will be an extra $80")
elif shuttle_bus == "no":
  print("OK then")
else:
  print("Please enter 'yes' or 'no'")
  shuttle_bus = input("Do you need the shuttle bus, it will cost an extra ${}".format(shuttle_bus_cost))
  while shuttle_bus == False:
    print("Please enter 'yes' or 'no'")
    shuttle_bus = input("Do you need the shuttle bus, it will cost an extra ${}".format(shuttle_bus_cost))

#questions for variables 
camp_days = int(input("How long does the camp course youve chosen last?"))
while camp_days < 3:
  print("we do not hhave a camp that lasts that long")
  camp_days = int(input("How long does the camp course youve chosen last?"))
  if camp_days > 5:
    print("we do not hhave a camp that lasts that long")
    camp_days = int(input("How long does the camp course youve chosen last?"))
  else:
    print("Thank you for your answer")

camp_type = input("which camp have you chosen?")
camp_type.lower()
if camp_type == "cultural immersion":
  print("Very good choice")
elif camp_type == "kayaking and pancakes":
  print("Good choice")
elif camp_type == "mountain biking":
  print("Exellent")
else:
  print("That is not an option")
  while camp_type == False:
    print("Thats not an option")
    camp_type = input("which camp have you chosen?")

difficulty = input("What is the difficulty of the camp you have chosen?")
difficulty.lower()
if difficulty == "easy":
  print("Good on you")
elif difficulty == "moderate":
  print("Gong up a notch eh?")
elif difficulty == "difficult":
  print("Wow! Good job")
else:
  print("thats not an option")
  while difficulty == False:
    print("thats not an option")
    difficulty = input("What is the difficulty of the camp you have chosen?")


#final statement
print("Ok {} you are {}, it lasts {} days, you're going {} which is {}, your meal option is {}".format(name, age, camp_days, camp_type, difficulty, meal_option))\

#total
camp_type_cost = int(input("How much does the camp cost that youve chosen"))
if camp_type_cost == 400:
  print("Good good")
elif camp_type_cost == 800:
  print("Good Great")
elif camp_type_cost == 900:
  print("Great great")
else:
  print("None of our options cost that much")
  while camp_type_cost == False:
    print("None of our options cost that much")
    camp_type_cost = int(input("How much does the camp cost that youve chosen"))

total = (camp_type_cost + shuttle_bus)
print("Your total is ${}".format(total))