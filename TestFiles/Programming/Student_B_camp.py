i = "easy"
j = "moderate"
k = "difficult"
food = True
camp = True
dif = []
price = 0
campend = True
foods = ["standard", "vegeterian", "vegan"]
print("These are the activities and cost: \n")

print("$800:")
print("Cultural immersion, last 5 days.")
print("Difficulty: 1, {}\n".format(i))

print("$400:")
print("Kayaking and pancakes, last 3 days.")
print("Difficulty: 2, {}\n".format(j))

print("$900:")
print("Mountain biking, last 4 days.")
print("Difficulty: 3, {}\n".format(k))
# stats over, nerdy inputs initiate!!
print("Signup:")
aks = input("What is your name?: ")
aks2 = int(input("How old are you?:"))
# Is there a simpler way I couldve done this?
while camp == True:
 ask2 = int(input("(Number 1-3)\nWhich camp would are you choosing?: ").strip().title())
 if ask2 > 3:
  print("Not a valid camp option.\n")
 elif ask2 == 3:
  price += 900
 elif ask2 == 2:
  price += 400
 elif ask2 == 1:
  price += 800
 if ask2 <= 3:
  camp = False
# question will continue until you choose a correct option
print("Theres 3 food types:\nstandard, vegeterian, and vegan\n")
while food == True:
 grask = input("Which food option would you like?: ").strip().lower()
 count = foods.count(grask)
 if grask in foods:
  food = False
 
 else:
  print("Please pick a specific food option.\n")



 
ask4 = input("\nDo you need the shuttle bus?\nthis will cost $80 more. ")
if ask4 == "yes":
 price += 80
while campend == True:
 print("\nHi {}.\nYou are currently {}, You will be going to Option {} which is classed as difficulty {}.".format(aks, aks2, ask2, ask2))
 print("Your food choice is {}.\n".format(grask))
 end = input("This will cost ${} are you sure? ".format(price)).strip().lower()
 if end == "yes":
  print("Enjoy the camp!")
  campend = False
  # if you accidentally picked the wrong option:
 elif end == "no":
  print("Here, redo that bit again")
  price -= 80
  ask4 = input("\nDo you need the shuttle bus?\nthis will cost $80 more.")