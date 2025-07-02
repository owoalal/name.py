from tkinter.font import names
print ("what is your name?")
import re

while True:
    name = input("Please enter your name: ")
    names={"mhd"}
    if name in names:
        print("name is banned")
    elif re.search(r'\d', name):
        print("Name cannot contain numbers. Please try again.")
    elif len(name) > 15:
        print("Name cannot exceed 15 characters. Please try again.")
    elif name:
        print(f"Hello, {name}!")
        break
    else:
        print("Nothing is inputted. Please try again.")


while True:
    password = input("Please choose your password: ")
    passwords = {"12345678"}
    if password in passwords:
        print("password is too weak")
    elif len(password) >= 8:
        break
    else:
        print("Password must be at least 8 characters. Please try again.")


with open('passwords.txt', 'a') as f:
    f.write(f'{name}:{password}\n')





print(f"Hello, {name}! Your password has been saved to a file.")
print("Thank you for chosing this program! and good bye")