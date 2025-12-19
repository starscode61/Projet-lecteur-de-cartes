import json
import tkinter as tk
from tkinter import PhotoImage, LEFT, RIGHT
import tkinter.ttk as ttk

with open("eleves.json", "r", encoding="utf-8") as f:
    base = json.load(f)

carte_prof = None
eleves = {}
super_dico_pour_changer_les_lettres_en_chiffres = {
    "&":"1",
    "é":"2",
    '"':"3",
    "'":"4",
    "(":"5",
    "-":"6",
    "è":"7",
    "_":"8",
    "ç":"9",
    "à":"0",
}

for identifiant, nom in base.items():
    if nom == "Professeur":
        carte_prof = identifiant
    else:
        eleves[identifiant] = nom

presents = []

def ajouter_nom(id,event):
    nom = entree.get()
    with open("eleves.json", "r") as f:
        fichier = f.readlines()
    while fichier[-1] == "\n":
        fichier.pop(-1)
    fichier.insert(-3,'    "'+id+'": "'+nom+'",\n')
    print(fichier)
    with open("eleves.json", "w") as f:
        f.writelines(fichier)
    
    label_info.config(text="Veuillez scanner votre carte")
    entree.unbind("<Return>")
    entree.bind("<Return>", verifier)
    entree.delete(0, tk.END)

def rentrer_nom():
    id = entree.get()
    entree.delete(0, tk.END)

    label_info.config(text="ajouter le nom")
    entree.unbind("<Return>")
    entree.bind("<Return>", lambda event: ajouter_nom(id,event))
    

def new_id():
    resultat.config(text="Identifiant inconnu voulez vous l'ajouter ?")
    button_box = tk.Frame(root)
    
    button_oui = tk.Button(button_box,text="oui",command=lambda: (button_box.destroy(),resultat.config(text=""),rentrer_nom()))
    button_oui.pack(side=LEFT, padx=10)
    button_non = tk.Button(button_box,text="non",command=lambda: (button_box.destroy(),resultat.config(text=""),entree.delete(0, tk.END)))
    button_non.pack(side=RIGHT, padx=10)

    button_box.pack(pady=10)



def verifier(event):
    id = ""
    try :
        int(entree.get())
        id = entree.get()
    except:
        for l in entree.get():
            id += super_dico_pour_changer_les_lettres_en_chiffres[l]

    if id not in base:
        new_id()
        return
    
    
    entree.delete(0, tk.END)
    entree.focus_set()

    if id == carte_prof:
        absents = []
        for nom in eleves.values():
            if nom not in presents:
                absents.append(nom)

        if len(absents) > 1:
            resultat.config(text="il y a "+ str(len(absents)) +" élèves absents soit "+str(round(len(absents)/len(eleves)*100,1))+"% de la classe :\n" + "\n".join(absents))
        elif len(absents) == 1:
            resultat.config(text="il y a 1 élève absent soit "+str(round(len(absents)/len(eleves)*100,1))+"% de la classe :\n" + "\n".join(absents))
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

progress_barre = ttk.Progressbar(root,length=350)
progress_barre.pack(pady=10)

entree = tk.Entry(root, font=("Marianne", 14))
entree.pack(pady=10)
entree.focus_set()

entree.bind("<Return>", verifier)

resultat = tk.Label(root, text="", font=("Marianne", 14))
resultat.pack(pady=20)

root.mainloop()

