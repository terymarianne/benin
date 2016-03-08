__author__ = 'tery'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parametres
from parametres import parametres
import pickle
import os
import xlrd
from xlwt import Workbook

import ipdb
import utilities

class c_identitee:
    def __init__(self,nom,prenom):
        self.nom = nom
        self.prenom = prenom
    def excel(self):
        return ""
    def __str__(self):
        return self.nom , self.prenom

class c_donnees_xls:
    def __init__(self, num_carte, identitee, nom_naissance, date_naissance, lieu_naissance, parents, adresse,
              date_emission, date_expiration):
        self.identitee = identitee
        self.num_carte = num_carte
        self.nom_naissance = nom_naissance
        self.date_naissance = date_naissance
        self.lieu_naissance = lieu_naissance
        self.parents = parents
        self.adresse = adresse
        self.date_emission = date_emission
        self.date_expiration = date_expiration

    def excel(self):
        return ""

    def __str__(self):
        demi = utilities.date_to_str(self.date_emission)
        dexp = utilities.date_to_str(self.date_expiration)
        aff = "{:5} {:20} {:10} {:10}".format(self.num_carte,self.nom_naissance,demi,dexp)
        return aff


class c_personne:
    def __init__(self, num_carte, identitee, nom_naissance, date_naissance, lieu_naissance,
              parents, adresse, profession, taille, teint, cheveux, yeux, signes, extrait, date_emission, date_expiration,photo):
        self.data = c_donnees_xls(num_carte,identitee,nom_naissance,date_naissance,lieu_naissance,parents,adresse,
                                  date_emission,date_expiration)
        self.photo = photo
        self.profession, self.taille, self.teint = profession, taille, teint
        self.cheveux, self.yeux, self.signes, self.extrait = cheveux, yeux, signes, extrait

    def excel(self):
        return self.data.excel()

    def __str__(self):
        return self.data.__str__() + " " + self.photo


class BDC():
    def __init__(self,nom_fichier_BD):
        try:
            f = open(nom_fichier_BD,'rb')
            mon_pickler = pickle.Unpickler(f)
            self.bdc = mon_pickler.load()
            print("la base de donnée {} est chargée".format(nom_fichier_BD))
            f.close()
        except:
            print("la base de donnée {} n'existe pas".format(nom_fichier_BD))
            self.bdc = {}

    def save(self,nom_fichier_BD):
        print("on sauve la base dans : ", nom_fichier_BD)
        with open(nom_fichier_BD,'wb') as f:
            mon_pickler = pickle.Pickler(f)
            mon_pickler.dump(self.bdc)

    def traduction(self):
        for e in self.bdc :
            if isinstance(self.bdc[e].data.adresse , str):
                self.bdc[e].data.adresse = [ self.bdc[e].data.adresse, "" ]

    def import_xls(self,nom_fichier_xls):
        try :
            wb = xlrd.open_workbook(nom_fichier_xls)
        except :
            print("le fichier {} n'existe pas".format(nom_fichier))
            return None
        nom_feuille = wb.sheet_names()
        print(nom_feuille)
        sh = wb.sheet_by_name(nom_feuille[0])
        print(sh.row_values(0))
        for rownum in range(1,sh.nrows,1):
            d1 = utilities.datetime.date(1900,1,1)
            delta1 = utilities.datetime.timedelta(days=sh.row_values(rownum)[2]-2)
            delta2 = utilities.datetime.timedelta(days=sh.row_values(rownum)[3]-2)
            print(sh.row_values(rownum)[0],sh.row_values(rownum)[1],d1+delta1,d1+delta2)
            identitee = c_identitee("nomU","prenom")
            demi = d1 + delta1
            dexp = d1 + delta2
            titi = c_personne(sh.row_values(rownum)[0], identitee,sh.row_values(rownum)[1],
                     "date_naissance"," lieu_naissance", ["parent1", "parent2"],
                     ["adresse",""], "profession", "taille",
                     "teint", "cheveux", "yeux", "signes",
                     ["extrait1","extrait2","extrait3"],
                     demi, dexp,"data/images.jpeg")
            self.ajout(titi)

    def search(self,num_carte):
        if num_carte in self.bdc :
            return self.bdc[num_carte]
        else:
            return None

    def ajout(self,personne):
        retour = 1
        if personne.data.num_carte in self.bdc :
            retour =0
        print("on ajoute/met à jour : ",personne.data.num_carte, personne.data.nom_naissance)
        self.bdc[personne.data.num_carte] = personne
        return retour

    def extract(self,de, a,nom_fichier_xls):
        book = Workbook()
        feuil1 = book.add_sheet('feuille 1')
        liste_extract = []
        feuil1.write(0,0,'num')
        feuil1.write(0,1,'nom')
        feuil1.write(0,2,'date émission')
        feuil1.write(0,3,'date expiration')

        cmpt_L = 1
        for elment in self.bdc:
            print(elment, self.bdc[elment].data.date_expiration, self.bdc[elment].data.date_expiration)
            if self.bdc[elment].data.date_expiration > de and self.bdc[elment].data.date_expiration < a :
                ligne = feuil1.row(cmpt_L)
                ligne.write(0,self.bdc[elment].data.num_carte)
                ligne.write(1,self.bdc[elment].data.nom_naissance)
                date_emission = utilities.date_to_str(self.bdc[elment].data.date_emission)
                ligne.write(2,date_emission)
                date_expiration = utilities.date_to_str(self.bdc[elment].data.date_expiration)
                ligne.write(3,date_expiration)
                liste_extract.append(self.bdc[elment])
                cmpt_L += 1
        book.save('\extraction_xls\{}.xls'.format(nom_fichier_xls))
        return liste_extract

    def __str__(self):
        aff = "{:5} {:20} {:10} {:10}\n".format("num_carte","nom","date emi","date exp")
        for elment in self.bdc:
            aff += self.bdc[elment].__str__() + "\n"
        return aff

def afficheMenu(menu):
    """ affiche l'entête du menu"""
    c="."
    print(55*c,end='')
    s="\n{C} {a:^51} {C}".format(a="MENU",C=c)
    print(s)
    print(55*c,end='')
    print("\n")

    """affiche le menu"""
    for e in menu:
        s="{a:^10}{b:<20}".format(a=e,b=menu[e])
        print(s)
    print("\n \t que voulez-vous faire ?")

def menu():
    """ création du menu"""
    menu = {'a':'ajouter/modifier un élément'}
    menu['s']='chercher un élément'
    menu['p']='affiche la base'
    menu['S']='sauvegarder la base'
    menu['q']='quitter'
    menu['e']='extraire'
    menu['d']="suppression d'un élément"
    menu['i']="import d'un fichier"
    return menu

if __name__ == "__main__":
    os.chdir(parametres["rep"])
    NOM_FICHIER = parametres["bdd"]
    instruction = 'a'
    """création de l'annuaire"""
    baseDD = {}
    baseDD = BDC(NOM_FICHIER)
    #baseDD.traduction()
    #baseDD.save(NOM_FICHIER + "_traduit")

    """création du menu"""
    menu = menu()
    while instruction != 'q':
        # os.system('clear')
        """affichage du menu"""
        print(baseDD)
        afficheMenu(menu)
        """récupération de l'instruction"""
        instruction = input()

        """on execute ce qu'il faut à partir de l'instruction donnée"""
        if instruction == 'p':
            print(baseDD)
            continue
        elif instruction == 'a':
            identitee = c_identitee("nomU","prenom")
            parent1 = c_identitee("nomU","prenoms")
            parent2 = c_identitee("nomU","prenoms")
            demi = utilities.datetime.date.today()
            dexp = utilities.datetime.date(demi.year+7,demi.month,demi.day)
            titi = c_personne("LY1", identitee, "aaaa", "date_naissance"," lieu_naissance", [parent1, parent2],
                     ["adresse","adresse2"], "profession", "taille", "teint", "cheveux", "yeux", "signes", "extrait",
                     demi, dexp,"photo")
            baseDD.ajout(titi)
            continue
        elif instruction == 'S':
            baseDD.save(NOM_FICHIER)
        elif instruction == 's':
            r = baseDD.search("LY3")
            if r :
                print(r,r.data.identitee.prenom)
            else:
                print("il n'est pas dans la base")
                continue
        elif instruction =='e' :
            datem = utilities.datetime.date(2017,1,1)
            dateM = utilities.datetime.date(2021,1,1)
            L = baseDD.extract(datem,dateM)
            print("extraction")
            for el in L:
                print(el)
        elif instruction == "d":
            num = input()
            if num in baseDD.bdc:
                del baseDD.bdc[num]
            else:
                print( num, " n'est pas dans la base")
        elif instruction == "i":
            #nom_fichier = input()
            nom_fichier_xls = "\data\test_import.xls"
            baseDD.import_xls(nom_fichier_xls)

    baseDD.save(NOM_FICHIER)
