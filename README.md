# Project_SelectivePlayer
This is the source code of project "Small fraction of selective players can elevate general cooperation level significantly".

Two type of code are written: C++(12.0.0) code and Python (3.7.7 or later) code. The results of the two experiments are identical. However, only the python code can generate the spatial distribution of strategies. For a 200 by 200 player matrix, C++ code finishes 10,000 rounds (each round contains 40,000 elementary steps) in 5 minutes whilst in Python, the same matrix takes more than 5 hours to finish 10,000 rounds.



For the C++ code, makefile is avaliable to compile the desired code with the following command:

```  makefile
make DESIRE
```

with DESIRE being the "Deterministic", "Bimodal", "Exponential", "Power_Low", and "Uniform" or nothing and it compiles all. 

Modify the source code in the main function if it is necessary to change the Alphas (alps) and Rs (rs) array, or it will run all the combination of default Alphas and Rs.

```c++
int main(){
	srand(time(NULL));
	double alps[] ={
		0,0.2,0.3,0.4,0.45,0.5,0.7,1.0
	};
	double rs[]= {
		2.4,2.41,2.42,2.43,2.44,2.45,2.46,2.47,2.48,2.49,2.5,2.6,2.7,2.8,2.9,
		3,3.1,3.15,3.17,3.2,3.25,3.3,3.35,3.4,3.5,3.6,3.74,3.747,3.748,3.75,3.76,3.78,
		3.80,3.82,3.84,3.86,3.88,3.90,3.92,3.94,3.96,3.98,
        	4.00,4.05,4.10,4.15,4.20,4.30,4.40,4.50,
        	4.60,4.70,4.80,4.90,5.00,5.10,5.20,5.30,5.40,5.44,5.49,5.5
	};
  ....
}
```

The header class_CFAPGG.h can also be modified if need to modifyed the default K or L.

```c++
#define K 0.5
#define L 200
#define LL (L * L)
```



For the Python code, please uncomment this part of code in the main function if need to generate the strategy distribution of players:

```python
#        if i % 20 == 0:
#            game.print_pic(path + '/' + 'r_'+str(r) + '_alp_'+str(alp) + '_' + str(i).zfill(6))
```

To run the Python code, simply type the command:

```
python3 XX_FAPGG_game.py (alp) (r)
```

Chane the "XX" to desired distribution such as "bi" (for bimodal). The alp and r are the float number of game's Alpha and R. It's optional. Without them, the programs run the default combinations of Rs and Alphas.



For any further problem, please send an email to colin.cleveland.formal@gmail.com. Thank you very much.

Colin Cleveland Oct. 2020
