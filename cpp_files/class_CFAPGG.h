#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <algorithm>
#include <string>
#include <sys/stat.h>
#include <sys/types.h>


#define K 0.5
#define L 200
#define LL (L * L)

class FAPGG{
public:
	long long rnd;
	double r;
	double P;
	char dir_name[100];

	int Strategy[LL];
	bool D_Strate[LL]; // False initially
	int Neighbour[LL][4];
	int MST_N[LL];
	int Next_MST_N[LL];
	double probs[LL];
	long long curr[LL];

	void build_specials(const double para);
	FAPGG(const double rate, const double para);
	double unit_game(const int cent);
	double centre_game(const int cent,const int isX);
	int game(bool ptf);
};