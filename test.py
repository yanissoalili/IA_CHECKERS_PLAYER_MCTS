from CheckersTree import Noeud
from CheckersBasic import Etat,Tuple,Mouvement,Pion
from copy import deepcopy
import time

nbIterations=25
maxProfondeur=6

class Jeu:
    def __init__(self, etat):
        self.etat=etat

    def jouerHumain(self,i,j,x,y):
        if (len(self.etat.mouvObgJ1) > 0):
            pionChoisi = self.etat.getIdByPosition(1, i, j)
            for mouvement in (pionChoisi.mouvOblig):
                if ((mouvement.ligne == x) and (mouvement.colonne == y)):
                    self.etat.effectuerMouvement(pionChoisi, mouvement)
                    self.etat.miseAJourTable()
                    return 0
                else:
                    print("Mouvement impossible pour ce pion")
        else:
            print("Veuillez choisir votre mouvment")
            pionChoisi = self.etat.getIdByPosition(1, i, j)
            for mouvement in (pionChoisi.mouvOblig + pionChoisi.mouvPossibles):
                if ((mouvement.ligne == x) and (mouvement.colonne == y)):
                    self.etat.effectuerMouvement(pionChoisi, mouvement)
                    self.etat.miseAJourTable()
                    return 0
                else:
                    print("Mouvement impossible pour ce pion")

    def jouerIA(self):
        root = Noeud("ROOT", 2, self.etat)
        print(root.etat.table)
        root.etat.miseAJourTable()  # METTRE A Jour les pions
        root.expansion()
        for i in range(0, nbIterations):
            root.lancerMCTS()
        # for element in root.children:
        # print(element.id+"[ " + str(element.nbVictoiresNoeud) + " / " + str(element.nbSimulationsNoeud) + " ] --> " + str(
        # element.evaluationNoeud))
        res = root.selectionnerMeilleurMouvment()
        self.etat=res.etat.copierEtat()

        print(self.etat.table)
    def jouer(self, tour):
        self.jouerIA()
        self.etat.afficherTable()


