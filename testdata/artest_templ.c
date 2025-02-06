// SPDX-License-Identifier: BSD-3-Clause
#include <stdio.h>  /* printf() */
#include <stdlib.h> /* calloc(), free() */
#include "../header/ctsa.h"

#include "csv_in.h" /* csv_in() */

#define DATA_IN "../data/1m-20241125_001625-20241125_165625.csv"
#define JSON_OUT "json/artest_0001.json"


int main(int argc, char* const* argv) {
	int i, L, method;
	double *inp;
	double *xpred, *amse;
	size_t n_rows;
	FILE* json_out = (FILE*)NULL;

	ar_object obj;

	L = 5;

	if (argc > 1) {
		printf("%s: WARNING Additional parameters ", argv[0]);
		
		int narg = 1;
		for (narg = 1; narg < argc; narg++) {
			printf("\'%s\' ", argv[narg]);
		}
		puts("will be ignored\n");
		
		/* Return to indicate failure*/
		return 1;
	}

	xpred = (double*)calloc(sizeof(double),  L);
	amse = (double*)calloc(sizeof(double), L);

	n_rows = read_csv_column(DATA_IN, "Close", &inp);
	if (0 == n_rows) {
		printf("%s: ERROR Could not load data from file '%s'\n", 
			argv[0], DATA_IN);
		
		/* Return to indicate failure*/
		return 1;
	}

	printf("Read %lu lines\n", n_rows);

	method = 0; // method 0 - Yule Walker, Method 1 - Burg, Method 2, MLE (Box-Jenkins)
	obj = ar_init(method, n_rows);
	ar_exec(obj, inp);
	ar_summary(obj);
	
	// Predict the next 5 values using the obtained ARIMA model
	ar_predict(obj, inp, L, xpred, amse);
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

	/* Saving the results and parameters as JSON file */
	json_out = fopen(JSON_OUT, "w");
	
	if (! json_out) {
		printf("%s: ERROR Could not open file '%s' for output\n", 
			argv[0], JSON_OUT);
		
		/* Return to indicate failure*/
		return 2;
	}
	
	fputs("{\n", json_out);
	
	fputs("\t\"parameters\" : {\n", json_out);
	
	fputs("\t\t\"reading\" : {\n", json_out);
	
	fprintf(json_out, "\t\t\t\"inp\" : \"%s\"\n", DATA_IN);
	
	fputs("\t\t},\n", json_out);
	
	fputs("\t\t\"init\" : {\n", json_out);
	
	fprintf(json_out, "\t\t\t\"L\" : %d,\n", L);
	fprintf(json_out, "\t\t\t\"n_rows\" : %lu,\n", n_rows);
	fprintf(json_out, "\t\t\t\"method\" : %d\n", method);
	
	fputs("\t\t},\n", json_out);
	
	fputs("\t\t\"fitting\" : {\n", json_out);
	fputs("\t\t\t\"obj\" : \"\",\n", json_out);
	fputs("\t\t\t\"inp\" : \"\"\n", json_out);
	fputs("\t\t},\n", json_out);
	
	fputs("\t\t\"summary\" : {\n", json_out);
	fputs("\t\t\t\"obj\" : \"\"\n", json_out);
	fputs("\t\t},\n", json_out);
	
	fputs("\t\t\"predict\" : {\n", json_out);
	fputs("\t\t\t\"obj\" : \"\",\n", json_out);
	fputs("\t\t\t\"inp\" : \"\",\n", json_out);
	fputs("\t\t\t\"L\" : \"\",\n", json_out);
	fputs("\t\t\t\"xpred\" : \"\",\n", json_out);
	fputs("\t\t\t\"amse\" : \"\"\n", json_out);
	fputs("\t\t},\n", json_out);
	
	fputs("\t},\n", json_out);
	
	fputs("\t\"results\" : {\n", json_out);
	
	fputs("\t}\n", json_out);
	
	fputs("}\n", json_out);
	
	fclose(json_out);

	/* Releasing of dynamic memory */
	ar_free(obj);
			
	free(inp);
	free(xpred);
	free(amse);

	
	return 0;
}
