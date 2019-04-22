def switchTabletoIA(table):
    for i in range(0,8):
        for j in range(0,8):
            if table[i][j]==3:
                table[i][j] =0


def switchtabletoPlayer(table):
    for i in range(0,8):
        for j in range(0,8):
            if i%2==0 and j%2==0 and table[i][j]==0:
                table[i][j]=3
            if i%2==1 and j%2==1 and table[i][j]==0:
                table[i][j]=3







