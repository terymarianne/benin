import os

my_system = os.uname()

machine = "maison"
machine = "dommartin"

lecteur_pdf = ""
repertoire_w = ""

if my_system.sysname == "Linux":
    lecteur_pdf = ""
    repertoire_w = ""
else
    if machine == "maison":
        lecteur_pdf = "c:/Program Files (x86)/Adobe/Reader 11.0/Reader/AcroRd32.exe"
        repertoire_w = "c:/benin"
    if machine == "dommartin":
        lecteur_pdf = "c:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe"
        repertoire_w = "c:/benin"
        
parametres = {"don":"c:/benin/data",
              "pdf": lecteur_pdf,
              "der":"2/3/2016",
              "bdd":"c:/benin/data/BD_benin",
              "sca":"chemin vers le scanner",
              "cmt":"0",
              "pho":"c:/benin/carte_pdf/photos",
              "imp":"c:/Program Files (x86)/Adobe/Reader 11.0/Reader/AcroRd32.exe",
              "car":"c:/benin/carte_pdf",
}

os.path.join(login, 'apogee')