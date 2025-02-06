// SPDX-License-Identifier: BSD-3-Clause
#include <time.h>   /* CLOCKS_PER_SEC, clock() */
#include <stdio.h>  /* printf() */
#include <stdlib.h> /* calloc(), free(), atoi() */

#include "../header/ctsa.h"

#include "csv_in.h" /* csv_in() */

#include "sjson_macros.h" /* SJM_ macros */

#define DATA_IN "../data/1m-20241125_001625-20241125_165625.csv"

int main(int argc, char* const* argv) {
	int i, L, method;
	double *inp;
	double *xpred, *amse;
	size_t n_rows;
	size_t exec_id;
	
	clock_t start;
	clock_t stop;
	double duration;
	
	FILE* json_out = (FILE*)NULL;
	char buf[2048] = {'\0'};
	SJSON_MACROS_VARS

	ar_object obj;

	L = 5;

	if (argc < 2) {
		printf("%s: ERROR Missing execution number\n", argv[0]);
				
		/* Return to indicate failure*/
		return 2;
	}
	
	exec_id = atoi(argv[1]);
	
	if (argc > 2) {
		printf("%s: WARNING Additional parameters ", argv[0]);
		
		int narg = 2;
		for (narg = 1; narg < argc; narg++) {
			printf("\'%s\' ", argv[narg]);
		}
		puts("will be ignored\n");
		
		/* Return to indicate failure*/
		return 2;
	}

	start = clock();
	
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
 
	/* Releasing of dynamic memory */
	ar_free(obj);
			
	free(inp);
	free(xpred);
	free(amse);
	
	stop = clock();
	duration = (stop - start) / CLOCKS_PER_SEC;

	/* Saving the results and parameters as JSON file */
	sprintf(buf, "json/%04d.json", exec_id);
	json_out = fopen(buf, "w");
	
	if (! json_out) {
		printf("%s: ERROR Could not open file '%s' for output\n", 
			argv[0], buf);
		
		/* Return to indicate failure*/
		return 2;
	}

	buf[0] = '\0';
/*	
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
 */	
	SJM_OPEN_ALL(buf);

		SJM_OPEN_STRUCT("parameters", buf);
		
			SJM_OPEN_STRUCT("reading", buf);
				SJM_ADD_PAIR_STR("inp", DATA_IN, buf);
			SJM_CLOSE_STRUCT(buf);
		
			SJM_OPEN_STRUCT("init", buf);
				SJM_ADD_PAIR_INT("L", L, buf);
				SJM_ADD_PAIR_INT("n_rows", n_rows, buf);
				SJM_ADD_PAIR_INT("method", method, buf);
			SJM_CLOSE_STRUCT(buf);
				
		SJM_CLOSE_STRUCT(buf);
		
		SJM_OPEN_STRUCT("result", buf);
				
		SJM_CLOSE_STRUCT(buf);
	
	SJM_CLOSE_ALL(buf);
	
	fputs(buf, json_out);
	fclose(json_out);
	
	return 0;
}
