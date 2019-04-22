from CheckersBasic import Etat,Mouvement
from copy import deepcopy,copy
from numpy import argmax,log,sqrt,inf
from operator import attrgetter
import time

global index
global cpt
cpt = 0
index = 0

#VERIFIER TEMPS EXECUTION COPIER JEU !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

nbIterations=100
maxProfondeur=6



class Noeud:  # Add Node feature

    def __init__(self,id,tour=1,etat=None, parent=None, children=None,):
        self.tour=tour
        self.children=list()
        if parent==None:#Noeud root
            self.root=self
            self.profondeur=0
            self.is_root=True
        else:
            self.root=parent.root
            self.profondeur = parent.profondeur + 1
            self.is_root=False
            parent.children.append(self)

        self.parent=parent

        self.etat=etat


        self.nbVictoiresNoeud=0
        self.nbSimulationsNoeud=0
        self.evaluationNoeud=0.0
        self.visite=False
        self.expanded=False

        self.id=id

        if self.is_root:self.nbSimulationsTotal=0
        else: self.nbSimulationsTotal=None

    def afficherNoeud(self):
        print("P=" + str(self.parent.id) + ",Fils:" + str(len(self.children)))

    def afficherArbre(self):
        profondeur=0

        self.afficherNoeud()
        for element in self.children:
           element.afficherNoeud()
        for element in self.children:
            element.afficherArbre()

    def copierNoeudPourSimulation(self,noeud):
        self.etat.table=list(noeud.etat.table)

        self.etat.pionsJ1=list(noeud.etat.pionsJ1)
        self.etat.pionsJ2=list(noeud.etat.pionsJ2)
        self.tour = copy(self.tour)
        self.etat.mouvObgJ1=list(noeud.etat.mouvObgJ1)
        self.etat.mouvObgJ2 = list(noeud.etat.mouvObgJ2)

    def calculerUCB(self):
        c=2.0
        ni=self.nbSimulationsNoeud
        t=self.parent.nbSimulationsNoeud
        wi=self.nbVictoiresNoeud
        if(ni == 0):self.evaluationNoeud=inf
        else:self.evaluationNoeud=(wi/ni)+(c*sqrt(log(99)/ni))

    def expansion(self):
        global index
        self.etat.miseAJourTable()
        if (self.id == "Noeud285"):
            print(self.expanded)

            self.etat.afficherTable()
            for i in self.etat.pionsJ1:
                print("[ %s , %s ]" % (i.ligne,i.colonne))
            print(self.etat.pionsJ1.__len__())
            print(self.etat.pionsJ2.__len__())

        self.expanded=True
        #Arreter la generation si la profondeur max est atteinte ! utilié l'attribut depth
        if self.tour==1:
            exp_time = time.time()
            if(len(self.etat.mouvObgJ1)>0):
                for i,element in enumerate(self.etat.mouvObgJ1):
                    etatTemp = Etat(self.etat)
                    pionTemp = element.pion.copierPion()
                    mouvTemp = element.mouvement.copierMouvement()
                    etatTemp.effectuerMouvement(pionTemp,mouvTemp)
                    etatTemp.pionsJ1[i] = pionTemp
                    etatTemp.miseAJourTable()
                    index = index + 1
                    noeud = Noeud("Noeud" + str(index),2, etatTemp, parent=self, children=None)
                    #TESTER FIN DE PARTIE ??
            else:
                for i,pion in enumerate(self.etat.pionsJ1):
                    for mouvement in pion.mouvPossibles:
                        etatTemp = Etat(self.etat)
                        pionTemp = pion.copierPion()
                        mouvTemp = mouvement.copierMouvement()
                        etatTemp.effectuerMouvement(pionTemp,mouvTemp)
                        etatTemp.pionsJ1[i] = pionTemp
                        etatTemp.miseAJourTable()
                        #etatTemp.afficherTable()
                        index = index + 1
                        noeud = Noeud("Noeud" + str(index), 2,etatTemp, parent=self, children=None)
                        #noeud.copierJeu(etatTemp)
                        #TESTER FIN DE PARTIE ??
            #print("--- ExpaXXXXXnsion : %s---" % (time.time() - exp_time))
        else:
            if (len(self.etat.mouvObgJ2) > 0):
                for i, element in enumerate(self.etat.mouvObgJ2):
                    etatTemp = Etat(self.etat)
                    pionTemp = element.pion.copierPion()
                    mouvTemp = element.mouvement.copierMouvement()
                    etatTemp.effectuerMouvement(pionTemp, mouvTemp)
                    etatTemp.pionsJ2[i] = pionTemp
                    etatTemp.miseAJourTable()
                    # TESTER FIN DE PARTIE ?? RETURN De la methode effectuerMouvement
                    index = index + 1
                    noeud = Noeud("Noeud" + str(index), 1,etatTemp, parent=self, children=None)

                    #noeud.copierJeu(etatTemp)
            else:
                for i, pion in enumerate(self.etat.pionsJ2):
                    for j, mouvement in enumerate(pion.mouvPossibles):
                        etatTemp = Etat(self.etat)
                        pionTemp = pion.copierPion()
                        mouvTemp = mouvement.copierMouvement()
                        etatTemp.effectuerMouvement(pionTemp, mouvTemp)
                        etatTemp.pionsJ2[i] = pionTemp
                        etatTemp.miseAJourTable()
                        # TESTER FIN DE PARTIE ??
                        index = index + 1
                        noeud = Noeud("Noeud" + str(index), 1,etatTemp, parent=self, children=None)
                        #t=time.time()
                        #print("SSSSSS %s" %(t-time.time()))

    def selection(self):#calcule l'ucb des fils et choisit le meilleur parmi eux
        global cpt
        cpt=cpt+1
        #le dernier noeud visité ne va pas calculer sa valeur
        for element in self.children:
            element.calculerUCB()

        try:
            meilleurNoeud=max(self.children, key=attrgetter('evaluationNoeud'))
        except:
            print("EROOOOOOOOOOOOOOOOOR")
            self.etat.table()
            print(self.id)


        return meilleurNoeud

    def update(self,resultat):#met a jour le noeud actuel et ses fils
        while(self.root!=self):
            self.parent.nbVictoiresNoeud=self.parent.nbVictoiresNoeud+resultat
            self.parent.nbSimulationsNoeud=self.parent.nbSimulationsNoeud+1
            self=self.parent
        #if(self.is_root):self.nbSimulationsTotal = self.nbSimulationsNoeud
        #On utilise la variable nbSimulationsTotal du root seulement

    def simulation(self):#simule le resultat d'un scenario aléaotoire a partir de l'etat actuel

        self.root.nbSimulationsTotal = self.root.nbSimulationsTotal + 1
        self.nbSimulationsNoeud = self.nbSimulationsNoeud+1

        temp=Noeud("Temp",self.tour,etat=Etat())
        #temp.copierNoeudPourSimulation(self)
        resultat = temp.etat.simulationAleatoire(self.tour)
        #soit on fait V=1,E=0,D=-1 ou V=1,Else=0
        if resultat==1 :
            self.nbVictoiresNoeud = self.nbVictoiresNoeud+1
            return 1
        #Ajouter Defaite : -1 egalité :0 ??????????????????????????????????????????????????????????????????????
        else: return 0

    def lancerMCTS(self):
        t=time.time()
        if(self.expanded==False):#le root a fais son expansion avant l'appel de la méthode
            self.expansion()

        elu=self.selection()
        if((elu.visite==False)and(elu.profondeur<maxProfondeur)):#le noeud a deja ete visite une fois ( ou profondeur max atteinte ) > excuter simulatio
            resultat=elu.simulation()
            elu.update(resultat)
            elu.visite=True
            if(elu.root.nbSimulationsTotal==nbIterations):
                elu.calculerUCB()#20 est le nombre de test a effectuer

            #print("------------------ ITERATION : %s---" % (time.time() - t))
        else:#le noeud n'a pas encore été visité > exécuter expansion
            elu.lancerMCTS()
            #elu.update()
            #pour faire les update en remontant


    def selectionnerMeilleurMouvment(self):
        return max(self.children, key=attrgetter('evaluationNoeud'))

def lancer(etat):

        root = Noeud("ROOT",2,etat)
        #print(type(root.etat))
        root.etat.miseAJourTable()  # METTRE A Jour les pions
        root.expansion()
        for i in range (0,nbIterations):
            root.lancerMCTS()

        #for element in root.children:
            #print(element.id+"[ " + str(element.nbVictoiresNoeud) + " / " + str(element.nbSimulationsNoeud) + " ] --> " + str(
              #element.evaluationNoeud))
        res=root.selectionnerMeilleurMouvment()

        return res

def none():
    etat=Etat()
    root=Noeud("ROOT",1,etat)
    root.etat.miseAJourTable()
    root.expansion()
    childnv1 = root.children[0]
    childnv1.etat.miseAJourTable()
    childnv1.expansion()
    childnv2 = childnv1.children[0]
    childnv2.etat.miseAJourTable()
    childnv2.expansion()
    childnv3 = childnv2.children[0]
    childnv3.etat.miseAJourTable()
    childnv3.expansion()
    childnv4 = childnv3.children[0]

    childnv4.expansion()
    childnv5 = childnv4.children[0]
    childnv5.etat.miseAJourTable()
    childnv5.expansion()

    liste=[root,childnv1,childnv2,childnv3,childnv4,childnv5]

    for i in liste:
        print(i.profondeur)
        i.etat.afficherTable()
        print (i.etat.pionsJ1.__len__())
        print(i.etat.pionsJ2.__len__())


#childnv2.etat.afficherTable()

#print(childnv2.etat.afficherMouvPossibles(tour=1))
#childnv2.etat.miseAJourTable()
#print(childnv2.etat.afficherMouvPossibles(tour=1))



#root.children[6].simulation()
#for i in root.children:
 #   i.etat.afficherTable()
#root.selection().etat.afficherTable()


#root.simulation()
#print(root.selection())

#x=lancer(etat)
#print("fin")
#x.etat.afficherTable()





