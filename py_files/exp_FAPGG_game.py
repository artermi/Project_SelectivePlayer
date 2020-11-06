from PGG_game import PGG_5G
from player import APlayer
from random import choice, randint,choices
from pathlib import Path
import numpy as np 
import sys
import time

class FAPGG_5G(PGG_5G):
    def __init__(self,r,K,L,alp):
        super().__init__(r,K,L)
        player_matrix = []
        for i in range(L): 
            temp_matrix = []
            for j in range(L):
                isD = np.random.exponential(scale = alp)
                isD = isD - int(isD)
                temp_matrix.append(APlayer(choice([True,False]),isD))
#                temp_matrix.append(APlayer(choices([True,False],[0.1,0.9])[0],alp))
            player_matrix.append(temp_matrix)

        self.player_matrix = np.array(player_matrix)

    def one_play(self,i,j,rnd):
        mat = self.player_matrix
        L = self.L
        goods = mat[i,j].allocate(0,rnd)
        goods = goods + mat[(i+1) % L,j].allocate(4,rnd)
        goods = goods + mat[(i-1) % L,j].allocate(3,rnd)
        goods = goods + mat[i,(j+1) % L].allocate(1,rnd)
        goods = goods + mat[i,(j-1) % L].allocate(2,rnd)

        #Tell you I'm your north or south
        #+-----------> i+          +------------> i+
        #|    n1                   |     s2
        #| w4  0   e3              | e3  t  w4
        #|    s2                   |     n1
        #˅                         ˅
        #j+                        j+ 
        #  (origin)                  (I'm your...)
        
        return goods * self.r /5.0

    def the_most(self,a,b,c,d): #north,south,east,west
        lst = [a,b,c,d]
        mst = max(lst)
        dire = [1,2,3,4]
        mst_list = []
        for i in range(4):
            if lst[i] == mst:
                mst_list.append(dire[i])

        if len(mst_list) > 0:
            return choice(mst_list)

        return 0

    def two_players_play(self,rnd):
        xi,xj = self.xi,self.xj
        yi,yj = self.yi,self.yj
        mat = self.player_matrix
        L = self.L

        profit_x = self.one_play(xi,xj,rnd)
        profit_x = profit_x + self.one_play((xi+1) % L,xj,rnd)
        profit_x = profit_x + self.one_play((xi-1) % L,xj,rnd)
        profit_x = profit_x + self.one_play(xi,(xj+1) % L,rnd)
        profit_x = profit_x + self.one_play(xi,(xj-1) % L,rnd)

        profit_x = profit_x - 5 if mat[xi,xj].isCoop else profit_x

        profit_y = self.one_play(yi,yj,rnd)
        pye = self.one_play((yi+1) % L,yj,rnd) #east
        pyw = self.one_play((yi-1) % L,yj,rnd) #west
        pyn = self.one_play(yi,(yj-1) % L,rnd) #north
        pys = self.one_play(yi,(yj+1) % L,rnd) #south
        profit_y = profit_y + pye + pyw + pyn + pys

        profit_y = profit_y - 5 if mat[yi,yj].isCoop else profit_y

        mat[yi,yj].change_strategy(mat[xi,xj],self.K,profit_y,profit_x,self.the_most(pyn,pys,pye,pyw))

    """
    def choose_players(self):
        if super().choose_players():
            return True
        elif self.player_matrix[self.xi,self.xj].isCoop:
            return True
        else:
            return False
    """

def do_all_mode():
    rlist = [#2.4,2.41,2.42,2.43,2.44,2.45,2.46,2.47,2.48,2.49,2.5,2.6,2.7,2.8,2.9,
            #3,3.1,3.15,3.17,3.2,3.25,3.3,3.35,
            3.4,3.5,3.6,
            3.74,3.747,3.748,3.75,3.76,3.78,3.80,3.82,3.84,3.86,3.88,3.90,
            3.92,3.94,3.96,3.98,4.00,4.05,4.10,4.15,4.20,4.30,4.40,4.50,
            4.60,4.70,4.80,4.90,5.00,5.10,5.20,5.30,5.40,5.44,5.49,5.5]
    alps = [1/0.603] #[1/0.603,1/1.230,1/2.672] #0.45 0.4 0.3 // = 1.65, 0.81, 0.374 

    paths = []
    for alp in alps:
        path = 'EXP_' + str(int(alp * 100)).zfill(3)
        Path(path).mkdir(parents=True, exist_ok=True)
        paths.append((path,alp))

    for path in paths:
        p, alp = path

        for r in rlist:
            filename = p + '/lmd_' + str(int(alp * 100)).zfill(3) + '_'
            filename += 'r_' +  str(int(r * 1000) ) + '.dat'
            
            f = open(filename,"w")
            print('Now doing:' + filename)

            L = 200
            LL = L*L

            game = FAPGG_5G(r,0.5,L,alp) #r,K,L alp
            per_c = 0.5
            for i in range(10001):
                if i < 1000 and i % 30 == 0:
                    per_c = game.calculate_rate()
                    
                if i % 500 == 0:
                    per_c = game.calculate_rate()
                    f.write(str(i).zfill(6) + ' ' + '%.3f'%(per_c) + '\n')
                    print(i,per_c)

                if per_c == 1 or per_c == 0:
                    continue

                for j in range(LL):
                    modi = game.choose_players()
                    if not modi:
                        continue
                #If the strategy is not modified, no need to play the game
                    game.two_players_play(j + i * 1600)
            f.close()

def do_alpha_mode():
    rs = [4,4.5,5]
    alps = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    paths = []

    for r in rs:
        path = 'EXP_' + str(int( r * 1000))
        #path = 'r_040'
        Path(path).mkdir(parents=True, exist_ok=True)
        paths.append((path,r))

    for path in paths:
        p, r = path

        for alp in alps:
            filename = p + '/' + 'alp_' + str(int(alp * 10)).zfill(3) + '_'
            filename += 'r_' + str(int( r * 1000)) + '.dat'
            f = open(filename,"w")
            print('Now doing:' + filename)

            game = FAPGG_5G(r,0.5,40,alp) #r,K,L alp
            for i in range(10001):


                if i % 500 == 0:
                    per_c = game.calculate_rate()
                    f.write(str(i).zfill(6) + ' ' + '%.3f'%(per_c) + '\n')
                    print(i,per_c)
                if per_c == 1 or per_c == 0:
                    break

                for j in range(1600):
                    modi = game.choose_players()
                    if not modi:
                        continue
                #If the strategy is not modified, no need to play the game
                    game.two_players_play(j + i * 1600)
            f.close()



        
if __name__ == '__main__':
    msg0 = 'type "python FAPGG_game.py" if you want to run the big simulation'
    msg1 = 'type "python FAPGG_game.py rate alpha path" if just want to try'
    msg2 = 'for example "python FAPGG_game.py 4 0.5 r4a5"'
    print(msg0)
    print(msg1)
    print(msg2)

    if len(sys.argv) < 2:
        do_all_mode()
        sys.exit()
    if len(sys.argv) == 2:
        do_alpha_mode()
        sys.exit()

    #read from argv
    r = float(sys.argv[1])
    alp = float(sys.argv[2])
    path = sys.argv[3]

    game = FAPGG_5G(r,0.5,40,alp)
    start = time.time()
    for i in range(10001):
        if i % 500 == 0:
            print(i,game.calculate_rate())
        for j in range(1600):
#        if True:
            modi = game.choose_players()
            if not modi:
                continue
            game.two_players_play(j + i*1600)

        #if i % 20 == 0:
        #    game.print_pic(path + '/' + 'r_'+str(r) + '_alp_'+str(alp) + '_' + str(i).zfill(6))
    
    end = time.time()
    print('total_time: {}'.format(end - start))