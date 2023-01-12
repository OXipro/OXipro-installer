import tkinter as tk
import tkinter.ttk as ttk
from tqdm import tqdm
import requests
import bs4
import os
import zipfile
import sys
from config import *

# Création de la fenêtre principale
window = tk.Tk()
window.title(windowname)
window.geometry("350x250")
tk.Label(window, text=windowlabletitle, font=('Arial', 30, 'bold')).pack(pady=5)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Création de la variable qui contiendra la valeur sélectionnée dans l'OptionMenu
def get_modpack_list():
    # Envoi de la requête HTTP
    response = requests.get(serveurURL)

    # Vérification que la requête a réussi
    if response.status_code == 200:
        # Parsing du HTML de la réponse
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        dirs = soup.find_all("a")
        link_texts = [link.string for link in dirs]
        print("get_modpack_list result is")
        print(link_texts)
        return link_texts


def installmods():
    # verifie si il ya un modpack selectioné
    if modpack_var.get() == "Veuillez sélectionner un modpack":
        print("no modpack selected")
        return "error no modpack"
    # on definis l'url de l'archive des mods
    modsarchiveurl = serveurURL + "" + modpack_var.get().replace(" ", "%20") + "archive.zip"
    # on créer le dossier de l'installateur
    os.system("mkdir temp")
    os.makedirs(os.path.expanduser('~') + "\\AppData\\Roaming\\.oxinstaller\\", exist_ok=True)
    os.makedirs(os.path.expanduser('~') + "\\AppData\\Roaming\\.oxinstaller\\" + modpack_var.get().replace(" ",
                                                                                                           "_") + "\\",
                exist_ok=True)
    # on definis le path dextraction de l'archive
    extract_path = os.path.expanduser('~') + "\\AppData\\Roaming\\.oxinstaller\\" + modpack_var.get().replace(" ",
                                                                                                              "_") + "\\"
    response = requests.head(modsarchiveurl)
    file_size = int(response.headers.get("Content-Length"))
    # Crée un popup avec une barre de progression
    popup = tk.Toplevel()
    ttk.Label(popup, text="Téléchargement de l'archive").pack()
    progress_bar = ttk.Progressbar(popup, orient="horizontal", length=200, mode="determinate")
    progress_bar["maximum"] = file_size
    progress_bar.pack()

    # Envoie une requête GET pour télécharger le fichier
    response = requests.get(modsarchiveurl, stream=True)
    # Utilise tqdm pour mettre à jour la barre de progression
    with open("./temp/archive.zip", "wb") as f:
        for chunk in tqdm(response.iter_content(chunk_size=1024), total=file_size // 1024, unit="KB"):
            f.write(chunk)
            progress_bar["value"] = f.tell()
            progress_bar.update()
    popup.destroy()
    popup2 = tk.Toplevel()
    progress_bar2 = ttk.Progressbar(popup2, orient="horizontal", length=200, mode="determinate")
    progress_bar2["maximum"] = 100
    progress_bar2.pack()

    # Ouvre le fichier zip
    with zipfile.ZipFile("./temp/archive.zip", "r") as zip_ref:
        # Récupère la liste des fichiers contenus dans le fichier zip
        file_list = zip_ref.infolist()

        # Utilise tqdm pour mettre à jour la barre de progression
        for file in tqdm(file_list, total=len(file_list), unit="fichiers"):
            # Extrait le fichier courant
            zip_ref.extract(file, path=extract_path)
            # Met à jour la valeur de la barre de progression
            progress_bar2["value"] = (file_list.index(file) + 1) / len(file_list) * 100
            progress_bar2.update()
    popup2.destroy()


# Créer le texte "Modpack to install"
tk.Label(window, text='Modpack a Installer', font=('Arial', 12)).pack(pady=2)
modpack_list = get_modpack_list()
modpack_var = tk.StringVar(window)
modpack_var.set("Veuillez sélectionner un modpack")
option_menu = tk.OptionMenu(window, modpack_var, *modpack_list)
option_menu.pack()


def installforge():
    # verifie si il ya un modpack selectioné
    if modpack_var.get() == "Veuillez sélectionner un modpack":
        print("no modpack selected")
        return "error no modpack"
    # on cré un dossier de temp
    os.system("mkdir temp")
    # détermine l'url de forge
    forgeurl = serveurURL + "" + modpack_var.get().replace(" ", "%20") + "forge.jar"
    print(forgeurl)
    # determine l'url de ForgeCLI
    forgecliurl = serveurURL + "" + modpack_var.get().replace(" ", "%20") + "forgecli.jar"
    # Crée un popup avec une barre de progression
    popup = tk.Toplevel()
    tk.Label(popup, text="téléchargement de forge").pack()
    progress_bar = ttk.Progressbar(popup, orient="horizontal", length=200, mode="determinate")
    progress_bar["maximum"] = 100
    progress_bar.pack()

    # Télécharge le premier fichier
    response = requests.get(forgeurl, stream=True)
    file_size = int(response.headers.get("Content-Length"))
    with open("./temp/forge.jar", "wb") as f:
        for chunk in tqdm(response.iter_content(chunk_size=1024), total=file_size // 1024, unit="KB"):
            f.write(chunk)
            progress_bar["value"] = (f.tell() / file_size) * 50
            progress_bar.update()

    # Télécharge le second fichier
    response = requests.get(forgecliurl, stream=True)
    file_size = int(response.headers.get("Content-Length"))
    with open("./temp/forgecli.jar", "wb") as f:
        for chunk in tqdm(response.iter_content(chunk_size=1024), total=file_size // 1024, unit="KB"):
            f.write(chunk)
            progress_bar["value"] = 50 + (f.tell() / file_size) * 50
            progress_bar.update()
    popup.destroy()
    # on comance l'installation
    print("start install")
    os.system('java -jar ./temp/forgecli.jar --target "%appdata%/.minecraft" --installer ./temp/forge.jar')


def updatemodpack():
    # verifie si il ya un modpack selectioné
    if modpack_var.get() == "Veuillez sélectionner un modpack":
        print("no modpack selected")
        return "error no modpack"
    # on definis l'url de l'archive des mods
    modsarchiveurl = serveurURL + "" + modpack_var.get().replace(" ", "%20") + "archive.zip"
    # on créer le dossier de l'installateur
    os.system("mkdir temp")
    os.makedirs(os.path.expanduser('~') + "\\AppData\\Roaming\\.oxinstaller\\", exist_ok=True)
    os.makedirs(os.path.expanduser('~') + "\\AppData\\Roaming\\.oxinstaller\\" + modpack_var.get().replace(" ",
                                                                                                           "_") + "\\",
                exist_ok=True)
    # on definis le path dextraction de l'archive
    extract_path = os.path.expanduser('~') + "\\AppData\\Roaming\\.oxinstaller\\" + modpack_var.get().replace(" ",
                                                                                                              "_") + "\\"
    response = requests.head(modsarchiveurl)
    file_size = int(response.headers.get("Content-Length"))
    # Crée un popup avec une barre de progression
    popup = tk.Toplevel()
    ttk.Label(popup, text="Téléchargement de l'archive").pack()
    progress_bar = ttk.Progressbar(popup, orient="horizontal", length=200, mode="determinate")
    progress_bar["maximum"] = file_size
    progress_bar.pack()

    # Envoie une requête GET pour télécharger le fichier
    response = requests.get(modsarchiveurl, stream=True)

    # Utilise tqdm pour mettre à jour la barre de progression
    with open("./temp/archive.zip", "wb") as f:
        for chunk in tqdm(response.iter_content(chunk_size=1024), total=file_size // 1024, unit="KB"):
            f.write(chunk)
            progress_bar["value"] = f.tell()
            progress_bar.update()
    popup.destroy()
    popup2 = tk.Toplevel()
    progress_bar2 = ttk.Progressbar(popup2, orient="horizontal", length=200, mode="determinate")
    progress_bar2["maximum"] = 100
    progress_bar2.pack()

    # Ouvre le fichier zip
    with zipfile.ZipFile("./temp/archive.zip", "r") as zip_ref:
        # Récupère la liste des fichiers contenus dans le fichier zip
        file_list = zip_ref.infolist()

        # Utilise tqdm pour mettre à jour la barre de progression
        for file in tqdm(file_list, total=len(file_list), unit="fichiers"):
            # Extrait le fichier courant
            zip_ref.extract(file, path=extract_path)
            # Met à jour la valeur de la barre de progression
            progress_bar2["value"] = (file_list.index(file) + 1) / len(file_list) * 100
            progress_bar2.update()
    popup2.destroy()


def fullinstall():
    print("launching installforge")
    if installforge() == "error no modpack":
        popup = tk.Toplevel()
        popupfaild = tk.Label(popup, text="Failed to install Forge")
        popupfaild.pack()
        popupbecose = tk.Label(popup, text="Veullez selectionez un modpack")
        popupbecose.pack()
        okbutton = tk.Button(popup, text="Zut alors", command=popup.destroy)
        okbutton.pack()
        print("error")
        os.system("rm -r temp")
        print("temp removed")
    else:
        print("launching installmods")
        if installmods() == "error no modpack":
            popup = tk.Toplevel()
            popupfaild = tk.Label(popup, text="Failed to install mods")
            popupfaild.pack()
            okbutton = tk.Button(popup, text="Zut alors", command=popup.destroy)
            okbutton.pack()
            print("error")
            os.system("rm -r temp")
            print("temp removed")
        else:
            popup = tk.Toplevel()
            popupfaild = tk.Label(popup, text="Successfully installed")
            popupfaild.pack()
            okbutton = tk.Button(popup, text="Super", command=popup.destroy)
            okbutton.pack()
            os.system("rm -r temp")
            print("temp removed")

    return


def updatemodpackmanager():
    if updatemodpack() == "error no modpack":
        popup = tk.Toplevel()
        popupfaild = tk.Label(popup, text="Failed to update modpack")
        popupfaild.pack()
        popupbecose = tk.Label(popup, text="Veullez selectionez un modpack")
        popupbecose.pack()
        okbutton = tk.Button(popup, text="Zut alors", command=popup.destroy)
        okbutton.pack()
        print("error no modpack")
        os.system("rm -r temp")
        print("temp removed")
    else:
        popup = tk.Toplevel()
        popup.title("Modpack successfully updated")
        popupfaild = tk.Label(popup, text="Modpack successfully updated")
        popupfaild.pack()
        okbutton = tk.Button(popup, text="Super", command=popup.destroy)
        okbutton.pack()
        os.system("rm -r temp")
        print("temp removed")
    return


def installforgemanager():
    print("launching installforge")
    if installforge() == "error no modpack":
        popup = tk.Toplevel()
        popupfaild = tk.Label(popup, text="Failed to install Forge")
        popupfaild.pack()
        popupbecose = tk.Label(popup, text="Veullez selectionez un modpack")
        popupbecose.pack()
        okbutton = tk.Button(popup, text="Zut alors", command=popup.destroy)
        okbutton.pack()
        print("error")
        os.system("rm -r temp")
        print("temp removed")
    else:
        popup = tk.Toplevel()
        popupfaild = tk.Label(popup, text="Successfully installed Forge")
        popupfaild.pack()
        okbutton = tk.Button(popup, text="Super", command=popup.destroy)
        okbutton.pack()
        os.system("rm -r temp")
        print("temp removed")
    return


# Crée le Text Options D'installation
tk.Label(window, text="Options d'Installation", font=('Arial', 12)).pack(pady=2)
# Créer le bouton d'installation all
tk.ttk.Button(window, command=fullinstall, text="Full Install (Forge + mods + ...)").pack()
# Crée le Bouton d'update
tk.ttk.Button(window, text="Mise a jour du modpack", command=updatemodpackmanager).pack()
# Crée le bouton d'installation de forge
tk.ttk.Button(window, text="Installer Forge", command=installforgemanager).pack()
# Exécution de l'application
logo = tk.PhotoImage(file=resource_path(relative_path=windowiconame))
window.wm_iconphoto(True, logo)
window.mainloop()
