from player import Player
from random import choice, randint
from gen_image import FromArr_png
import numpy as np
import sys
import time

class PGG_5G:
    def __init__(self,r,K,L):
        #rate, noise and size
        self.r = r
        self.K = K
        self.L = L

        #x is the chosen player that need to suggest y its strategy
        self.xi = -1
        self.xj = -1
        self.yi = -1
        self.yj = -1

        self.first = True
        player_matrix = []
        for i in range(L):
            temp_matrix = []
            for j in range(L):
                temp_matrix.append(Player(choice([True,False])))
            player_matrix.append(temp_matrix)

        self.player_matrix = np.array(player_matrix)


    def one_play(self,i,j):
        #each we asked the players of grid[i][j] to play
        player_matrix = self.player_matrix
        goods = player_matrix[i,j].allocate()
        goods = goods + player_matrix[(i+1) % self.L, j].allocate() + player_matrix[(i-1) % self.L , j].allocate() 
        goods = goods + player_matrix[i, (j+1) % self.L].allocate() + player_matrix[i , (j-1) % self.L].allocate()

        return goods * self.r / 5.0 #just record the gain


    def two_players_play(self):
         #Means x and y have different strateies
        L = self.L
        player_matrix = self.player_matrix
        xi, xj = self.xi,self.xj
        yi, yj = self.yi,self.yj
        profit_x = self.one_play(xi,xj)
        profit_x = profit_x + self.one_play((xi+1)%L,xj) 
        profit_x = profit_x + self.one_play((xi-1)%L,xj)
        profit_x = profit_x + self.one_play(xi,(xj+1)%L) 
        profit_x = profit_x + self.one_play(xi,(xj-1)%L)
        if player_matrix[xi , xj].isCoop:
            profit_x = profit_x - 5

        profit_y = self.one_play(yi,yj)
        profit_y = profit_y + self.one_play((yi+1)%L,yj) + self.one_play((yi-1)%L,yj)
        profit_y = profit_y + self.one_play(yi,(yj+1)%L) + self.one_play(yi,(yj-1)%L)
        if player_matrix[yi, yj].isCoop:
            profit_y = profit_y - 5
            
        player_matrix[yi][yj].change_strategy(player_matrix[xi][xj],self.K,profit_y,profit_x)



    def choose_players(self):
        L = self.L
        i = randint(0,L-1)
        j = randint(0,L-1)

        rand_neigh = randint(0,3)
        
        if rand_neigh == 0:
        	self.yi = (i+1)%L
        	self.yj = j
        elif rand_neigh == 1:
        	self.yi = (i-1)%L
        	self.yj = j
        elif rand_neigh == 2:
        	self.yi = i
        	self.yj = (j+1)%L
        else:
        	self.yi = i
        	self.yj = (j-1)%L


        self.xi = i
        self.xj = j
        
        if self.player_matrix[self.yi,self.yj].isCoop != self.player_matrix[i,j].isCoop:
            return True

        return False #means two players use the same strategy, so no necessary to do the next run


    def calculate_rate(self):
        coor = 0
        L = self.L
        player_matrix = self.player_matrix
        ttl = L * L
        for i in range(L):
            for j in range(L):
                if player_matrix[i,j].isCoop:
                    coor = coor + 1
        return coor/ttl
        
    def print_pic(self,fname):
        FromArr_png(self.player_matrix,fname)


def do_all_mode():
    rlist = [3.74,3.747,3.748,3.75,3.76,3.78,3.80,3.82,3.84,3.86,3.88,3.90,
            3.92,3.94,3.96,3.98,4.00,4.05,4.10,4.15,4.20,4.30,4.40,4.50,
            4.60,4.70,4.80,4.90,5.00,5.10,5.20,5.30,5.40,5.44,5.49,5.5]
    for r in rlist:
        filename = 'sim2/sim_' +  str(int(r * 1000) ) + '.dat'
        f = open(filename,'w')
        print('Now doing:' + filename)

        game = PGG_5G(r,0.5,40) #r,K,L
        for i in range(10001):
            if i % 500 == 0:
                per_c = game.calculate_rate()
                f.write(str(i).zfill(6) + ' ' + '%.3f'%(per_c) + '\n')
                print(i,per_c)

            for j in range(1600):
                modi = game.choose_players()
                if not modi:
                    continue
            #If the strategy is not modified, no need to play the game
                game.two_players_play()
        f.close() 
      


if __name__ == '__main__':
    msg0 = 'type "python PGG_game.py" if you want to run the big simulation'
    msg1 = 'type "python PGG_game.py rate path" if just want to try'
    msg2 = 'for example "python PGG_game.py 4 r4"'
    print(msg0)
    print(msg1)
    print(msg2)

    if len(sys.argv) < 2:
        do_all_mode()
        sys.exit()

    r = float(sys.argv[1])
    path = sys.argv[2]
    game = PGG_5G(r,0.5,40) #r,K,L

    start = time.time()
    for i in range(10001):

        if i % 500 == 0:
            per_c = game.calculate_rate()
            print(i,per_c)

        #if i % 20 == 0:
        #    game.print_pic( path + '/r_'+ sys.argv[1] + '_' + str(i).zfill(6))

        for j in range(1600):
            modi = game.choose_players()
            if not modi:
                continue
            #If the strategy is not modified, no need to play the game
            game.two_players_play()
    end = time.time()
    print('total_time: {}'.format(end - start))
