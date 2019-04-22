class pion :
    def __init__(self, case_X, case_Y):
        self.x = case_X
        self.y = case_Y
        self.possibilityPion=[]
###########################IA##################""




   #####################simple user ##############

    def existEat(self, grid):

        if self.y == 0 :

            if grid[self.x - 1][self.y + 1] == 2:
                bool = self.possibility_to_eat_right(grid)
                if bool is not None:
                    return True



        elif self.y == 7:
            if grid[self.x - 1][self.y - 1] == 2:
                bool = self.possibility_to_eat_left(grid)
                if bool is not None:
                    return True
        else:

            if grid[self.x - 1][self.y + 1] == 2 and self.y<6:
                bool = self.possibility_to_eat_right(grid)
                if bool is not None:
                    return True

            if grid[self.x - 1][self.y - 1] == 2 and self.y>1:
                bool = self.possibility_to_eat_left(grid)
                if bool is not None:
                    return True
        return False


    def mouvment_possible(self,grid, x_vide, y_vide,eat):
        possibility = self.get_possible(grid,eat)
        if (x_vide, y_vide) in possibility:
            return True
        return False

    def possibility_to_eat_left(self,grid):
        case_x=self.x-1
        case_y=self.y-1
        if grid[case_x - 1][case_y - 1] == 0:
            return case_x - 1, case_y - 1
        return None

    def possibility_to_eat_right(self,grid):
        case_x=self.x-1
        case_y=self.y+1

        if grid[case_x - 1][case_y + 1] == 0:
            return case_x - 1, case_y + 1
        return None
    #def possibilty(self)
    def get_possible(self, grid,eat):
        x = self.x
        y = self.y
        possibility = []


        # cas Simple deux cases sont vides ####
        #############update her to force to eat Player 1 ############
        if y == 0:

            if grid[x - 1][y + 1] == 2 and self.y <6:
                bool = self.possibility_to_eat_right(grid)
                if bool is not None:
                    possibility.append(bool)

            elif grid[x - 1][y + 1] == 0 and eat is False:
                possibility.append((x - 1, y + 1))
        elif y == 7:
            if grid[x - 1][y - 1] == 0 and eat is False:

                possibility.append((x - 1, y - 1))
            elif grid[x - 1][y - 1] == 2 and self.y>1:
                bool = self.possibility_to_eat_left(grid)
                if bool is not None:
                    possibility.append(bool)
        else:



            if grid[x - 1][y + 1] == 2 and self.y<6:
                bool = self.possibility_to_eat_right(grid)
                if bool is not None:
                    possibility.append(bool)


            if grid[x - 1][y - 1] == 2 and self.y>1:
                bool = self.possibility_to_eat_left(grid)
                if bool is not None:
                    possibility.append(bool)
            if grid[x - 1][y - 1] == 0 and eat is False:


                possibility.append((x - 1, y - 1))
            if grid[x - 1][y + 1] == 0 and eat is False:
                possibility.append((x - 1, y + 1))

        self.possibilityPion=possibility

        return possibility

