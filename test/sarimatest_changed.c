// SPDX-License-Identifier: BSD-3-Clause
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../header/ctsa.h"

int main(void) {
	int i, N, d, L;
	double *inp;
	int p, q;
	int s, P, D, Q;
	double *phi, *theta;
	double *PHI, *THETA;
	double *xpred, *amse;
	sarima_object obj;
	p = 0;
	d = 1;
	q = 1;
	s = 12;
	P = 0;
	D = 1;
	Q = 1;


	L = 5;

	phi = (double*)malloc(sizeof(double)* p);
	theta = (double*)malloc(sizeof(double)* q);
	PHI = (double*)malloc(sizeof(double)* P);
	THETA = (double*)malloc(sizeof(double)* Q);

	xpred = (double*)malloc(sizeof(double)* L);
	amse = (double*)malloc(sizeof(double)* L);

	FILE *ifp;
	double temp[1200];

	puts("Will open file"); fflush(stdout);
//	ifp = fopen("../data/seriesG.txt", "r");
// TODO avoid tiny files, with N - s*D negative 
//	ifp = fopen("../data/ohlc_min.txt", "r");
	ifp = fopen("../data/1m-20241125_001625-20241125_165625.txt", "r");
	
	i = 0;
	if (!ifp) {
		printf("Cannot Open File");
		exit(100);
	}
	
	puts("Will read data"); fflush(stdout);	
	while (!feof(ifp)) {
		fscanf(ifp, "%lf \n", &temp[i]);
		i++;
	}
	N = i;
	printf("Read %d lines\n", N); fflush(stdout);	

	puts("Will calculate logarithm"); fflush(stdout);	
	inp = (double*)malloc(sizeof(double)* N);
	//wmean = mean(temp, N);

	for (i = 0; i < N; ++i) {
		inp[i] = log(temp[i]);
		//printf("%g \n",inp[i]);
	}

	/** TODO  compare N versus s*D */
	puts("Will init SARIMA"); fflush(stdout);	
	obj = sarima_init(p, d, q,s,P,D,Q, N);
	
	puts("Will fit a SARIMA nodel"); fflush(stdout);	
	sarima_setMethod(obj, 0); // Method 0 ("MLE") is default so this step is unnecessary. The method also accepts values 1 ("CSS") and 2 ("Box-Jenkins")
	//sarima_setOptMethod(obj, 7);// Method 7 ("BFGS with More Thuente Line Search") is default so this step is unnecessary. The method also accepts values 0,1,2,3,4,5,6. Check the documentation for details.
	sarima_exec(obj, inp);
	
	puts("Will print the summary"); fflush(stdout);	
	sarima_summary(obj);
	// Predict the next 5 values using the obtained ARIMA model
	sarima_predict(obj, inp, L, xpred, amse);
	printf("\n");
	printf("Predicted Values : ");
	for (i = 0; i < L; ++i) {
		printf("%g ", xpred[i]);
	}
	printf("\n");
	printf("Standard Errors  : ");
	for (i = 0; i < L; ++i) {
		printf("%g ", sqrt(amse[i]));
	}
	printf("\n");
	sarima_free(obj);
	free(inp);
	free(phi);
	free(theta);
	free(PHI);
	free(THETA);
	free(xpred);
	free(amse);
	return 0;

}
