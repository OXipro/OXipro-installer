# OXipro's installer <a href="https://github.com/OXipro/OXipro-installer"><img alt="CodeHub" src="https://raw.githubusercontent.com/OXipro/OXipro-installer/master/installer.png" width="%"></a>
OXipro's installer is a customizable minecraft modpack installer the project was inspired by [Canine's Modpack Installer](https://github.com/TheGamerCanine/GamerDog-Modpack/) but with many improvements as modpack updating and light installer file size
# How it works
its operation does not really look like [Canine's Modpack Installer](https://github.com/TheGamerCanine/GamerDog-Modpack/).

The installer retrieves the list of folders in a web server with the "dierectory listing" and then it stores the server's container and lists it in the drop-down menu.
when we press "install forge" a function is called this function downloads minecraft forge and forge cli which are stored in webserver "http://ipoftheserver/modpackname/forge.jar" and
"http://ipoftheserver/modpackname/forgecli.jar"
then it displays the download percentage in a progress bar and then it launches the installation with java in silent mode "java -jar ./temp/forgecli.jar --target "%appdata%/.minecraft" --installer . /temp/forge.jar"
and it's almost the same for the other functions.
For function
install modpack/update modpack
the function will launch the download of the archive from the web server "http://ipoftheserver/modpackname/archive.zip" and displays the progress of the download in a progress bar and then the function will extract the archive in "%appdata%/.oxiprosinstaller/"
# Customize installer
to make your own version of the installer you must follow these steps
1. __Download the [__lasted archive in the project relases page__](https://github.com/OXipro/OXipro-installer/releases/)__
2. **Download** [**Auto-py-to-exe**](https://github.com/brentvollebregt/auto-py-to-exe/archive/refs/heads/master.zip)
3. **Extract auto py to exe in a folder**
4. **Extract the archive of oxipro's installer in another folder**
5. **Modify the config.py in the installer folder :**
```
#config.py file :

serveurURL = "http://oxproject.fr.nf:8000/" <-- set the url of the web server whit directory listing
# name of installer window
windowname = "OXipro launcher" <-- set the name of installer window
# text of first text lable in GUI
windowlabletitle = "OXipro's launcher"
# name of the installer window icon default is oxiprosinstaller.png
windowiconame = "installer.png"
```