import pygame
from test import *
from Function import *
from usefulFunction import *
pygame.init()


def deplacement(x,y,caseVide_X,caseVide_Y):
    temp=grid[x][y]
    grid[x][y] = 0
    grid[caseVide_X][caseVide_Y]=temp

state = Etat()
state.miseAJourTable()
jeu=Jeu(state)


jeu.etat.table = [
    [3, 2, 3, 2, 3, 2, 3, 2],
    [2, 3, 2, 3, 2, 3, 2, 3],
    [3, 2, 3, 2, 3, 2, 3, 2],
    [0, 3, 0, 3, 0, 3, 0, 3],
    [3, 0, 3, 0, 3, 0, 3, 0],
    [1, 3, 1, 3, 1, 3, 1, 3],
    [3, 1, 3, 1, 3, 1, 3, 1],
    [1, 3, 1, 3, 1, 3, 1, 3]]
grid = jeu.etat.table
marron =(174, 137, 100)
color=(115, 8, 0)
screen = pygame.display.set_mode((480,480))
pygame.display.set_caption("chekers")
screen.fill(marron)
pygame.display.flip()
xx=0
yy=0
for x in range(8):
    xx=60*x
    for y in range(8):
        yy=60*y
        if x%2==1:
            if y%2==0:
                pygame.draw.rect(screen, color, (xx,yy,60,60),0)
        else:
            if y%2==1:
                pygame.draw.rect(screen, color, (xx,yy,60,60),0)

######## fonction affiche pion
def etat (grid):
    for i in range(8):
        for j in range (8):
            if grid[i][j]==2:
                pygame.draw.circle(screen, (255, 255, 255), (60*j+30, 60*i+30), 25)
            if grid[i][j]==1:
                pygame.draw.circle(screen, (0,0,0), (60 * j + 30, 60 * i + 30), 25)
            if  grid[i][j]==0:
                pygame.draw.rect(screen, color, (j*60,i*60, 60, 60), 0)
    pygame.display.flip()


etat(grid)
pygame.display.flip()









run = True
choisi= None
choice = False
J2=joueur(grid)
a=0
b=0



while run :


    pygame.time.delay(100)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
        else:
            if(  event.type == pygame.MOUSEBUTTONDOWN and
            grid[int(pygame.mouse.get_pos()[1]/60)][int(pygame.mouse.get_pos()[0]/60)]==1):
                print(pygame.mouse.get_pos())
                posX = int(pygame.mouse.get_pos()[1]/60)
                posy = int(pygame.mouse.get_pos()[0]/60)
                choice = True
                if J2.pion_eat is None:
                    choisi = (posX, posy)
                elif posX==J2.pion_eat[0] and posy == J2.pion_eat[1]:
                    choisi = (posX, posy)


            if (event.type == pygame.MOUSEBUTTONDOWN and choice==True and
                    grid[int(pygame.mouse.get_pos()[1]/60)][int(pygame.mouse.get_pos()[0]/60)]==0 ):
                caseVide_X=int(pygame.mouse.get_pos()[1]/60)
                caseVide_Y=int(pygame.mouse.get_pos()[0]/60)
                print(J2.play(grid, choisi[0], choisi[1], caseVide_X, caseVide_Y))
                if J2.play(grid,choisi[0], choisi[1],caseVide_X,caseVide_Y ):
                    deplacement(choisi[0], choisi[1], caseVide_X, caseVide_Y)
                    if choisi[0]-1!=caseVide_X:
                        J2.pion_eat=(caseVide_X, caseVide_Y)
                        if choisi[1]-2 == caseVide_Y:
                           grid[choisi[0]-1][choisi[1]-1] = 0
                        elif choisi[1]+2 == caseVide_Y:
                            grid[choisi[0] - 1][choisi[1] + 1] = 0
                        p=pion(caseVide_X, caseVide_Y)
                        if p.existEat(grid):

                            b=False
                    else:
                        b=True
                    J2.miseAjourPion(grid, 1)
                    etat(grid)
                    if b :
                        #############Algoriyhme_IA to apply#############
                        J2.pion_eat = None

                        pygame.display.flip()

                    #########Play########put_Algorithme_her########
                        switchTabletoIA(grid)

                        state = Etat()
                        state.miseAJourTable()
                        jeu = Jeu(state)
                        jeu.etat.table=grid

                        jeu.etat.initPositions()
                        jeu.etat.miseAJourTable()
                        jeu.etat.afficherTable()


                        jeu.jouerIA()

                        jeu.etat.afficherTable()

                        grid=jeu.etat.table
                        switchtabletoPlayer(grid)
                        etat(grid)
                        pygame.display.flip()

                    pygame.display.flip()


            J2.eat_force = False



pygame.quit()
