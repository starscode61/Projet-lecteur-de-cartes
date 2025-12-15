import json
import tkinter as tk
from tkinter import PhotoImage
import tkinter.ttk as ttk

with open("eleves.json", "r", encoding="utf-8") as f:
    base = json.load(f)

carte_prof = None
eleves = {}

for identifiant, nom in base.items():
    if nom == "Professeur":
        carte_prof = identifiant
    else:
        eleves[identifiant] = nom

presents = []


def verifier(event):
    id = entree.get()
    entree.delete(0, tk.END)
    entree.focus_set()

    if id not in base:
        resultat.config(text="Identifiant inconnu")
        return

    if id == carte_prof:
        absents = []
        for nom in eleves.values():
            if nom not in presents:
                absents.append(nom)

        if len(absents) > 0:
            resultat.config(text="il y a "+ str(len(absents)) +" élèves absents :\n" + "\n".join(absents))
        else:
            resultat.config(text="Tous les élèves sont présents")
        return

    nom = base[id]

    if nom not in presents:
        presents.append(nom)

    resultat.config(text=f"{nom} est présent.")
    progress_barre.config(value=len(presents)/len(eleves)*100)


root = tk.Tk()
root.geometry("500x300")
root.title("Projet lecteur de cartes")
logo_noel= PhotoImage(file="père_noël.png")
root.iconphoto(True, logo_noel)

label_info = tk.Label(root, text="Veuillez scanner votre carte", font=("Marianne", 16))
label_info.pack(pady=10)

progress_barre = ttk.Progressbar(root,length=100)
progress_barre.pack(pady=10)

entree = tk.Entry(root, font=("Marianne", 14), bg="#CFC1A3")
entree.pack(pady=10)
entree.focus_set()

entree.bind("<Return>", verifier)

resultat = tk.Label(root, text="", font=("Marianne", 14))
resultat.pack(pady=20)

root.mainloop()
