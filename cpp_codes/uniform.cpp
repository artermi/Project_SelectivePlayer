#include "class_CFAPGG.h"

class UNIFAPGG: public FAPGG
{
public:
	 UNIFAPGG(const double rate,const double para):FAPGG(rate,para){
	 	build_specials(para);
	 }

	 void build_specials(const double para);
};
void UNIFAPGG::build_specials(const double para){
	double mover = (para <= 0.5) ? 0: (2.0 * para - 1.0) ;
	double range = (para <= 0.5) ? 2.0 * para: 2.0 * (1.0 - para);

	for(int i = 0; i < LL; i++)
		probs[i] = (double)rand()/(double)RAND_MAX * range + mover;
	memset(dir_name,'\0',sizeof(dir_name));
	strcpy(dir_name,"uniform");
	P = para;
}


int main(){
	srand(time(NULL));
	double alps[] ={
	0.2,0.3,0.4,0.45,0.5,0.7
	};
	double rs[]= {
		2.4,2.41,2.42,2.43,2.44,2.45,2.46,2.47,2.48,2.49,2.5,2.6,2.7,2.8,2.9,
		3,3.1,3.15,3.17,3.2,3.25,3.3,3.35,3.4,3.5,3.6,3.74,3.747,3.748,3.75,3.76,3.78,
		3.80,3.82,3.84,3.86,3.88,3.90,3.92,3.94,3.96,3.98,
        4.00,4.05,4.10,4.15,4.20,4.30,4.40,4.50,
        4.60,4.70,4.80,4.90,5.00,5.10,5.20,5.30,5.40,5.44,5.49,5.5
	};
	int Anum = sizeof(alps) / sizeof(alps[0]);
	int Rnum = sizeof(rs)/ sizeof(rs[0]);
	for(int i = 0; i < Anum; i++){
		for(int j = 0; j < Rnum; j++){
			UNIFAPGG gameOBj(rs[j],alps[i]);
			gameOBj.game(true);
		}
	}
	return 0;
}