print("what is your tabaro3?")
import re


while True:
    why = input("why are you doing tabaro3: ")
    if not why.strip():
        print("Input cannot be empty. Please try again.")
        continue
    if re.search(r'\d', why):
        print("Invalid input. Please try again.")
        continue
    elif len(why) < 5:
        print("reason must be at least 5 characters. Please try again.")
        continue
    x = input("Please enter your tabaro3: ")
    if not x.strip():
        print("Input cannot be empty. Please try again.")
        continue
    if re.search(r'\D', x):
        print("Invalid input. Please try again.")
        continue
    if int(x) <= 100:
        print("you is to poor for this world dont do tabroo3 now")
        continue
    else:
        print(f"Your tabaro3 is: {x}")
    break





while True:
    y = input("Please enter your nuber of countries you want to give tabaro3 for: ")
    if not y.strip():
        print("Input cannot be empty. Please try again.")
        continue
    if re.search(r'\D', y):
        print("Invalid input. Please try again.")

        continue

    z = int(x) / int(y)

    print (f"Your reason is: {why}")
    print(f"Each country will receive: {round(z)}")
    print ("you rest is: ", int(x) % int(y))


    break