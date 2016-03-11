import local_parametre

#import platform
#my_system = platform.uname()

#lecteur_pdf = ""
#repertoire_w = ""
#scanner = ""

#if my_system.system == "Linux":
    #lecteur_pdf = "evince"
    #repertoire_w = "/home/tery/Documents/PROG/benin/benin"
#else:
    #if machine == "maison":
        #lecteur_pdf = "c:/Program Files (x86)/Adobe/Reader 11.0/Reader/AcroRd32.exe"
        #repertoire_w = "c:/benin"
        #lecteur_pdf = "evince"
    #if machine == "dommartin":
        #lecteur_pdf = "c:/Program Files (x86)/Adobe/Acrobat Reader DC/Reader/AcroRd32.exe"
        #repertoire_w = "c:/benin"
        #scanner = ""
        
parametres = { "rep": local_parametre.repertoire_w,
               "don": local_parametre.repertoire_w + "/DATA",
               "bdd": local_parametre.repertoire_w + "/DATA/BD_benin",
               "par": local_parametre.repertoire_w + "/DATA/parametre.txt",
               "car": local_parametre.repertoire_w + "/carte_pdf",
               "pho": local_parametre.repertoire_w + "/carte_pdf/photos",
               "pdf": local_parametre.lecteur_pdf,
}
#os.path.join(login, 'apogee')
