from NodePion import *
class Etat :
    def __init__(self, grid):
        self.grid = grid
        self.SON = []#les etats SON
        self.PION = []#position de pion
        self.SonNode=[]#liste de pointeur vers les sons
        #recupperer les position de chaque pion
    def pionOfEtat(self):
        for x in range(0,8):
            for y in range(0,8):
                if self.grid[x][y] == 1:
                    self.PION.append((x, y))
    def sonOfEtat(self):
        ##########force EAT################
        for element in self.PION:
            print(element)
            node=NodePion(element)
            node.generatefils(self.grid)
            if node.existEat(self.grid):
                node.ETAT__POSSIBLE(self.grid, self.SON)
        if len(self.SON)==0 :
            for element in self.PION:

                node = NodePion(element)
                node.generatefils(self.grid)
                node.simpleMove(self.grid,self.SON)
    #Expansion d'un noeud
    def Expansion(self):
        for element in self.SON:
            self.SonNode.append(Etat(element))
    

e= Etat([
    [1, 3, 1, 3, 1, 3, 1, 3],
    [3, 1, 3, 2, 3, 1, 3, 2],
    [1, 3, 0, 3, 1, 3, 1, 3],
    [3, 2, 3, 2, 3, 1, 3, 2],
    [0, 3, 1, 3, 0, 3, 0, 3],
    [3, 2, 3, 2, 3, 2, 3, 2],
    [2, 3, 2, 3, 2, 3, 2, 3],
    [3, 2, 3, 2, 3, 2, 3, 2]])
e.pionOfEtat()
e.sonOfEtat()
e.Expansion()








