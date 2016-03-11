import platform
import local_parametre

my_system = platform.uname()

lecteur_pdf = ""
repertoire_w = ""
scanner = ""

if my_system.system == "Linux":
    lecteur_pdf = ""
    repertoire_w = "/home/tery/Documents/PROG/benin/benin"
else:
    if machine == "maison":
        lecteur_pdf = "c:/Program Files (x86)/Adobe/Reader 11.0/Reader/AcroRd32.exe"
        repertoire_w = "c:/benin"
    if machine == "dommartin":
        lecteur_pdf = "c:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe"
        repertoire_w = "c:/benin"
        scanner = ""
        
parametres = { "rep": repertoire_w,
               "don": repertoire_w + "/DATA",
               "bdd": repertoire_w + "/DATA/BD_benin",
               "par": repertoire_w + "/DATA/parametre.txt",
               "car": repertoire_w + "/carte_pdf",
               "pho": repertoire_w + "/carte_pdf/photos",
               "pdf": lecteur_pdf,
               "sca": scanner,
               "der":"2/3/2016",
               "cmt":"0",
}
#os.path.join(login, 'apogee')