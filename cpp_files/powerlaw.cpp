#include "class_CFAPGG.h"

#define fine 50
bool arr_gen = false;
double value[fine];
double pbs[fine];

void gen_rv(double exp){
	double Upper = 3.0;
	double Lower = 0.1;
	while(Upper - Lower > 0.00001){
		double x = (Upper + Lower) / 2.0;
		double expe = 0;
		double prob_sum = 0;
		for(int i = 0; i < 50; i++){
			prob_sum += pow( (1/(double)(i+1)), x);
			expe += double(i+1) / fine * ( pow((1/ (double)(i+1)),x) );
		}
		double diff = expe/prob_sum - exp;
		if(diff > 0)
			Lower = (Upper + Lower) / 2;
		else
			Upper = (Upper + Lower) / 2;
	}
	double pr = (Upper + Lower) / 2;
	double sum = 0;
	for(int i = 0; i < fine; i++){
		value[i] = (double)(i+1) / fine;
		pbs[i] = pow(1/ (double)(i+1),pr);
		sum += pbs[i];
	}
	for(int i = 0; i < fine; i++)
		pbs[i] /= sum;
}


double random_with_prob(){
	double p = (double) rand()/(double) RAND_MAX;
	double accu = 0.0;

	for(int i = 0; i < fine; i++){
		accu += pbs[i];
		if(accu >= p)
			return value[i];
	}
	return value[fine-1];
}

double power_law(const double exp){
	if(!arr_gen){
		gen_rv(exp);
		arr_gen = true;
	}

	return random_with_prob();
}


class PLFAPGG: public FAPGG
{
public:
	 PLFAPGG(const double rate,const double para):FAPGG(rate,para){
	 	build_specials(para);
	 }

	 void build_specials(const double para);
};
void PLFAPGG::build_specials(const double para){
	for(int i = 0; i < LL; i++)
		probs[i] = power_law(para);
	memset(dir_name,'\0',sizeof(dir_name));
	strcpy(dir_name,"pLaw");
	P = para;
}


int main(){
	srand(time(NULL));
	double alps[] ={
	0.3,0.4,0.45
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
			PLFAPGG gameOBj(rs[j],alps[i]);
			gameOBj.game(true);
			arr_gen = false;
		}
	}
	return 0;
}