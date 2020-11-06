#include "class_CFAPGG.h"
using namespace std;

void FAPGG::build_specials(const double para){
	for(int i = 0; i < LL; i++)
		probs[i] = para;
	memset(dir_name,'\0',sizeof(dir_name));
	strcpy(dir_name,"_det");
	P = para;
}

FAPGG::FAPGG(const double rate,const double para){
	r = rate;

	for(int i = 0; i < LL; i++){
		Strategy[i] = rand() % 2;
		D_Strate[i] = false;
		MST_N[i] = -1;
		Next_MST_N[i] = -1; 
	}

	for(int i = 0; i < LL; i++){
		Neighbour[i][0] = (i - L + LL ) % LL; //North
		Neighbour[i][1] = (i + L) % LL;
		Neighbour[i][2] = (i + 1) % LL;
		Neighbour[i][3] = (i - 1 + LL) % LL;
	}
	build_specials(para);
		
}

double FAPGG::unit_game(const int cent){

	if(curr[cent] < rnd){
		if(Strategy[cent] == 1){
			D_Strate[cent] =  (double)rand()/(double)RAND_MAX < probs[cent];
			MST_N[cent] = Next_MST_N[cent];
		}
		curr[cent] = rnd;
	}
	for(int i = 0; i < 4; i ++){
		int person = Neighbour[cent][i];
		if(curr[person] < rnd){
			if(Strategy[person] == 1){
				D_Strate[person] = (double)rand()/(double)RAND_MAX < probs[person];
				MST_N[person] = Next_MST_N[person];
			}
			curr[person] = rnd;
		}
	}
	
	double contrib = (double) Strategy[cent];

	for(int i = 0; i < 4; i++){
		int person = Neighbour[cent][i];
		if(Strategy[person] == 0)
			contrib += 0;
		
		else if(D_Strate[person] && MST_N[person] >= 0){
			contrib += (MST_N[person] == cent)? 4:0;
		}
		else
			contrib += 1.0;
	}

	return (contrib * r) / 5.0;
}


double FAPGG::centre_game(const int cent,const int isX){
	double profit = unit_game(cent);
	double earn[4] = {0.0,0.0,0.0,0.0};
	for(int i = 0; i < 4; i++){
		earn[i] = unit_game(Neighbour[cent][i]);
		profit += earn[i];
	}

	profit -= 5.0 * double(Strategy[cent]);
	if(isX)
		return profit;

	double mst_amount = *max_element(earn,earn+4);
	int maxNes[4] = {-1,-1,-1,-1};
	int max_amount = 0;

	for(int i = 0; i < 4; i ++){
		if(earn[i] + 0.0000001 >= mst_amount){
			maxNes[max_amount] = Neighbour[cent][i];
			max_amount ++;
		}
	}

	Next_MST_N[cent] = maxNes[rand() % max_amount];

	return profit;
}

int FAPGG::game(bool ptf){
	FILE *file;
	if(ptf){
		char path[100];
		char dirt[100];
		sprintf(dirt,"%s_%03d",dir_name, (int)(P*100));
		sprintf(path,"%s/alp_%03d_r_%04d.dat", dirt, (int)(P*100), (int)(r*1000));
		printf("Now file:%s\n",path);
		mkdir(dirt,0700);
		file = fopen(path,"w+");
	}
	double rate = 0.0;

	for(int i = 0; i < 10001; i++){

		if(i % 500 == 0){
			double total = 0;
			for(int j = 0; j < LL; j++)
				total += double(Strategy[j]);

			rate = double (total/double(LL));
			if(ptf)
				fprintf(file, "%06d %.3f\n",i,rate);
			printf("%d %.3f\n",i, rate );

		}
		if(rate - 0.000001 <= 0 || rate + 0.000001 >= 1 || i == 10000)
			continue;
		

		for(int j = 0; j < LL; j++){
			int x = rand() % LL;
			int y = Neighbour[x][rand() % 4 ];
			rnd++;
			if (Strategy[x] == Strategy[y])
				continue;
//			cout << x << ',' << y <<endl;
			double x_earn = centre_game(x,1);
			double y_earn = centre_game(y,0);

			if ((double)rand()/(double)RAND_MAX < 1.0/( 1.0 + exp((y_earn - x_earn)/K) ) )
				Strategy[y] = Strategy[x];
		}
	}
	if(ptf)
		fclose(file);

	return 0;
}

/*
int main(int argc, char** argv){
	srand(time(NULL));
	double para = 0.3;
	double r = 3.5;
	if(argc > 2){
		r =    atof(argv[1]);
		para = atof(argv[2]);
	}
	printf("Now doing Derermistic mode with r:%f alpha:%f\n",r,para);
	FAPGG gameOBJ(r,para);
	gameOBJ.game(true);

	return 0;
}
*/