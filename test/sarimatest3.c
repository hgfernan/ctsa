// SPDX-License-Identifier: BSD-3-Clause
#include <stdio.h>
#include <stdlib.h> /* calloc(), malloc(), free()*/
#include <math.h>
#include "../header/ctsa.h"

#include "csv_in.h" /* csv_in() */

#define INPUT_FILE "../data/1m-20241125_001625-20241125_165625.csv"

int main(void) {
	int i, d, L;
	int p, q;
	int s, P, D, Q;
	double *xpred, *amse;
	double *inp = (double*)NULL;
	double *column = (double*)NULL;
	size_t n_rows = 0;
	sarima_object obj;
	
	p = 0;
	d = 1;
	q = 1;
	s = 12;
	P = 0;
	D = 1;
	Q = 1;

	L = 5;

	xpred = (double*)malloc(sizeof(double)* L);
	amse = (double*)malloc(sizeof(double)* L);

	n_rows = read_csv_column(INPUT_FILE, "Close", &column);
	if (0 == n_rows) {
		printf("Could not load data from file '%s'", INPUT_FILE);
		exit(100);
	}

	printf("Read %lu lines\n", n_rows);
	
	inp = (double*)calloc(n_rows, sizeof(double));
	//wmean = mean(temp, N);

	for (i = 0; i < n_rows; ++i) {
		inp[i] = log(column[i]);
		//printf("%g \n",inp[i]);
	}

	obj = sarima_init(p, d, q, s, P, D, Q, n_rows);
	sarima_setMethod(obj, 0); 
	/** \brief Method 0 ("MLE") is default so this step is unnecessary. 
	 * The method also accepts values 1 ("CSS") and 2 ("Box-Jenkins")
	 **/

	// sarima_setOptMethod(obj, 7);
	/** \brief Method 7 ("BFGS with More Thuente Line Search") is 
	 * default so this step is unnecessary. The method also accepts 
	 * values 0,1,2,3,4,5,6. Check the documentation for details.
	 **/
	 
	sarima_exec(obj, inp);
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
	free(column);
	free(inp);
	free(xpred);
	free(amse);
	
	return 0;
}
