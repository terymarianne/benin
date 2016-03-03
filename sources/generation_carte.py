__author__ = 'tery'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import basedonnees
import utilities

class carte_consulaire:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        from os import getcwd
        print(getcwd())
        self.fond = "c:/benin/data/fond.jpg"
        self.tampon_blanc = "c:/benin/data/tampon_blanc.png"
        self.tampon_rouge = "c:/benin/data/tampon_rouge.png"
        self.FontSizeLabel = 6
        self.FontSizeData = 8
        self.COL = [0.2,2.6,5.3,8.5,13.4,15.3]
        self.LIG = 0.4
        self.PRL = 5.7
        self.col_photo = 10.3

    def impress(self,pdf,c,l,txt):
        pdf.drawString((self.x + self.COL[c])*cm, (self.y + (self.PRL - l*self.LIG))*cm, txt)

    def initialise(self,pdf,personne):
        pdf.drawImage(self.fond,self.x*cm,self.y*cm,preserveAspectRatio=True)

        pdf.drawImage("c:/benin/data/logo.png",(self.x + 8)*cm, (self.y + 0.9)*cm,height = 120,preserveAspectRatio=True,mask="auto")
        #text drapeau et titres
        pdf.setFillColorRGB(255,255,255)
        pdf.setFontSize(6)
        pdf.drawString((self.x + self.col_photo)*cm, (self.y + 5.4)*cm, 'AMBASSADE EN FRANCE')
        pdf.setFillColorRGB(0,0,0)
        pdf.setFontSize(12)
        pdf.drawString((self.x + 13.4)*cm, (self.y + 6.5)*cm, 'REPUBLIQUE DU BENIN')
        pdf.setFillColorRGB(0.0,0.525490,0.317647)
        pdf.setFontSize(10)
        pdf.drawString((self.x + 13.4)*cm, (self.y + 5.9)*cm, 'CARTE D\'IDENTITE CONSULAIRE')
        pdf.setFillColorRGB(0,0,0)
        pdf.setFontSize(10)
        pdf.drawString((self.x + 0.2)*cm, (self.y + 6.5)*cm, 'REPUBLIQUE DU BENIN')
        pdf.setFontSize(8)
        pdf.drawString((self.x + 0.6)*cm, (self.y + 6.1)*cm, 'CONSULAT DE LYON (France)')

        ##text sous photo
        pdf.setFillColorRGB(0,0,0)
        textobject = pdf.beginText()
        textobject.setTextOrigin((self.x + self.col_photo - 0.1)*cm, (self.y + 2)*cm)
        textobject.setFont("Times-Roman", 5.5)
        textobject.setCharSpace(0.1)
        textobject.setWordSpace(1)
        textobject.textLine("L'Ambassade de la République du")
        textobject.setCharSpace(0)
        textobject.setWordSpace(0)
        textobject.textLine("BENIN à Paris certifie que le titulaire")
        textobject.setCharSpace(0)
        textobject.setWordSpace(1)
        textobject.textLine("de la présente carte est immatriculé")
        textobject.setCharSpace(0.05)
        textobject.setWordSpace(0)
        textobject.textLine("auprès d'ELLE et prie les services de")
        textobject.setCharSpace(0.1)
        textobject.setWordSpace(0)
        textobject.textLine("police de bien vouloir lui faciliter la")
        textobject.setCharSpace(0.09)
        textobject.setWordSpace(0)
        textobject.textLine("libre circulation, lui accorder aide et")
        textobject.textLine("protection en cas de besoin.")
        pdf.drawText(textobject)

        pdf.drawImage(personne.photo, (self.x + self.col_photo)*cm, (self.y + 2.3)*cm, width=2.6*cm, height = 2.6*cm, preserveAspectRatio=True)

        #grille de gauche
        pdf.setFontSize(self.FontSizeLabel)
        self.impress(pdf,0,1,"Profession/Occupation")
        self.impress(pdf,0,2, "Taille/Height")
        self.impress(pdf,0,3, "Teint/Carnation")
        self.impress(pdf,0,4, "Cheveux/Colour of hair")
        self.impress(pdf,0,5, "Yeux/Colour of eyes")
        self.impress(pdf,0,7, "Signes particuliers/Distinctives marks")

        self.impress(pdf,2,1, "Date d'émission/Date of issue")
        self.impress(pdf,2,2, "Date d'expiration/Date of expiry")
        self.impress(pdf,2,7, "Signature de l'autorité/Authority's signature")

        self.impress(pdf,4,2, 'Carte n°/Carte no')
        self.impress(pdf,4,3, 'Nom/Surname')
        self.impress(pdf,4,4, 'Prénom(s)/Given names')
        self.impress(pdf,4,6, 'Date et lieu de naissance/Date and place of birth')
        self.impress(pdf,4,8, 'De/of')
        self.impress(pdf,4,9, 'Et de/And of')
        self.impress(pdf,4,10, 'Domicile/Residence')
        self.impress(pdf,4,12, 'Signature du titulaire/')
        self.impress(pdf,4,12.5, "Holder's signature")

        DEC = 1.8
        pdf.setFontSize(9)
        pdf.drawString((self.x + self.COL[1])*cm, (self.y + (self.PRL - 1*self.LIG))*cm, personne.profession)
        pdf.drawString((self.x + self.COL[1])*cm, (self.y + (self.PRL - 2*self.LIG))*cm, personne.taille)
        pdf.drawString((self.x + self.COL[1])*cm, (self.y + (self.PRL - 3*self.LIG))*cm, personne.teint)
        pdf.drawString((self.x + self.COL[1])*cm, (self.y + (self.PRL - 4*self.LIG))*cm, personne.cheveux)
        pdf.drawString((self.x + self.COL[1])*cm, (self.y + (self.PRL - 5*self.LIG))*cm, personne.yeux)
        pdf.drawString((self.x - DEC + self.COL[1])*cm, (self.y + (self.PRL - 8*self.LIG))*cm, personne.signes)

        pdf.setFontSize(7)

        date_Emission = utilities.date_to_str(personne.data.date_emission)
        date_Expiration = utilities.date_to_str(personne.data.date_expiration)
        pdf.drawString((self.x + self.COL[3])*cm, (self.y + (self.PRL - 1*self.LIG))*cm, date_Emission)
        pdf.drawString((self.x + self.COL[3])*cm, (self.y + (self.PRL - 2*self.LIG))*cm, date_Expiration)
        pdf.setFillColorRGB(0,0,50)
        pdf.setFontSize(7)
        pdf.drawString((self.x + self.COL[2]+0.1)*cm, (self.y + (self.PRL - 4*self.LIG))*cm, personne.extrait[0])
        pdf.drawString((self.x + self.COL[2]+0.1)*cm, (self.y + (self.PRL - 5*self.LIG))*cm, personne.extrait[1])
        pdf.drawString((self.x + self.COL[2]+0.1)*cm, (self.y + (self.PRL - 6*self.LIG))*cm, personne.extrait[2])
        pdf.setFillColorRGB(0,0,0)
        pdf.setFontSize(11)
        pdf.drawString((self.x + self.COL[2] + 0.5 )*cm, (self.y + (self.PRL - 9*self.LIG))*cm, 'Pierre GAZAGNE')
        pdf.drawString((self.x + self.COL[2] + 0.5 )*cm, (self.y + (self.PRL - 10*self.LIG))*cm, 'Consul à LYON')

        pdf.setFontSize(9)
        pdf.drawString((self.x + self.COL[5])*cm, (self.y + (self.PRL - 2*self.LIG))*cm, personne.data.num_carte)
        fin_nom = ""
        if personne.data.identitee.nom != "":
            fin_nom = " ép. {}".format(personne.data.identitee.nom)
        nomu_nome = "{}{}".format(personne.data.nom_naissance,fin_nom)
        pdf.drawString((self.x + self.COL[5])*cm, (self.y + (self.PRL - 3*self.LIG))*cm, nomu_nome)
        pdf.drawString((self.x + self.COL[5])*cm, (self.y + (self.PRL - 5*self.LIG))*cm, personne.data.identitee.prenom)
        pdf.drawString((self.x + self.COL[5] - DEC)*cm, (self.y + (self.PRL - 7*self.LIG))*cm, personne.data.date_naissance)
        pdf.drawString((self.x + self.COL[5])*cm, (self.y + (self.PRL - 7*self.LIG))*cm, personne.data.lieu_naissance)
        pdf.drawString((self.x + self.COL[5])*cm, (self.y + (self.PRL - 8*self.LIG))*cm, personne.data.parents[0])
        pdf.drawString((self.x + self.COL[5])*cm, (self.y + (self.PRL - 9*self.LIG))*cm, personne.data.parents[1])
        pdf.setFontSize(8)
        pdf.drawString((self.x + self.COL[5] - DEC)*cm, (self.y + (self.PRL - 11*self.LIG))*cm, personne.data.adresse)

        #tampon
        pdf.drawImage(self.tampon_blanc,(self.x + 11.5)*cm, (self.y + 0.95)*cm, width = 1.9*cm, preserveAspectRatio=True,mask="auto")
        pdf.drawImage(self.tampon_rouge,(self.x + self.COL[2] + 2.5)*cm, (self.y - 0.3)*cm, width = 1.9*cm, preserveAspectRatio=True,mask="auto")

def generation(carte,personne):
    try :
        os.remove(carte)
        sleep(3)
    except :
        pass
    pdf = canvas.Canvas(carte)
    carte = carte_consulaire(0.3,22)
    carte.initialise(pdf,personne)
    carte2 = carte_consulaire(0.3,14.8)
    carte2.initialise(pdf,personne)
    pdf.setDash([1,1])
    pdf.setStrokeColor("black")
    pdf.line(0.3*cm,22*cm,20.7*cm,22*cm)
    pdf.setDash([1,0])
    pdf.save()

if __name__ == "__main__":
    os.chdir("c:\\benin\\")
    identitee = basedonnees.c_identitee("W w w w w w w","W W W w w w w w w w w w w w w")
    dateA = utilities.datetime.date(2015,11,11)
    dateB = utilities.datetime.date(2020,11,11)
    personne = basedonnees.c_personne("LY15-031299", identitee, "W w w w w w w", "21/02/1981", "W W W W w w w w w w w w w w w w",
                                   ["W W w w w w w w w w w","Pouzol Chantal 16"], "A W W W W w w w w w w w w w w w w w w w w w w", "Métier 9",
                                   "Orthophoniste", "blanche", "noir", "marron", "A B C D E F G H A B C D E F G",
                                   ["extrait","W w w w w w w w w w w w w w w w w ",""], dateA, dateB,"c:/benin/data/photo.png")
    generation("test.pdf",personne)

