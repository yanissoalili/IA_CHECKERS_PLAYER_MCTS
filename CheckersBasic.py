import random
from copy import deepcopy,copy
from random import randint,choice

#Classe etat de partie contient le plan du jeu
class Etat:
    def __init__(self,etat=None):
        self.table=list()
        self.pionsJ1=list()
        self.mouvObgJ1=list()
        self.pionsJ2=list()
        self.mouvObgJ2 = list()

        if(etat != None):
            temp=etat.copierEtat()
            self.table=temp.table
            self.pionsJ1 = temp.pionsJ1
            self.mouvObgJ1 = temp.mouvObgJ1
            self.pionsJ2 = temp.pionsJ2
            self.mouvObgJ2 = temp.mouvObgJ2

        if (etat==None):
            self.initTable()

    #InitTable avec les positions initiales des pions ( 0 -> LIBRE ; 1 -> JOUEUR1(Humain) ; 1 -> JOUEUR2(IA)
    def initTable(self):
        self.table = [[0,2,0,2,0,2,0,2],[2,0,2,0,2,0,2,0],[0,2,0,2,0,2,0,2],
                      [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                      [1,0,1,0,1,0,1,0],[0,1,0,1,0,1,0,1],[1,0,1,0,1,0,1,0]]
        self.initPositions()

    def initPositions(self):
        #init les positions initiales des pions
        for i,row in enumerate(self.table):
            for j,element in enumerate(row):
                if element == 1 : self.pionsJ1.append(Pion(i, j, 1))
                if element == 2 : self.pionsJ2.append(Pion(i, j, 2))
                if element == 5 : self.pionsJ1.append(Pion(i, j, 1,True))
                if element == 6 : self.pionsJ2.append(Pion(i, j, 2,True))

    def copierEtat(self):
        copie = Etat()
        copie.pionsJ1 = list(self.pionsJ1)
        copie.pionsJ2 = list(self.pionsJ2)
        copie.mouvObgJ1 = list(self.mouvObgJ1)
        copie.mouvObgJ2 = list(self.mouvObgJ2)
        for i,row in enumerate(self.table):
            copie.table[i] = self.table[i][:]
        return copie

    #Afficher les mouvements possibles/obligatoires pour un joueur ou un pion précis
    def afficherMouvPossibles(self,pion=None,tour=None):
        if (pion==None):
            if(tour==1):
                print("Joueur 1", end=" ")
                for i in self.pionsJ1:
                    print("[ " + str(i.ligne) + " , " + str(i.colonne) + " ] ---> ", end=" ")
                    for j in i.mouvPossibles:
                        print("( " + str(j.ligne) + " , " + str(j.colonne) + " )", end=",")
                    print(" , Obligés : ", end=" ")
                    for k in i.mouvOblig:
                        print("( " + str(k.ligne) + " , " + str(k.colonne) + " )", end=",")
                    print()
            else:
                print("Joueur 2", end=" ")
                for i in self.pionsJ2:
                    print("[ " + str(i.ligne) + " , " + str(i.colonne) + " ] ---> ", end=" ")
                    for j in i.mouvPossibles:
                        print("( " + str(j.ligne) + " , " + str(j.colonne) + " )", end=",")
                    print(" , Obligés : ", end=" ")
                    for k in i.mouvOblig:
                        print("( " + str(k.ligne) + " , " + str(k.colonne) + " )", end=",")
                    print()
        else :
            print("Joueur"+str(pion.joueur),end=" ")
            print("[ " + str(pion.ligne) + " , " + str(pion.colonne) + " ] ---> ", end=" ")
            for j in pion.mouvPossibles:
                print("( " + str(pion.ligne) + " , " + str(pion.colonne) + " )", end=",")
            print(" , Obligés : ",end=" ")
            for k in pion.mouvOblig:
                print("( " + str(pion.ligne) + " , " + str(pion.colonne) + " )", end=",")
            print()

    #Recuperer l'instance d'un pion a partir de sa position sur le jeu
    def getIdByPosition(self,joueur,i,j):
        if joueur==1:
            for element in self.pionsJ1:
                if ((element.ligne==i) and (element.colonne==j)):
                    return element
            return None
        else :
            for element in self.pionsJ2:
                if ((element.ligne==i) and (element.colonne==j)):
                    return element
            return None

    #Méthode pour afficher l'etat de la partie(Afficher la matrice du jeu
    def afficherTable(self):
        print("    0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 ")
        for i,row in enumerate (self.table):
            print("   ___ ___ ___ ___ ___ ___ ___ ___")
            print(str(i) +" ", end="| ")
            for j,element in enumerate(row):

                if element == 0 : print(" ",end=" | ")
                if element == 1:
                    p=self.getIdByPosition(1,i,j)
                    if p.dame==False: print("X", end=" | ")
                    else : print("DX", end=" | ")
                if element == 2:
                    p = self.getIdByPosition(2, i, j)
                    if p.dame == False:
                        print("O", end=" | ")
                    else:
                        print("DO", end=" | ")
            print()

    #s'arreter si aucun pion ne peut avancer càd blocage ( PAS DE DAMES POUR LE MOMENT ) >>> EGALITE
    def testerFinPartie(self):
        x=0
        for pion in (self.pionsJ1):
            if((len(pion.mouvOblig) != 0) or (len(pion.mouvPossibles) != 0)):
                x=1
                break
        if (x==0):return True
        x=0
        for pion in (self.pionsJ2):
            if((len(pion.mouvOblig) != 0) or (len(pion.mouvPossibles) != 0)):
                x=1
        if (x == 0): return True
        return False

    #Retourne le resultat de la partie selon les règles du jeu : 0>Egalité , 1>VictoireJ1 , 2>VictoireJ2
    def testerResultat(self):
        if (self.testerFinPartie()==True):
            return 0 # EGALITE
        else :
            if len(self.pionsJ1) == 0 : return 2
            else :
                if len(self.pionsJ2) == 0 : return 1
                else :
                    return 3 # La partie continue

    #Effectue un mouvement d'un joueur sur l'état du jeu(verification faite au préalable)
    def effectuerMouvement(self,pion,mouvement):
        #Mettre à jour table
        self.table[pion.ligne][pion.colonne]=0
        self.table[mouvement.ligne][mouvement.colonne]=pion.joueur

        #self.afficherMouvPossibles(pion)
        #print()

        pion.ligne=deepcopy(mouvement.ligne)
        pion.colonne=deepcopy(mouvement.colonne)

        ##AFFECTER LES DAMES
        if ((pion.joueur==1)and(pion.ligne==0)):
            pion.dame=True
        if ((pion.joueur==2)and(pion.ligne==7)):
            pion.dame=True




        if(len(mouvement.pionManges)>0):
            for element in mouvement.pionManges:
                self.table[element.ligne][element.colonne] = 0
                try:
                    if element.joueur == 1:
                        self.pionsJ1.remove(element)
                    else:
                        self.pionsJ2.remove(element)
                except:
                    print
                    "This is an error message!*****************************************************************************"

        self.mouvObgJ1.clear()
        self.mouvObgJ2.clear()

    #Mettre a jour table et les pions apres un mouvement effectué
    def miseAJourTable(self):
        for pion in (self.pionsJ1 + self.pionsJ2):
            pion.mouvOblig.clear()
            pion.mouvPossibles.clear()
            pion.testerMouvPossibles(self)

    # Effectue un tour du jeu pour l'humain PIONS A 1
    def jouerHumain(self):
        if (len(self.mouvObgJ1) >= 0):
            print("Veuillez choisir le mouvement obligatoire")
        else:
            print("Veuillez choisir votre mouvment")
        while True:
            while True:
                print("Saisir la ligne !")
                i = int(input())
                if (i in range(0, 8)): break
                print("Index de ligne incorrect ! Reessayer !")
            while True:
                print("Saisir colonne")
                j = int(input())
                if (j in range(0, 8)): break
                print("Index de colonne incorrect ! Reessayer !")
            if self.table[i][j]==1: break
            else : print ("Choix du pion incorrect")

        print("Choix du mouvement")
        while True:
            while True:
                print("Saisir la ligne !")
                x = int(input())
                if (x in range(0, 8)): break
                print("Index de ligne incorrect ! Reessayer !")
            while True:
                print("Saisir colonne")
                y = int(input())
                if (y in range(0, 8)): break
                print("Index de colonne incorrect ! Reessayer !")
            pionChoisi=self.getIdByPosition(1,i,j)
            for mouvement in (pionChoisi.mouvOblig+pionChoisi.mouvPossibles):
                if ((mouvement.ligne == x) and (mouvement.colonne == y)):
                        self.effectuerMouvement(pionChoisi, mouvement)
                        self.miseAJourTable()
                        return 0
                else:print("Mouvement impossible pour ce pion")

    #

    # Effectue un simulation pour le reste de la partie et retourne le resultat
    def simulationAleatoire(self,tour):
        cpt=0
        resultat=3
        while (True):
            #if (tour == 1):
             #   print("TOUR DE : 2")
              #  self.afficherMouvPossibles(tour=2)
            #else:
             #   print("TOUR DE : 1")
              #  self.afficherMouvPossibles(tour=1)
            #cpt=cpt+1
            #self.afficherTable()
            if (tour == 1):
                # switchTour
                tour=2
                if (len(self.mouvObgJ1) > 0):
                    # Priorité aux mouvements obligatoires
                    index = randint(0, len(self.mouvObgJ1) - 1)
                    self.effectuerMouvement(self.mouvObgJ1[index].pion, self.mouvObgJ1[index].mouvement)
                else :#Choisir un mouvement aléatoire parmi les mouvements non obligatoires
                    while (True):
                        pionAleatoire = choice(self.pionsJ1)
                        if(len(pionAleatoire.mouvPossibles)>0):
                            mouvAleatoire = choice(pionAleatoire.mouvPossibles)
                            #print(
                                #"Mouvement du pion : [" + str(pionAleatoire.ligne) + "," + str(pionAleatoire.colonne) + "] --- > [" + str(
                                    #mouvAleatoire.ligne) + "," + str(mouvAleatoire.colonne) + "]")
                            self.effectuerMouvement(pionAleatoire,mouvAleatoire)
                            break
                        else:
                            if(self.testerFinPartie()):break

            else:#Tour 2
                # switchTour
                tour = 1
                if (len(self.mouvObgJ2)>0):#Priorité aux mouvements obligatoires
                    index = randint(0,len(self.mouvObgJ2)-1)
                    #mouvementAleatoire=self.mouvObgJ2[index]
                    self.effectuerMouvement(self.mouvObgJ2[index].pion,self.mouvObgJ2[index].mouvement)
                else :#Choisir un mouvement aléatoire parmi les mouvements non obligatoires
                    while (True):
                        pionAleatoire = choice(self.pionsJ2)
                        if (len(pionAleatoire.mouvPossibles) > 0):
                            mouvAleatoire = choice(pionAleatoire.mouvPossibles)
                            #print(
                                #"Mouvement du pion : [" + str(pionAleatoire.ligne) + "," + str(
                                    #pionAleatoire.colonne) + "] --- > [" + str(
                                    #mouvAleatoire.ligne) + "," + str(mouvAleatoire.colonne) + "]")
                            self.effectuerMouvement(pionAleatoire,mouvAleatoire)
                            break
                        else:
                            if(self.testerFinPartie()): break
            self.miseAJourTable()

            if(cpt==50):return 0
            #Tester le résultat
            resultat = self.testerResultat()
            if resultat == 0:
                #print ("Egalité")
                return 0
            if resultat == 1:
                #print("Victoire J1")
                return 1
            if resultat == 2:
                #print("Victoire J2")
                return 2

    #Classe qui gére l'alternance des tours ( J1 - J2 )
    def jouer(self,tour):
        resultat=3#Partie en cours
        while (resultat==3):
            if tour == 1 :
                self.jouerHumain()
                tour=2
            else:
                self.jouerIA()
                tour=1
            resultat=self.testerResultat()
            print (resultat)


#Classe qui instancie les mouvements
class Mouvement:#Type : //// Ligne Colonnes : positions finales du mouvement, PionManges : liste des pions adversaires eliminés si ce mouvement est executé
    def __init__(self,i,j):
        self.ligne=i
        self.colonne=j
        self.pionManges=list()

    def copierMouvement(self):
        copie = Mouvement(self.ligne,self.colonne)
        copie.pionManges = list(self.pionManges)
        return copie

#Classe couple(Pion,Mouvment)--> Utilisé pour des raisons de conception uniquement
class Tuple:
    def __init__(self,pion,mouvement):
        self.pion=pion
        self.mouvement=mouvement


#Classe qui instancie chaque pion sur le dammier
class Pion:
    def __init__(self,i,j,joueur,dame=False):
        self.ligne=i
        self.colonne=j
        self.mouvOblig=list()#Liste des mouvements obligés
        self.mouvPossibles=list()#Liste des mouvements possibles
        self.joueur=joueur#Appartenance du pion ( J1 ou J2 )
        self.dame=dame

    def copierPion(self):
        copie = Pion(self.ligne, self.colonne, self.joueur)
        copie.mouvOblig = list(self.mouvOblig)  # Liste des mouvements obligés
        copie.mouvPossibles = list(self.mouvPossibles)  # Liste des mouvements possibles
        copie.dame=self.dame
        return copie

    #Teste si un saut vers la gauche est possible
    def testerSautGauche(self,etat,mouvement=None):
        table=etat.table
        fin=True
        if (mouvement == None):
            i=self.ligne
            j=self.colonne
        else:
            i=mouvement.ligne
            j=mouvement.colonne

        if self.joueur==1:
            if ((i - 2 in range(0,8)) and (j - 2 in range(0,8)) and (table[i - 2][j - 2] == 0)):
                fin = False
                if (mouvement == None):
                    mouvement = Mouvement(i - 2, j - 2)
                else:#Mouvement de plusieurs sauts
                    mouvement.ligne = i - 2
                    mouvement.colonne = j - 2
                temp = etat.getIdByPosition(2, i - 1, j - 1)
                if (temp is not None):

                    mouvement.pionManges.append(temp)
                if ((mouvement.ligne-1 in range(0,8)) and (mouvement.colonne-1 in range(0,8)) and (table[mouvement.ligne-1][mouvement.colonne-1] == 2)):
                    self.testerSautGauche(etat,mouvement)
                else:
                    if ((mouvement.ligne - 1 in range(0, 8)) and (mouvement.colonne + 1 in range(0, 8)) and (
                            table[mouvement.ligne - 1][mouvement.colonne + 1] == 2)):
                        self.testerSautDroit(etat,mouvement)
                    else:#Arreter la boucle iterative
                        fin = True
        else :#Joueur2
            if ((i + 2 in range(0,8)) and (j + 2 in range(0,8)) and (table[i + 2][j + 2] == 0)):
                fin=False
                if (mouvement == None):
                    mouvement = Mouvement(i + 2, j + 2)
                else:#Mouvement de plusieurs sauts
                    mouvement.ligne = i + 2
                    mouvement.colonne = j + 2
                temp = etat.getIdByPosition(1, i + 1, j + 1)
                if (temp is not None):
                    mouvement.pionManges.append(temp)
                if ((mouvement.ligne+1 in range(0,8)) and (mouvement.colonne+1 in range(0,8)) and (table[mouvement.ligne+1][mouvement.colonne+1] == 1)):
                    self.testerSautGauche(etat,mouvement)
                else:
                    if ((mouvement.ligne + 1 in range(0, 8)) and (mouvement.colonne - 1 in range(0, 8)) and (
                            table[mouvement.ligne + 1][mouvement.colonne - 1] == 1)):
                        self.testerSautDroit(etat,mouvement)
                    else:#Arreter la boucle iterative
                        fin = True
        if (fin == True):
            if mouvement is not None:
                self.mouvOblig.append(mouvement)
                tuple = Tuple(self, mouvement)
                if (self.joueur == 1):
                    etat.mouvObgJ1.append(tuple)
                else:
                    etat.mouvObgJ2.append(tuple)

    #Teste si un saut vers la droite est possible
    def testerSautDroit(self, etat,mouvement=None):
        table=etat.table
        fin = True
        if (mouvement == None):
            i = self.ligne
            j = self.colonne
        else:
            i = mouvement.ligne
            j = mouvement.colonne

        if self.joueur == 1:
            if ((i - 2 in range(0, 8)) and (j + 2 in range(0, 8)) and (table[i - 2][j + 2] == 0)):
                fin = False
                if (mouvement == None):
                    mouvement = Mouvement(i - 2, j + 2)
                else:  # Mouvement de plusieurs sauts
                    mouvement.ligne = i - 2
                    mouvement.colonne = j + 2
                temp = etat.getIdByPosition(2, i - 1, j + 1)
                if (temp is not None):
                    mouvement.pionManges.append(temp)
                if ((mouvement.ligne - 1 in range(0, 8)) and (mouvement.colonne - 1 in range(0, 8)) and (
                        table[mouvement.ligne - 1][mouvement.colonne - 1] == 2)):
                    self.testerSautGauche(etat, mouvement)
                else :
                    if ((mouvement.ligne - 1 in range(0, 8)) and (mouvement.colonne + 1 in range(0, 8)) and (
                        table[mouvement.ligne - 1][mouvement.colonne + 1] == 2)):
                        self.testerSautDroit(etat, mouvement)
                    else:#Arreter la boucle iterative
                        fin = True
        else:  # Joueur 2
            if ((i + 2 in range(0, 8)) and (j - 2 in range(0, 8)) and (table[i + 2][j - 2] == 0)):
                fin = False
                if (mouvement == None):
                    mouvement = Mouvement(i + 2, j - 2)
                else:  # Mouvement de plusieurs sauts
                    mouvement.ligne = i + 2
                    mouvement.colonne = j - 2
                temp = etat.getIdByPosition(1, i + 1, j - 1)
                if (temp is not None):
                    mouvement.pionManges.append(temp)#SI LE PION MANGEE EXISTE DEJA NE PAS AJOUTER
                if ((mouvement.ligne + 1 in range(0, 8)) and (mouvement.colonne + 1 in range(0, 8)) and (
                        table[mouvement.ligne + 1][mouvement.colonne + 1] == 1)):
                    self.testerSautGauche(etat, mouvement)
                else:
                    if ((mouvement.ligne + 1 in range(0, 8)) and (mouvement.colonne - 1 in range(0, 8)) and (
                        table[mouvement.ligne + 1][mouvement.colonne - 1] == 1)):
                        self.testerSautDroit(etat, mouvement)
                    else:  # Arreter la boucle iterative
                        fin = True

        if (fin == True):
            if mouvement is not None:
                self.mouvOblig.append(mouvement)
                tuple = Tuple(self, mouvement)
                if (self.joueur == 1):
                    etat.mouvObgJ1.append(tuple)
                else:
                    etat.mouvObgJ2.append(tuple)

    def testerSautDame(self, etat,x,y,orientation,mouvement=None):
        #1 : upleft
        #2 : upright
        #3 : downleft
        #4 : downright
        #print("TESTSAUT (%d , %d) orientation = %d" % (x,y,orientation) )
        table=etat.table
        fin = True
        if (mouvement == None):
            i = self.ligne
            j = self.colonne
        else:
            i = mouvement.ligne
            j = mouvement.colonne

        if self.joueur == 1:
            if orientation == 1:
                if ((x - 1 in range(0, 8)) and (y - 1 in range(0, 8)) and (table[x - 1][y - 1] == 0)):
                    tempLigne=x-1
                    tempColonne=y-1
                    fin = False
            if orientation == 2:
                if ((x - 1 in range(0, 8)) and (y + 1 in range(0, 8)) and (table[x - 1][y + 1] == 0)):
                    tempLigne = x - 1
                    tempColonne = y + 1
                    fin = False
            if orientation == 3:
                if ((x + 1 in range(0, 8)) and (y - 1 in range(0, 8)) and (table[x + 1][y - 1] == 0)):
                    tempLigne = x + 1
                    tempColonne = y - 1
                    fin = False
            if orientation == 4:
                if ((x + 1 in range(0, 8)) and (y + 1 in range(0, 8)) and (table[x + 1][y + 1] == 0)):
                    tempLigne = x + 1
                    tempColonne = y + 1
                    fin = False
            if (fin==False):
                if (mouvement == None):
                    mouvement = Mouvement(tempLigne, tempColonne)
                else:  # Mouvement de plusieurs sauts
                    mouvement.ligne = tempLigne
                    mouvement.colonne = tempColonne
                temp = etat.getIdByPosition(1, x, y)
                if ((temp is not None) and (temp not in self.pionManges)):
                    mouvement.pionManges.append(temp)
                ##
                k=1
                while ((tempLigne - k >=0)and(tempColonne - k >=0) and orientation != 4):
                    if (table[tempLigne - k][tempColonne - k] == 1):break
                    if (table[tempLigne - k][tempColonne - k] == 2):
                        self.testerSautDame(etat,tempLigne - k,tempColonne - k,1,mouvement)
                        break
                k = 1
                while ((tempLigne - k >= 0) and (tempColonne + k <= 7) and orientation != 3):
                    if (table[tempLigne - k][tempColonne - k] == 1): break
                    if (table[tempLigne - k][tempColonne + k] == 2):
                        self.testerSautDame(etat, tempLigne - k, tempColonne + k, 2, mouvement)
                        break
                k = 1
                while ((tempLigne + k <= 7) and (tempColonne - k >= 0) and orientation != 2):
                    if (table[tempLigne - k][tempColonne - k] == 1): break
                    if (table[tempLigne + k][tempColonne - k] == 2):
                        self.testerSautDame(etat, tempLigne - k, tempColonne - k, 3, mouvement)
                        break
                k = 1
                while ((tempLigne + k <= 7) and (tempColonne + k <= 7)and orientation != 1):
                    if (table[tempLigne - k][tempColonne - k] == 1): break
                    if (table[tempLigne + k][tempColonne + k] == 2):
                        self.testerSautDame(etat, tempLigne + k, tempColonne + k, 4, mouvement)
                        break
        else:  # Joueur 2
            if orientation == 1:

                if ((x - 1 in range(0, 8)) and (y - 1 in range(0, 8)) and (table[x - 1][y - 1] == 0)):
                    tempLigne = x - 1
                    tempColonne = y - 1
                    fin = False
            if orientation == 2:
                if ((x - 1 in range(0, 8)) and (y + 1 in range(0, 8)) and (table[x - 1][y + 1] == 0)):
                    tempLigne = x - 1
                    tempColonne = y + 1
                    fin = False
            if orientation == 3:
                if ((x + 1 in range(0, 8)) and (y - 1 in range(0, 8)) and (table[x + 1][y - 1] == 0)):
                    tempLigne = x + 1
                    tempColonne = y - 1
                    fin = False
            if orientation == 4:
                if ((x + 1 in range(0, 8)) and (y + 1 in range(0, 8)) and (table[x + 1][y + 1] == 0)):
                    tempLigne = x + 1
                    tempColonne = y + 1
                    fin = False
            if (fin == False):
                if (mouvement == None):
                    mouvement = Mouvement(tempLigne, tempColonne)
                else:  # Mouvement de plusieurs sauts
                    mouvement.ligne = tempLigne
                    mouvement.colonne = tempColonne
                temp = etat.getIdByPosition(1, x, y)
                if ((temp is not None) and (temp not in mouvement.pionManges)):
                    mouvement.pionManges.append(temp)
                    ##
                k = 1
                while ((tempLigne - k >= 0) and (tempColonne - k >= 0) and orientation != 4):
                    if (table[tempLigne - k][tempColonne - k] == 2): break
                    if (table[tempLigne - k][tempColonne - k] == 1):
                        self.testerSautDame(etat, tempLigne - k, tempColonne - k, 1, mouvement)
                        break
                    k=k+1
                k = 1
                while ((tempLigne - k >= 0) and (tempColonne + k <= 7) and orientation != 3):
                    #print(tempLigne,tempColonne)
                    if (table[tempLigne - k][tempColonne + k] == 2): break
                    if (table[tempLigne - k][tempColonne + k] == 1):
                        try:
                            self.testerSautDame(etat, tempLigne - k, tempColonne + k, 2, mouvement)
                        except:print(self.ligne,self.colonne,tempLigne,tempColonne)
                        break
                    k=k+1
                k = 1
                while ((tempLigne + k <= 7) and (tempColonne - k >= 0) and orientation != 2):
                    if (table[tempLigne + k][tempColonne - k] == 2): break
                    if (table[tempLigne + k][tempColonne - k] == 1):
                        self.testerSautDame(etat, tempLigne - k, tempColonne - k, 3, mouvement)
                        break
                    k=k+1
                k = 1
                while ((tempLigne + k <= 7) and (tempColonne + k <= 7) and orientation != 1):
                    if (table[tempLigne + k][tempColonne + k] == 2): break
                    if (table[tempLigne + k][tempColonne + k] == 1):
                        self.testerSautDame(etat, tempLigne + k, tempColonne + k, 4, mouvement)
                        break
                    k=k+1
        if (fin == True):
            if mouvement is not None:
                self.mouvOblig.append(mouvement)
                tuple = Tuple(self, mouvement)
                if (self.joueur == 1):
                    etat.mouvObgJ1.append(tuple)
                else:
                    etat.mouvObgJ2.append(tuple)
    #Teste tout les mouvements possibles pour un pion
    def testerMouvPossibles(self,etat):#Tester les deux chemins possibles ( droite / gauche ) selon le joueur
        table=etat.table
        i=self.ligne
        j=self.colonne
        if(self.joueur==1):
            if(self.dame==False):
                if (i - 1 >= 0 and j - 1 >= 0):#CASE GAUCHE LIBRE
                    mouv = Mouvement(i - 1, j - 1)
                    if (table[i - 1][j - 1] == 0):
                        self.mouvPossibles.append(mouv)
                    if (table[i - 1][j - 1] == 2): self.testerSautGauche(etat=etat)
                if (i - 1 >= 0 and j + 1 <= 7):#CASE GAUCHE PION ADVERSAIRE
                    mouv = Mouvement(i - 1, j + 1)
                    if (table[i - 1][j + 1] == 0):
                        self.mouvPossibles.append(mouv)
                    if (table[i - 1][j + 1] == 2): self.testerSautDroit(etat=etat)
            else:#Cas des dammes
                for k in range (0,7):
                    if ((i+k <=7)and(j+k <=7)):
                        if(table[i + k][j + k] == 0): self.mouvPossibles.append(Mouvement(i + k, j + k))
                        if (table[i + k][j + k] == 2):
                            self.testerSautDame(etat,i+k,j+k,4)
                            break
                        if (table[i + k][j + k] == 1): break
                    if ((i+k <=7)and(j-k >=0)):
                        if(table[i + k][j - k] == 0): self.mouvPossibles.append(Mouvement(i + k, j - k))
                        if (table[i + k][j - k] == 2):
                            self.testerSautDame(etat,i+k,j-k,3)
                            break
                        if (table[i + k][j - k] == 1):break
                    if ((i-k >=0)and(j+k <=7)):
                        if(table[i - k][j + k] == 0): self.mouvPossibles.append(Mouvement(i - k, j + k))
                        if (table[i - k][j + k] == 2):
                            self.testerSautDame(etat,i-k,j+k,2)
                            break
                        if (table[i - k][j + k] == 1):break
                    if ((i-k >=0)and(j-k >=0)):
                        if(table[i - k][j - k] == 0): self.mouvPossibles.append(Mouvement(i - k, j - k))
                        if (table[i - k][j - k] == 2):
                            self.testerSautDame(etat,i-k,j-k,1)
                            break
                        if (table[i - k][j - k] == 1):break
        else:
            if (self.dame == False):
                if (i + 1 <= 7 and j - 1 >= 0):
                    mouv = Mouvement(i + 1, j - 1)
                    if (table[i + 1][j - 1] == 0):
                        self.mouvPossibles.append(mouv)
                    if (table[i + 1][j - 1] == 1):
                        self.testerSautDroit(etat=etat)
                if (i + 1 <= 7 and j + 1 <= 7):
                    mouv = Mouvement(i + 1, j + 1)
                    if (table[i + 1][j + 1] == 0):
                        self.mouvPossibles.append(mouv)
                    if (table[i + 1][j + 1] == 1):
                        self.testerSautGauche(etat=etat)
            else:#Cas des dammes
                sens1 = True
                sens2 = True
                sens3 = True
                sens4 = True
                for k in range (1 ,7):

                    if ((i+k <=7)and(j+k <=7)and(sens1)):
                        if(table[i + k][j + k] == 0): self.mouvPossibles.append(Mouvement(i + k, j + k))
                        if (table[i + k][j + k] == 1):
                            self.testerSautDame(etat,i+k,j+k,4)
                            sens1=False
                        if (table[i + k][j + k] == 2):sens1=False
                    if ((i+k <=7)and(j-k >=0)and(sens2)):
                        if(table[i + k][j - k] == 0): self.mouvPossibles.append(Mouvement(i + k, j - k))
                        if (table[i + k][j - k] == 1):
                            self.testerSautDame(etat,i+k,j-k,3)
                            sens2=False
                        if (table[i + k][j - k] == 2):sens2=False
                    if ((i-k >=0)and(j+k <=7)and(sens3)):
                        if(table[i - k][j + k] == 0): self.mouvPossibles.append(Mouvement(i - k, j + k))
                        if (table[i - k][j + k] == 1):
                            self.testerSautDame(etat,i-k,j+k,2)
                            sens3=False
                        if (table[i - k][j + k] == 2):sens3=False
                    if ((i-k >=0)and(j-k >=0)and(sens4)):
                        if(table[i - k][j - k] == 0): self.mouvPossibles.append(Mouvement(i - k, j - k))
                        if (table[i - k][j - k] == 1):
                            self.testerSautDame(etat,i-k,j-k,1)
                            sens4 = False
                        if (table[i - k][j - k] == 2):sens4=False

#MAIN
#etat=Etat()
#etat.simulationAleatoire(tour=1)

#CheckersTree.lancer(etat)
#etat.simulationAleatoire(1)#Lancer la simulation aléatoire en commençant par le joueur1

#NOTES :
#________
 ############## MODIFIER REGLES DE FIN DU JEU
 ############## MODIFIER LA STRUCTURE D'ARBRE(SIMPLIFIER)

#BONUS
######SUPPRIMER REDONDANCES MOUVEMENT OBLIGATOIRE