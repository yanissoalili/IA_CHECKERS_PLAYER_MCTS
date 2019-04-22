from copy import deepcopy
def eatDroit(grid_copy,val):
    grid_copy[val[0]][val[1]]=0
    grid_copy[val[0]+1][val[1]-1]=0
    grid_copy[val[0]+2][val[1]-2]=1

def eatGauche(grid_copy,val):
    grid_copy[val[0]][val[1]] = 0
    grid_copy[val[0] + 1][val[1] + 1] = 0
    grid_copy[val[0] + 2][val[1] + 2] = 1
class NodePion:
    def __init__(self, val):
        self.val = val
        self.filsGauche = None
        self.filsDroit = None
        self.possibility=[]

    def generatefils(self, grid):
        if self.val[0] < 6 and self.val[1] > 1:

            if grid[self.val[0] + 1][self.val[1] - 1] == 2 and grid[self.val[0] + 2][self.val[1] - 2] == 0:

                self.filsDroit = NodePion((self.val[0] + 2, self.val[1] - 2))
                self.filsDroit.generatefils(grid)
        if self.val[0] < 6 and self.val[1] < 6:

            if grid[self.val[0] + 1][self.val[1] + 1] == 2 and grid[self.val[0] + 2][self.val[1] + 2] == 0:

                self.filsGauche = NodePion((self.val[0] + 2, self.val[1] + 2))
                self.filsGauche.generatefils(grid)

    @property
    def feuille (self):

        return self.filsGauche is None and self.filsDroit is None

    def existEat(self,grid):

        if self.val[0]<6:
            if self.val[1]==0:
                if grid[self.val[0]+1][self.val[1]+1]==2 and grid[self.val[0]+2][self.val[1]+2]==0:

                    return True
            elif self.val[1]==7:
                if grid[self.val[0] + 1][self.val[1] - 1] == 2 and grid[self.val[0] + 2][self.val[1] - 2] == 2:
                    return True
            else:

                if (grid[self.val[0] + 1][self.val[1] - 1] == 2 and grid[self.val[0] +2][self.val[1] - 2] == 0 and
                    self.val[1]>1)or\
                        (grid[self.val[0] + 1][self.val[1]+ 1] == 2 and self.val[1] < 6 and grid [self.val[0] + 2][self.val[1] + 2]== 0
                         ):
                    return True
        return False






    def ETAT__POSSIBLE(self, grid,possibility):
        if self.feuille is True:
            #append all grid in possibility
            print(grid)
            possibility.append(grid)
        else:
            if self.filsDroit is not None:
                grid_copy = deepcopy(grid)
                eatDroit(grid_copy, self.val)
                self.filsDroit.ETAT__POSSIBLE(grid_copy, possibility)
            if self.filsGauche is not None:
                grid_copy = deepcopy(grid)
                eatGauche(grid_copy, self.val)
                self.filsGauche.ETAT__POSSIBLE(grid_copy, possibility)

    def simpleMove(self, grid, liste):
        if self.val[0] < 7:

            if grid[self.val[0] + 1][self.val[1] + 1] == 0 and self.val[1] < 7:
                gridcopy = deepcopy(grid)
                gridcopy[self.val[0] + 1][self.val[1] + 1] = 1
                gridcopy[self.val[0]][self.val[1]] = 0
                liste.append(gridcopy)

            if grid[self.val[0] + 1][self.val[1] - 1] == 0 and self.val[1] > 0:
                gridcopy = deepcopy(grid)
                gridcopy[self.val[0] + 1][self.val[1] + 1] = 1
                gridcopy[self.val[0]][self.val[1]] = 0
                liste.append(gridcopy)





