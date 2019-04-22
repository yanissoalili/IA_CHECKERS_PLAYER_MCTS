#####################IA Function######################

from Pion import *
class joueur :
    def __init__(self, grid):
        self.eat_force=False
        self.listPion=[]
        self.pion_eat= None
        for x in range(0,8):
            for y in range(0,8):
                if(grid[x][y]==1):
                    self.listPion.append(pion(x, y))

    def existEat(self, grid):

        for element in self.listPion:
            if element.existEat(grid):
                if self.pion_eat is None:
                    return True
                elif self.pion_eat[0] == element.x and self.pion_eat[1] == element.y:
                    return True


        return False



    def possibility_J1(self, grid):
        joueur_possibility=[]
        for x in self.listPion :
            joueur_possibility.append(x.get_possible(grid, self.eat_force))
        return  joueur_possibility
    def possiblity_to_play(self, grid, x, y ):
        if(x,y) in self.possibility_J1(grid):
            return True
        return False
    def miseAjourPion(self, grid, joueurnum):
        self.listPion=[]
        for x in range(0,8):
            for y in range(0,8):
                if(grid[x][y]==joueurnum):
                    self.listPion.append(pion(x, y))

    def existPion(self,x,y):

        for index,element in enumerate(self.listPion):
            if x==element.x and y== element.y:

                return index
        return -1

    def temp(self, list, tuple):
        for element in list:
            if tuple in element :
                return True
        return False



    def play(self,grid,x,y,x_vide,y_vide):
        exist =self.existPion(x,y)

        self.eat_force=self.existEat(grid)


        if exist!= -1:
            pion_choisi=self.listPion[exist]


            if pion_choisi.mouvment_possible(grid,x_vide,y_vide,self.eat_force) and self.temp(self.possibility_J1(grid),(x_vide,y_vide)):
                return True,
        return False



















