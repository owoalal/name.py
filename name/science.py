import random
def main():
    print("Nous allons calculer des propriétés chimiques.")
    print("Choisissez une option :\n"
          "1 : Masse\n"
          "2 : Concentration massique\n"
          "3 : Masse volumique\n"
          "4 : Volume\n"
          "5 : Nouvelle concentration après ajout d'eau\n"
          "6 : Masse volumique et concentration massique d'une solution sucrée\n"
          "7 : Calcul entre V_initial, gamma_initial, V_final, gamma_final")

    while True:
        choice = input("Que voulez-vous calculer ? (1/2/3/4/5/6/7) ou 'q' pour quitter : ").strip().lower()

        if choice == "1":
            print("Calcul de la masse : m = C * V")
            C = float(input("Entrez la concentration massique (en g/L) : "))
            V = float(input("Entrez le volume (en L) : "))
            m = C * V
            print(f"La masse est : {m:.2f} g")

        elif choice == "2":

            print("Calcul de la concentration massique : C = m / V")
            m = float(input("Entrez la masse (en g) : "))
            V = float(input("Entrez le volume (en L) : "))
            if V != 0:
                C = m / V
                print(f"La concentration massique est : {C:.2f} g/L")
            else:
                print("Erreur : le volume ne peut pas être nul.")

        elif choice == "3":

            print("Calcul de la masse volumique : rho = m / V")
            m = float(input("Entrez la masse (en g) : "))
            V = float(input("Entrez le volume (en cm³ ou mL) : "))
            if V != 0:
                rho = m / V
                print(f"La masse volumique est : {rho:.2f} g/cm³")
            else:
                print("Erreur : le volume ne peut pas être nul.")

        elif choice == "4":

            print("Calcul du volume : V = m / C")
            m = float(input("Entrez la masse (en g) : "))
            C = float(input("Entrez la concentration massique (en g/L) : "))
            if C != 0:
                V = m / C
                print(f"Le volume est : {V:.2f} L")
            else:
                print("Erreur : la concentration massique ne peut pas être nulle.")


        elif choice == "5":
            print("Calcul de la nouvelle concentration après ajout d'eau")
            V1 = float(input("Entrez le volume initial de la solution (en L) : "))
            gamma1 = float(input("Entrez la concentration massique initiale (en g/L) : "))
            V2 = float(input("Entrez le volume d'eau ajouté (en L) : "))
            m = gamma1 * V1
            V_total = V1 + V2
            gamma2 = m / V_total
            print(f"La nouvelle concentration massique est : {gamma2:.2f} g/L")

        elif choice == "6":

            print("Calcul de la masse volumique et de la concentration massique d'une solution sucrée")
            m_solution = float(input("Entrez la masse totale de la solution (en g) : "))
            V_solution = float(input("Entrez le volume de la solution (en mL) : "))
            m_sucre = float(input("Entrez la masse de sucre (en g) : "))
            rho = m_solution / V_solution
            gamma = m_sucre / (V_solution / 1000)
            print(f"La masse volumique est : {rho:.2f} g/mL")
            print(f"La concentration massique est : {gamma:.2f} g/L")

        elif choice == "7":

            print("Calcul basé sur la formule : V_initial * gamma_initial = V_final * gamma_final")
            V_initial = input("Entrez le volume initial (en L) ou X si inconnu : ").strip().lower()
            gamma_initial = input("Entrez la concentration initiale (en g/L) ou X si inconnue : ").strip().lower()
            V_final = input("Entrez le volume final (en L) ou X si inconnu : ").strip().lower()
            gamma_final = input("Entrez la concentration finale (en g/L) ou X si inconnue : ").strip().lower()

            values = {
                "V_initial": None if V_initial == "x" else float(V_initial),
                "gamma_initial": None if gamma_initial == "x" else float(gamma_initial),
                "V_final": None if V_final == "x" else float(V_final),
                "gamma_final": None if gamma_final == "x" else float(gamma_final),
            }

            if values["V_initial"] is None:
                if values["gamma_final"] and values["gamma_initial"] and values["V_final"]:
                    V_initial = (values["gamma_final"] * values["V_final"]) / values["gamma_initial"]
                    print(f"Le volume initial est : {V_initial:.2f} L")
            elif values["gamma_initial"] is None:
                if values["V_initial"] and values["gamma_final"] and values["V_final"]:
                    gamma_initial = (values["gamma_final"] * values["V_final"]) / values["V_initial"]
                    print(f"La concentration initiale est : {gamma_initial:.2f} g/L")
            elif values["V_final"] is None:
                if values["gamma_initial"] and values["V_initial"] and values["gamma_final"]:
                    V_final = (values["gamma_initial"] * values["V_initial"]) / values["gamma_final"]
                    print(f"Le volume final est : {V_final:.2f} L")
            elif values["gamma_final"] is None:
                if values["gamma_initial"] and values["V_initial"] and values["V_final"]:
                    gamma_final = (values["gamma_initial"] * values["V_initial"]) / values["V_final"]
                    print(f"La concentration finale est : {gamma_final:.2f} g/L")
            else:
                print("Vous avez déjà toutes les valeurs. Aucun calcul nécessaire.")

        elif choice == "secret":
            russian = input("wanna play russian roulette? (yes/no): ")
            if russian.lower() == 'yes':
                while True:
                    print("Russian roulette started")

                    gun = random.randint(0, 6)

                    if gun == 1:
                        print("You lost the game.")
                        break
                    else:
                        print("You are still alive.")

                    continue1 = input("Do you want to play again? (yes/no): ").strip().lower()
                    if continue1 != 'yes':
                        break


            else:
                print("Russian roulette cancelled")
                print("dont ever try to play russian roulette pussy ")


        elif choice == "q":
            print("Merci d'avoir utilisé le programme ! À bientôt.")
            break



        else:
            print("Choix invalide. Veuillez entrer un numéro d'option valide ou 'q' pour quitter.")


if __name__ == "__main__":
    main()
