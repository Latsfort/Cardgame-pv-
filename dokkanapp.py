import tkinter as tk
import time

def ouvrirfenetre(fermer, ouverte):
    fermer.destroy()
    ouverte()

def lapartie(pvjoueur,pvboss):

    partiefenetre = tk.Tk()

    label_pvboss = tk.Label(partiefenetre, text="")
    label_pvboss.pack()

    label_pvjoueur = tk.Label(partiefenetre, text ="")
    label_pvjoueur.pack()

    label_pvboss.config(text=f"PV du boss : {pvboss}")
    label_pvjoueur.config(text=f"PV du joueur : {pvjoueur}")   
    

    label_pvenlevé = tk.Label(partiefenetre, text="PV enlevé")
    label_pvenlevé.pack(side=tk.LEFT)  

    pveneleveentry = tk.Entry(partiefenetre)
    pveneleveentry.pack()  

    def enleverauboss():
        nonlocal pvboss
        try:
            pvenleve = int(pveneleveentry.get()) 
        except ValueError:
            print("erreur enlever pvboss")

        pvboss= pvboss-pvenleve

        label_pvboss.config(text=f"PV du boss : {pvboss}")

        check_fin_de_jeu()

    def enleveraujoueur():
        nonlocal pvjoueur
        try:
            pvenleve = int(pveneleveentry.get()) 
        except ValueError:
            print("erreur enlever joueur")
        pvjoueur= pvjoueur-pvenleve

        label_pvjoueur.config(text=f"PV du joueur : {pvjoueur}")   

        check_fin_de_jeu()
      
    #boutons
    enleveraubosse= tk.Button(partiefenetre,text="enlever au boss", command=enleverauboss)
    enleveraubosse.pack()

    enleveraujoueure= tk.Button(partiefenetre,text="enlever au joueur", command=enleveraujoueur)
    enleveraujoueure.pack()

    def check_fin_de_jeu():
        if pvboss <= 0:
            label_pvboss.config(text="Le boss est vaincu !")
            partiefenetre.after(2000, lambda: ouvrirfenetre(partiefenetre, menu))
        elif pvjoueur <= 0:
            label_pvjoueur.config(text="Le joueur est vaincu !")
            partiefenetre.after(2000, lambda: ouvrirfenetre(partiefenetre, menu))

    partiefenetre.mainloop()

def menu():
    menufenetre = tk.Tk()

    gocomptage = tk.Button(menufenetre, text="Nouvelle partie", command=lambda: ouvrirfenetre(menufenetre, comptage))
    gocomptage.pack()

    menufenetre.mainloop()

def comptage():
    comptagefenetre = tk.Tk()

    # Label pour les PV du boss
    label_pvboss = tk.Label(comptagefenetre, text="PV du boss:")
    label_pvboss.pack(side=tk.LEFT)  # Aligner à gauche

    # Champ d'entrée pour les PV du boss
    pvbossentry = tk.Entry(comptagefenetre)
    pvbossentry.pack(side=tk.LEFT)  # Aligner à gauche
    pvbossentry.insert(0, "20")  # Texte par défaut

    # Label pour les PV du joueur
    label_pvjoueur = tk.Label(comptagefenetre, text="PV du joueur:")
    label_pvjoueur.pack(side=tk.LEFT)  # Aligner à gauche

    # Champ d'entrée pour les PV du joueur
    pvgars = tk.Entry(comptagefenetre)
    pvgars.pack(side=tk.LEFT)  # Aligner à gauche
    pvgars.insert(0, "50")  # Texte par défaut

    # Créer le label pour afficher le résultat
    '''label_pvboss = tk.Label(comptagefenetre, text="")
    label_pvboss.pack()

    label_pvjoueur = tk.Label(comptagefenetre, text ="")
    label_pvjoueur.pack()'''

    #boutons
    lancerlapartie= tk.Button(comptagefenetre,text="lancer la partie", command=lambda: lancerpartie(pvbossentry,pvgars))
    lancerlapartie.pack()


    def lancerpartie(pvbosse,pvgars):

        try:
            pvboss = int(pvbosse.get()) 
            #label_pvboss.config(text=f"PV du boss : {pvboss}")
        except ValueError:
            #label_pvboss.config(text="Veuillez entrer un nombre")
            print("erreur pvboss")

        try:
            pvjoueur = int(pvgars.get())  
            #label_pvjoueur.config(text=f"PV du joueur : {pvjoueur}")
        except ValueError:
            #label_pvjoueur.config(text="Veuillez entrer un nombre")
            print("erreur pvjoueur")

        ouvrirfenetre(comptagefenetre,lambda:lapartie(pvjoueur, pvboss))

    comptagefenetre.mainloop()

menu()

