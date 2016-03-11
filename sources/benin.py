#__author__ = 'tery'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import parametres
from parametres import parametres

from tkinter import *
from PIL import Image, ImageTk 
import ipdb
import os
import subprocess
import time
import shutil
from os import getcwd


import generation_carte
from basedonnees import *
import utilities
#import pygame

#largeur bouton
spab = 15
spal = 5
spaf = 5
os.chdir(parametres["rep"])

class champ():
    def __init__(self,fenetre,cle,val,max):
        self.parent = fenetre
        self.V = StringVar(value=val)
        self.V.trace_variable("w",OnValidate)
        self.E = Entry(self.parent,textvariable=self.V)
        self.L = Label(self.parent,text=cle)
        self.Max = max
        self.Verreur = StringVar(value="")
        self.erreur = Label(self.parent,textvariable=self.Verreur)
    def aff_ligne(self,c,l):
        self.L.grid(column=c,row=l)
        self.E.grid(column=c+1,row=l)
        self.erreur.grid(column=c+2,row=l)
    def aff_colonne(self,c,l):
        self.L.grid(column=c,row=l)
        self.E.grid(column=c,row=l+1)
        self.erreur.grid(column=c,row=l+2)
    def update(self,text):
        self.V.set(text)
    def message_erreur(self,text):
        self.Verreur.set(text)

class Cadre(Frame):
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, bg = "dim gray",  **kwargs)
        self.parent = fenetre

class Search(Frame):
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, height=40, bg="slate gray",  **kwargs) #bg="red",
        self.parent = fenetre
        label = Label(self, text="Numéro de carte",width=spab)
        label.pack(side="left",padx=spal,pady=spal)
        self.V_search = StringVar()
        E_search = Entry(self,textvariable=self.V_search)
        E_search.pack(side="left",padx=spal,pady=spal)
        bouton_cliquer = Button(self, text="Rechercher",width=spab, command=self.rechercher)
        bouton_cliquer.pack(side="right",padx=spal,pady=spal)
    def rechercher(self):
        r = self.parent.parent.BD.search(self.V_search.get())
        if not r :
            self.parent.parent.erreur.affiche("la carte {} n'existe pas".format(self.V_search.get()))
            self.parent.parent.formulaire.update_data(None)
        else :
            #print(r)
            self.parent.parent.formulaire.update_data(r)

class Commandes(Frame):
    def __init__(self, fenetre, **kwargs):
        self.parent = fenetre
        Frame.__init__(self, fenetre, width=50,  **kwargs) #bg="green",
        self.bouton_quitter = Button(self, text="Quitter", fg="red", width=spab, command=self.quit)
        self.bouton_quitter.pack(side="bottom",padx=spal,pady=spal)
        self.B_print = Button(self, text="Imprimer", width=spab, command=self.imprimer)
        self.B_print.pack(side="bottom",padx=spal,pady=spal)
        self.B_save = Button(self, text="Enregistrer", width=spab, command=self.save)
        self.B_save.pack(side="bottom",padx=spal,pady=spal)

    def imprimer(self):
        personne = self.save()
        if personne :
            nom_fichier_pdf = "{}/{}.pdf".format(parametres["car"],personne.data.num_carte)
            generation_carte.generation(nom_fichier_pdf,personne)
            exe = parametres["pdf"]
            subprocess.Popen([exe,nom_fichier_pdf])

        else:
            self.parent.parent.erreur.affiche("le formulaire n'est pas complet")

    def personne(self):
        formulaire = self.parent.parent.formulaire
        date = formulaire.V_dateEmi.get().split("/")
        date1 = utilities.datetime.date(int(date[2]),int(date[1]),int(date[0]))
        date = formulaire.V_dateExp.get().split("/")
        date2 = utilities.datetime.date(int(date[2]),int(date[1]),int(date[0]))
        identitee = c_identitee(formulaire.V_nomu.get(),formulaire.V_prenoms.get())
        personne = c_personne(formulaire.V_numcarte.get(),identitee,formulaire.V_nomn.get(),formulaire.V_date_n.get(),
                        formulaire.V_lieu_n.get(),[formulaire.V_nomP1.get(),formulaire.V_nomP2.get()],
                        [formulaire.V_adresse.get(), formulaire.V_adresse2.get()], formulaire.V_profession.get(),formulaire.V_taille.get(),
                        formulaire.V_teint.get(),formulaire.V_cheveux.get(),formulaire.V_yeux.get(),formulaire.V_signe.get(),
                        [formulaire.V_extrait1.get(),formulaire.V_extrait2.get(),formulaire.V_extrait3.get()],
                        date1,date2,self.parent.parent.photo.image)
        if personne.data.nom_naissance == "" :
            return None
        else :
            return personne

    def save(self):
        personne = self.personne()
        self.parent.parent.photo.update("{}/photo.png".format(parametres["don"]))
        if personne :
            self.parent.parent.compteur += self.parent.parent.BD.ajout(personne)
            self.parent.parent.formulaire.update_data()
        else:
            print("attention pas de sauvegarde possible")
        return personne

class Photo(Frame):
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, **kwargs) #bg="blue",
        # Création de nos widgets
        self.parent = fenetre
        print("{}/photo.png".format(parametres["don"]))
        self.image = "{}/photo.png".format(parametres["don"])
        im =  Image.open(self.image)
        x=im.size[0]
        y=im.size[1]
        if x>y :
            y = int((y*90)/x)
            x = 90
        else :
            x = int((x*90)/y)
            y = 90
        im = im.resize((x,y),3)
        self.canvas = Canvas(self, width=100,height=100)
        self.canvas.image= ImageTk.PhotoImage(im)
        self.canvas.create_image(50, 50, image=self.canvas.image)
        self.canvas.pack(padx=spal,pady=spal)

        self.bouton_scanner = Button(self, text="Scanner",width=spab, fg="blue",
                                command=self.scanner)
        self.bouton_scanner.pack(padx=5,pady=5)

    def scanner(self):
        #self.image = recadrage("data/images.jpeg")
        #self.image.save("data/imagesR.jpeg")
        self.image = "{}/{}.jpeg".format(parametres["pho"],
                        self.parent.parent.formulaire.V_numcarte.get())
        try :
            os.remove("c:/test/testR.jpeg")
        except :
            pass
        try :
            os.remove("c:/test/test.jpg")
        except :
            pass
        try :
            retour = os.popen(parametres["rep"] + "/sources/scanconvert.bat")
            print("*" * 5 , retour.read())
            retour.close()
        except :
            pass
        try :
                    shutil.move("c:/test/testR.jpeg", self.image)
        except :
                    self.parent.parent.erreur.affiche("le scanner n'est pas branché")
                    return
        im = Image.open(self.image)
        x=im.size[0]
        y=im.size[1]
        if x>y :
            y = int((y*90)/x)
            x = 90
        else :
            x = int((x*90)/y)
            y = 90
        im = im.resize((x,y),3)
        self.canvas.delete(self.canvas.image)
        self.canvas.image= ImageTk.PhotoImage(im)
        self.canvas.create_image(50, 50, image=self.canvas.image)
        self.canvas.update()


    def update(self,adresse):
        self.image = adresse
        im = Image.open(self.image)
        x=im.size[0]
        y=im.size[1]
        if x>y :
            y = int((y*90)/x)
            x = 90
        else :
            x = int((x*90)/y)
            y = 90
        im = im.resize((x,y),3)
        self.canvas.delete(self.canvas.image)
        self.canvas.image= ImageTk.PhotoImage(im)
        self.canvas.create_image(50, 50, image=self.canvas.image)
        self.canvas.update()

class MessageERR(Frame):
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre,bg="dim gray",**kwargs) #bg="purple",
        self.message = Label(self, text="message d'erreur",fg="red")
    def affiche(self,txt):
        self.message["text"] = txt
        self.message.pack(side="right")
    def efface(self):
        self.message.forget()

def OnValidate(*args):
    if len(app.formulaire.V_nomn.get()) > 12 :
        app.formulaire.V_nomn.set(app.formulaire.V_nomn.get()[:-1])
    if len(app.formulaire.V_nomu.get()) > 12 :
        app.formulaire.V_nomu.set(app.formulaire.V_nomu.get()[:-1])
    if len(app.formulaire.V_prenoms.get()) > 28 :
        app.formulaire.V_prenoms.set(app.formulaire.V_prenoms.get()[:-1])
    if len(app.formulaire.V_adresse.get()) > 45 :
        app.formulaire.V_adresse.set(app.formulaire.V_adresse.get()[:-1])
    if len(app.formulaire.V_adresse2.get()) > 45 :
        app.formulaire.V_adresse2.set(app.formulaire.V_adresse2.get()[:-1])
    if len(app.formulaire.V_date_n.get()) > 10 :
        app.formulaire.V_date_n.set(app.formulaire.V_date_n.get()[:-1])
    if len(app.formulaire.V_lieu_n.get()) > 30 :
        app.formulaire.V_lieu_n.set(app.formulaire.V_lieu_n.get()[:-1])
    if len(app.formulaire.V_nomP1.get()) > 30 :
        app.formulaire.V_nomP1.set(app.formulaire.V_nomP1.get()[:-1])
    if len(app.formulaire.V_nomP2.get()) > 30 :
        app.formulaire.V_nomP2.set(app.formulaire.V_nomP2.get()[:-1])
    if len(app.formulaire.V_extrait1.get()) > 35 :
        app.formulaire.V_extrait1.set(app.formulaire.V_extrait1.get()[:-1])
    if len(app.formulaire.V_extrait2.get()) > 35 :
        app.formulaire.V_extrait2.set(app.formulaire.V_extrait2.get()[:-1])
    if len(app.formulaire.V_extrait3.get()) > 35 :
        app.formulaire.V_extrait3.set(app.formulaire.V_extrait3.get()[:-1])
    if len(app.formulaire.V_profession.get()) > 15 :
        app.formulaire.V_profession.set(app.formulaire.V_profession.get()[:-1])
    if len(app.formulaire.V_taille.get()) > 8 :
        app.formulaire.V_taille.set(app.formulaire.V_taille.get()[:-1])
    if len(app.formulaire.V_teint.get()) > 9 :
        app.formulaire.V_teint.set(app.formulaire.V_teint.get()[:-1])
    if len(app.formulaire.V_cheveux.get()) > 9 :
        app.formulaire.V_cheveux.set(app.formulaire.V_cheveux.get()[:-1])
    if len(app.formulaire.V_yeux.get()) > 9 :
        app.formulaire.V_yeux.set(app.formulaire.V_yeux.get()[:-1])
    if len(app.formulaire.V_signe.get()) > 25 :
        app.formulaire.V_signe.set(app.formulaire.V_signe.get()[:-1])


class Formulaire(Frame):
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre,**kwargs) #bg="yellow",
        self.parent = fenetre
        F_carte = LabelFrame(self,text="Carte consulaire")
        L_numcarte = Label(F_carte, text="Carte n°")
        L_dateEmi = Label(F_carte, text="Date d'émission")
        L_dateExp = Label(F_carte, text="Date d'expiration")
        d = utilities.datetime.date.today()
        nomcarte = "LY{}-{:02}{:02}{}".format(str(d.year)[2:], d.month, d.day, self.parent.parent.compteur)
        self.V_numcarte = StringVar(value=nomcarte)
        E_numcarte = Entry(F_carte,textvariable=self.V_numcarte)
        self.V_dateEmi = StringVar(value=utilities.date_to_str(d))
        E_dateEmi = Entry(F_carte,textvariable=self.V_dateEmi)
        dexp = dexp = utilities.date_expiration(d)
        self.V_dateExp = StringVar(value=utilities.date_to_str(dexp))
        E_dateExp = Entry(F_carte,textvariable=self.V_dateExp)
        L_numcarte.grid(column=1,row=0,sticky='W',padx=spal)
        E_numcarte.grid(column=1,row=1,sticky='EW',padx=spal,pady=spal)
        L_dateEmi.grid(column=2,row=0,sticky='W',padx=spal)
        E_dateEmi.grid(column=2,row=1,sticky='EW',padx=spal,pady=spal)
        L_dateExp.grid(column=3,row=0,sticky='W',padx=spal)
        E_dateExp.grid(column=3,row=1,sticky='EW',padx=spal,pady=spal)

        F_ID = LabelFrame(self,text="Identitée")
        L_nomn = Label(F_ID, text="Nom de naissance")
        L_nomu = Label(F_ID, text="Nom usuel")
        L_prenoms = Label(F_ID, text="Prénoms")
        L_adresse = Label(F_ID, text="Adresse")
        self.V_nomn = StringVar(value="")
        self.V_nomn.trace_variable("w",OnValidate)
        E_nomn = Entry(F_ID,textvariable=self.V_nomn)
        self.V_nomu = StringVar(value="")
        self.V_nomu.trace_variable("w",OnValidate)
        E_nomu = Entry(F_ID,textvariable=self.V_nomu)
        self.V_prenoms = StringVar(value="")
        self.V_prenoms.trace_variable("w",OnValidate)
        E_prenoms = Entry(F_ID,textvariable=self.V_prenoms)
        self.V_adresse = StringVar(value="")
        self.V_adresse.trace_variable("w",OnValidate)
        E_adresse = Entry(F_ID,textvariable=self.V_adresse)
        self.V_adresse2 = StringVar(value="")
        self.V_adresse2.trace_variable("w",OnValidate)
        E_adresse2 = Entry(F_ID,textvariable=self.V_adresse2)
        L_nomn.grid(column=1,row=2,sticky='w',padx=spal)
        L_nomu.grid(column=2,row=2,sticky='w',padx=spal)
        L_prenoms.grid(column=3,row=2,sticky='w',padx=spal)
        E_nomn.grid(column=1,row=3,sticky='EW',padx=spal,pady=spal)
        E_nomu.grid(column=2,row=3,sticky='EW',padx=spal,pady=spal)
        E_prenoms.grid(column=3,row=3,sticky='EW',padx=spal,pady=spal)
        L_adresse.grid(column=1,row=10,sticky='w',padx=spal)
        E_adresse.grid(column=1,row=11,sticky='EW',padx=spal,pady=spal,columnspan=3)
        E_adresse2.grid(column=1,row=12,sticky='EW',padx=spal,pady=spal,columnspan=3)

        F_naissance = LabelFrame(self,text="Naissance")
        L_date_n = Label(F_naissance, text="Date de naissance")
        L_lieu_n = Label(F_naissance, text="Lieu de naissance")
        L_de = Label(F_naissance, text="De")
        L_et_de = Label(F_naissance, text="Et de")
        L_nomP1 = Label(F_naissance, text="Nom Prénom")
        L_nomP2 = Label(F_naissance, text="Nom Prénom")
        self.V_date_n = StringVar(value="")
        self.V_date_n.trace_variable("w",OnValidate)
        E_date_n = Entry(F_naissance,textvariable=self.V_date_n)
        self.V_lieu_n = StringVar(value="")
        self.V_lieu_n.trace_variable("w",OnValidate)
        E_lieu_n = Entry(F_naissance,textvariable=self.V_lieu_n)
        self.V_nomP1 = StringVar(value="")
        self.V_nomP1.trace_variable("w",OnValidate)
        E_nomP1 = Entry(F_naissance,textvariable=self.V_nomP1)
        self.V_nomP2 = StringVar(value="")
        self.V_nomP2.trace_variable("w",OnValidate)
        E_nomP2 = Entry(F_naissance,textvariable=self.V_nomP2)
        L_Extrait = Label(F_naissance, text = "Extrait")
        self.V_extrait1 = StringVar(value="")
        self.V_extrait1.trace_variable("w",OnValidate)
        E_extrait1 = Entry(F_naissance,textvariable=self.V_extrait1)
        self.V_extrait2 = StringVar(value="")
        self.V_extrait2.trace_variable("w",OnValidate)
        E_extrait2 = Entry(F_naissance,textvariable=self.V_extrait2)
        self.V_extrait3 = StringVar(value="")
        self.V_extrait3.trace_variable("w",OnValidate)
        E_extrait3 = Entry(F_naissance,textvariable=self.V_extrait3)

        L_date_n.grid(column=1,row=4,sticky='w',padx=spal)
        L_lieu_n.grid(column=2,row=4,sticky='w',padx=spal)
        L_Extrait.grid(column=3,row=4,sticky='w',padx=spal,pady=spal)
        E_date_n.grid(column=1,row=5,sticky='EW',padx=spal,pady=spal)
        E_lieu_n.grid(column=2,row=5,columnspan=2,sticky='EW',padx=spal,pady=spal)
        E_extrait1.grid(column=3,row=5,sticky='EW',padx=spal)
        L_de.grid(column=1,row=6,sticky='E',rowspan=2)
        L_nomP1.grid(column=2,row=6,sticky='w',padx=spal)
        E_extrait2.grid(column=3,row=6,sticky='EW',padx=spal,pady=spal)
        E_nomP1.grid(column=2,row=7,sticky='EW',padx=spal,pady=spal)
        E_extrait3.grid(column=3,row=7,sticky='EW',padx=spal,pady=spal)
        L_et_de.grid(column=1,row=8,sticky='E',rowspan=2)
        L_nomP2.grid(column=2,row=8,sticky='w',padx=spal)
        E_nomP2.grid(column=2,row=9,sticky='EW',padx=spal,pady=spal)

        F_info = LabelFrame(self,text="Informations")
        L_profession = Label(F_info, text="Profession")
        L_taille = Label(F_info, text="Taille")
        L_teint = Label(F_info, text="Teint")
        L_cheveux = Label(F_info, text="Cheveux")
        L_yeux = Label(F_info, text="Yeux")
        L_signe = Label(F_info, text="Signes particuliers")
        self.V_profession = StringVar()
        self.V_profession.trace_variable("w",OnValidate)
        E_profession = Entry(F_info,textvariable=self.V_profession)
        self.V_taille = StringVar(value="")
        self.V_taille.trace_variable("w",OnValidate)
        E_taille = Entry(F_info,textvariable=self.V_taille)
        self.V_teint = StringVar(value="")
        self.V_teint.trace_variable("w",OnValidate)
        E_teint = Entry(F_info,textvariable=self.V_teint)
        self.V_cheveux = StringVar(value="")
        self.V_cheveux.trace_variable("w",OnValidate)
        E_cheveux = Entry(F_info,textvariable=self.V_cheveux)
        self.V_yeux = StringVar(value="")
        self.V_yeux.trace_variable("w",OnValidate)
        E_yeux = Entry(F_info,textvariable=self.V_yeux)
        self.V_signe = StringVar(value="")
        self.V_signe.trace_variable("w",OnValidate)
        E_signe = Entry(F_info,textvariable=self.V_signe)
        L_profession.grid(column=1,row=12,sticky='w',padx=spal)
        E_profession.grid(column=1,row=13,sticky='EW',padx=spal,pady=spal,columnspan=2)
        L_taille.grid(column=1,row=14,sticky='w',padx=spal)
        L_teint.grid(column=2,row=14,sticky='w',padx=spal)
        E_taille.grid(column=1,row=15,sticky='EW',padx=spal,pady=spal)
        E_teint.grid(column=2,row=15,sticky='EW',padx=spal,pady=spal)
        L_cheveux.grid(column=1,row=16,sticky='w',padx=spal)
        L_yeux.grid(column=2,row=16,sticky='w',padx=spal)
        E_cheveux.grid(column=1,row=17,sticky='EW',padx=spal,pady=spal)
        E_yeux.grid(column=2,row=17,sticky='EW',padx=spal,pady=spal)
        L_signe.grid(column=1,row=18,sticky='w',padx=spal)
        E_signe.grid(column=1,row=19,sticky='EW',padx=spal,pady=spal,columnspan=2)

        F_carte.grid(column=0,row=0,sticky='W',padx=spaf,pady=spaf)
        F_ID.grid(column=0,row=1,sticky='W',padx=spaf,pady=spaf)
        F_naissance.grid(column=0,row=3,sticky='W',padx=spaf,pady=spaf)
        F_info.grid(column=0,row=4,sticky='W',padx=spaf,pady=spaf)


    def update_data(self,personne=None):
        if personne == None:
            self.parent.parent.photo.update("{}/photo.png".format(parametres["don"]))
            d = utilities.datetime.date.today()
            nomcarte = "LY{}-{:02}{:02}{}".format(str(d.year)[2:], d.month, d.day, self.parent.parent.compteur)
            self.V_numcarte.set(nomcarte)
            dexp = utilities.date_expiration(d)
            self.V_dateEmi.set(str(d.day)+"/"+str(d.month)+"/"+str(d.year))
            self.V_dateExp.set(str(dexp.day)+"/"+str(dexp.month)+"/"+str(dexp.year))
            self.V_nomu.set("")
            self.V_nomn.set("")
            self.V_prenoms.set("")
            self.V_adresse.set("")
            self.V_adresse2.set("")
            self.V_date_n.set("")
            self.V_lieu_n.set("")
            self.V_nomP1.set("")
            self.V_nomP2.set("")
            self.V_extrait1.set("")
            self.V_extrait2.set("")
            self.V_extrait3.set("")
            self.V_profession.set("")
            self.V_taille.set("")
            self.V_teint.set("")
            self.V_cheveux.set("")
            self.V_yeux.set("")
            self.V_signe.set("")
        else:
            self.V_numcarte.set(personne.data.num_carte)
            d = personne.data.date_emission
            self.V_dateEmi.set(str(d.day)+"/"+str(d.month)+"/"+str(d.year))
            d = personne.data.date_expiration
            self.V_dateExp.set(str(d.day)+"/"+str(d.month)+"/"+str(d.year))
            self.V_nomu.set(personne.data.identitee.nom)
            self.V_nomn.set(personne.data.nom_naissance)
            self.V_prenoms.set(personne.data.identitee.prenom)
            self.V_adresse.set(personne.data.adresse[0])
            self.V_adresse2.set(personne.data.adresse[1])
            self.V_date_n.set(personne.data.date_naissance)
            self.V_lieu_n.set(personne.data.lieu_naissance)
            self.V_nomP1.set(personne.data.parents[0])
            self.V_nomP2.set(personne.data.parents[1])
            self.V_extrait1.set(personne.extrait[0])
            self.V_extrait2.set(personne.extrait[1])
            self.V_extrait3.set(personne.extrait[2])
            self.V_profession.set(personne.profession)
            self.V_taille.set(personne.taille)
            self.V_teint.set(personne.teint)
            self.V_cheveux.set(personne.cheveux)
            self.V_yeux.set(personne.yeux)
            self.V_signe.set(personne.signes)
            self.parent.parent.photo.update(personne.photo)

        #self.parent.parent.update()
        #self.parent.update()
class Parametre(Frame):
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width = 300,height = 200,**kwargs) #bg="black",
        self.parent = fenetre
        repertoire = Label(self, text="Répertoire d'instalation du programme")
        repertoire.grid(column=0,row=1,padx=spal,pady=spal)
        self.V_repertoire = StringVar(value= parametres["rep"])
        E_repertoire = Entry(self,width=70,textvariable=self.V_repertoire)
        E_repertoire.grid(column=1,row=1,padx=spal,pady=spal)
        pdf = Label(self, text="Visualiseur PDF")
        pdf.grid(column=0,row=2,padx=spal,pady=spal)
        self.V_pdf = StringVar(value=parametres["pdf"])
        E_pdf = Entry(self,width=70,textvariable=self.V_pdf)
        E_pdf.grid(column=1,row=2,padx=spal,pady=spal)
        bouton = Button(self, text="Enregistrer",width=spab, command=self.save)
        bouton.grid(column = 3,row = 2,padx=spal,pady=spal)

    def save(self):
        parametres["rep"] = self.V_repertoire.get()
        parametres["pdf"] = self.V_pdf.get()

    def editer(self):
        self.parent.efface()
        self.pack(side="left",padx=spal,pady=spal)

    def afficher(self):
        self.parent.efface()
        self.pack(padx=spal,pady=spal)

class Extraction(Frame):
    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre,width = 300,height = 200,**kwargs) #bg="black",
        self.parent = fenetre
        self.de = champ(self,"de","JJ/MM/AAAA",10)
        self.a =  champ(self,"a","JJ/MM/AAAA",10)
        date = utilities.datetime.date.today()
        nom_fichier_extraction = "extraction_{}{}{}".format(date.year,date.month,date.day)
        self.nom_extraction = champ(self,"nom du fichier",nom_fichier_extraction,15)
        self.de.aff_ligne(0,0)
        self.a.aff_ligne(0,1)
        self.nom_extraction.aff_ligne(0,2)
        bouton = Button(self, text="Extraire",width=spab, command=self.extraire)
        bouton.grid(column = 3,row = 3,padx=spal,pady=spal)

    def extraire(self):
        print(self.de.V.get())
        print(self.a.V.get())
        print(self.nom_extraction.V.get())
        self.de.message_erreur("mauvais format")
        de = self.de.V.get()
        de = utilities.str_to_date(de)
        a = self.a.V.get()
        a = utilities.str_to_date(a)
        print(de," ",a)
        self.parent.BD.extract(de,a,self.nom_extraction.V.get())
        
    #def editer(self):
        #self.parent.efface()
        #self.pack(side="left",padx=spal,pady=spal)

    def afficher(self):
        self.parent.efface()
        self.pack(padx=spal,pady=spal)


class simpleapp_tk(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.charge()
        #self.attributes('-fullscreen', 1)
        self.cadre = Cadre(self)
        self.initialize()
        self.menu()

    def initialize(self):
        #self.image = "data/photo.png"
        recherche = Search(self.cadre)
        recherche.pack(side="top",fill="x",padx=5,pady=5)
        self.formulaire = Formulaire(self.cadre)
        self.formulaire.pack(side="left",padx=5,pady=5)
        commande = Commandes(self.cadre)
        commande.pack(side="bottom",fill="x",padx=5,pady=5)
        self.photo = Photo(self.cadre)
        self.photo.pack(side="top",fill="x",padx=5,pady=5)
        self.erreur = MessageERR(self.cadre)
        self.erreur.pack(side="right",fill="both",padx=5,pady=5)
        self.cadre.pack()
        self.parametres = Parametre(self)
        self.extraction = Extraction(self)

    def affiche(self):
        self.efface()
        self.cadre.pack()

    def charge(self):
        date = utilities.datetime.datetime.today()
        self.compteur = 0

        sauvegarde = parametres["bdd"][:-8]
        sauvegarde += "sauvegarde/BD_benin.{}{:02}{:02}_{:02}{:02}".format(date.year, date.month, date.day,
                                                                           date.hour, date.minute)
        try:
            shutil.copy(parametres["bdd"],sauvegarde)
        except:
            print("Sauvegarde impossible, la base de données n'existe pas")

        self.BD = BDC(parametres["bdd"])
        print("on vérifie le chargement")
        print(self.BD)
        
        try :
            date_compare = "{:02}/{:02}/{}".format(date.day,date.month,str(date.year)[2:])
            print(date_compare)
            liste = list(self.BD.bdc.keys())
            liste.sort()
            compteur = liste[len(liste)-1]
            date_der = "{}/{}/{}".format(compteur[7:9], compteur[5:7], compteur[2:4])
            print(compteur, " => ", compteur[9:], " - ", date_der)

            if date_compare == date_der:
                self.compteur = int(compteur[9:]) + 1
        except :
            pass

    def save(self):
#        date = utilities.datetime.date.today()
#        date_compare = utilities.date_to_str(date)
#        self.Dico_parametres["der"] = date_compare
#        print("avant de faire save, on a date : {}, compteur : {}".format(date_compare,self.compteur))
#        self.Dico_parametres["cmt"] = str(self.compteur)
        self.BD.save(parametres["bdd"])
#        s = "{"
#        for el in self.Dico_parametres:
#            s += '"{}":"{}",\n'.format(el,self.Dico_parametres[el])
#        s +="}"
#        with open(parametres["par"],'w',encoding="utf8") as f:
#            f.write(s)
  
    def efface(self):
        self.formulaire.update_data(None)
        self.cadre.forget()
        self.parametres.forget()
        self.extraction.forget()

    def menu(self):
        self.menubar = Menu(self)
        menu1 = Menu(self.menubar, tearoff=0)
        menu1.add_command(label="Nouvelle carte", command=self.affiche)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=self.quit)
        self.menubar.add_cascade(label="Fichier", menu=menu1)

        menu2 = Menu(self.menubar, tearoff=0)
        menu2.add_command(label="Vers excel", command=self.extraction.afficher)
        self.menubar.add_cascade(label="Extraction", menu=menu2)

        menu3 = Menu(self.menubar, tearoff=0)
        menu3.add_command(label="Editer", command=self.parametres.editer)
        menu3.add_command(label="Afficher", command=self.parametres.afficher)
        menu3.add_command(label="A propos")#, command=self.parametres.afficher)
        self.menubar.add_cascade(label="Paramètres", menu=menu3)
        self.config(menu=self.menubar)

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Consulat du BENIN : Edition de carte consulaire')
    app.mainloop()
    app.save()
