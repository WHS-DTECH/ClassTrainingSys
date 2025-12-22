print("These are the activities and costs")
activities = {"cultural immersion", "kayaking and pancakes", "mountain biking"}
for x in activities:
    print(x)
print("0 cultural immersion 5 easy 800")
print("1 kayaking & pancakes 3 moderate 400")
print("2 mountain biking 4 difficult 900")
name = input("what is your name?")
print("your name is: " + name) 

# DEBUG:
# Test: Test if its updating code --- User entered letters instead of a number
# Issue: Program crashed with ValueError
# Fix: Wrapped input in try/except block
age = input("enter age:")
print("your age is: " + age)
#https://www.w3schools.com/python/showpython.asp?filename=demo_user_input3
print("the different camps are: 0: cultural immersion 5 easy 800, 1: kayaking & pankcakes 3 moderate 400, 2: mountain biking 4 difficult 900")
camp = input("what camp do you want to go to?")
print("you would like to go to:" + camp) 
meal = "vegan"
print("the meals are:belle standard, vegeterian or vegan?") 
#print("what meal do you want: standard, vegeterian or vegan")  
a = "standard"
b = "vegeterian"
c = "vegan"
meal = input("what meal would you like?")
if a > b:
  print("your meal is standard")
elif c:
   print("your meal is vegan")
  #https://www.w3schools.com/python/trypython.asp?filename=demo_if2

shuttle_bus = "yes"
print("do you need the shuttle bus - extra $80?",shuttle_bus)
#print("do you need the shuttle bus - extra $80")
name = name
age = age
meal = meal
print(f"hello {name} you are {age}, it lasts 3 days, going to {camp}, your meal is {meal}")

conformation = input("please confirm you want to go with the cost 480 (yes/no): ")
if conformation == "yes":
  print("enjoy camp!")
else: 
   print("sorry! maybe next time")
print("These are the activities and costs")
activities = {"cultural immersion", "kayaking and pancakes", "mountain biking"}
for x in activities:
    print(x)
print("0 cultural immersion 5 easy 800")
print("1 kayaking & pancakes 3 moderate 400")
print("2 mountain biking 4 difficult 900")

name = input("what is your name?")
print("your name is: " + name) 
age = input("enter age:")
print("your age is: " + age)
#https://www.w3schools.com/python/showpython.asp?filename=demo_user_input3
print("the different camps are: 0: cultural immersion 5 easy 800, 1: kayaking & pankcakes 3 moderate 400, 2: mountain biking 4 difficult 900")
camp = input("what camp do you want to go to?")
print("you would like to go to:" + camp) 
meal = "vegan"
print("the meals are:belle standard, vegeterian or vegan?") 
#print("what meal do you want: standard, vegeterian or vegan")  
a = "standard"
b = "vegeterian"
c = "vegan"
meal = input("what meal would you like?")
if a > b:
  print("your meal is standard")
elif c:
   print("your meal is vegan")
  #https://www.w3schools.com/python/trypython.asp?filename=demo_if2

shuttle_bus = "yes"
print("do you need the shuttle bus - extra $80?",shuttle_bus)
#print("do you need the shuttle bus - extra $80")
name = name
age = age
meal = meal
print(f"hello {name} you are {age}, it lasts 3 days, going to {camp}, your meal is {meal}")

conformation = input("please confirm you want to go with the cost 480 (yes/no): ")
if conformation == "yes":
  print("enjoy camp!")
else: 
   print("sorry! maybe next time")
