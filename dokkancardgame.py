import tkinter as tk


def ouvrirfenetre(fermer, ouverte):
    fermer.destroy()
    ouverte()

def lapartie(pvjoueur, pvboss):
    partiefenetre = tk.Tk()
    partiefenetre.title("Jeu de cartes")

    # Styles
    bg_color = "#f0f0f0"
    partiefenetre.configure(bg=bg_color)

    label_pvboss = tk.Label(partiefenetre, text=f"PV du boss : {pvboss}", bg=bg_color, font=("Helvetica", 16))
    label_pvboss.pack(pady=10)

    label_pvjoueur = tk.Label(partiefenetre, text=f"PV du joueur : {pvjoueur}", bg=bg_color, font=("Helvetica", 16))
    label_pvjoueur.pack(pady=10)

    label_pvenlevé = tk.Label(partiefenetre, text="PV enlevé", bg=bg_color)
    label_pvenlevé.pack(side=tk.LEFT, padx=10)

    pveneleveentry = tk.Entry(partiefenetre)
    pveneleveentry.pack(side=tk.LEFT, padx=10)  

    def enleverauboss():
        nonlocal pvboss
        if pvboss <= 0:
            return
        try:
            pvenleve = int(pveneleveentry.get()) 
            pvboss -= pvenleve
            label_pvboss.config(text=f"PV du boss : {pvboss}")
            check_fin_de_jeu()
        except ValueError:
            print("Erreur : Veuillez entrer un nombre valide.")

    def enleveraujoueur():
        nonlocal pvjoueur
        if pvjoueur <= 0:
            return
        try:
            pvenleve = int(pveneleveentry.get()) 
            pvjoueur -= pvenleve
            label_pvjoueur.config(text=f"PV du joueur : {pvjoueur}")
            check_fin_de_jeu()
        except ValueError:
            print("Erreur : Veuillez entrer un nombre valide.")

    def check_fin_de_jeu():
        if pvboss <= 0:
            label_pvboss.config(text="Le boss est vaincu !")
            partiefenetre.after(2000, lambda: ouvrirfenetre(partiefenetre, menu))
        elif pvjoueur <= 0:
            label_pvjoueur.config(text="Le joueur est vaincu !")
            partiefenetre.after(2000, lambda: ouvrirfenetre(partiefenetre, menu))

    # Boutons
    enleveraubosse = tk.Button(partiefenetre, text="Enlever au boss", command=enleverauboss, bg="#ffcccb")
    enleveraubosse.pack(pady=5)

    enleveraujoueure = tk.Button(partiefenetre, text="Enlever au joueur", command=enleveraujoueur, bg="#add8e6")
    enleveraujoueure.pack(pady=5)

    partiefenetre.mainloop()

def menu():
    menufenetre = tk.Tk()
    menufenetre.title("Menu Principal")

    gocomptage = tk.Button(menufenetre, text="Nouvelle partie", command=lambda: ouvrirfenetre(menufenetre, comptage), bg="#90ee90")
    gocomptage.pack(pady=20)

    menufenetre.mainloop()

def comptage():
    comptagefenetre = tk.Tk()
    comptagefenetre.title("Paramètres de la Partie")

    label_pvboss = tk.Label(comptagefenetre, text="PV du boss :", font=("Helvetica", 14))
    label_pvboss.pack(side=tk.LEFT)

    pvbossentry = tk.Entry(comptagefenetre)
    pvbossentry.pack(side=tk.LEFT)
    pvbossentry.insert(0, "20")

    label_pvjoueur = tk.Label(comptagefenetre, text="PV du joueur :", font=("Helvetica", 14))
    label_pvjoueur.pack(side=tk.LEFT)

    pvgars = tk.Entry(comptagefenetre)
    pvgars.pack(side=tk.LEFT)
    pvgars.insert(0, "50")

    lancerlapartie = tk.Button(comptagefenetre, text="Lancer la partie", command=lambda: lancerpartie(pvbossentry, pvgars), bg="#ffa07a")
    lancerlapartie.pack(pady=10)

    def lancerpartie(pvbosse, pvgars):
        try:
            pvboss = int(pvbosse.get()) 
        except ValueError:
            print("Erreur : Veuillez entrer un nombre valide.")
            return

        try:
            pvjoueur = int(pvgars.get())  
        except ValueError:
            print("Erreur : Veuillez entrer un nombre valide.")
            return

        ouvrirfenetre(comptagefenetre, lambda: lapartie(pvjoueur, pvboss))

    comptagefenetre.mainloop()

menu()
