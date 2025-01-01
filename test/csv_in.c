/*
 * Tiny library to read CSV files in C
 * Created on Fri Dec 27 19:37:13 2024
 * 
 * @author: hilton
 * OBS: requires c99
 */

#if ! defined(__STDC_VERSION__)
	#error C99 is required 
	
#else /* defined(__STDC_VERSION__) */
#	if __STDC_VERSION__ < 199901
		#error This compiler is not implementing C99
#	endif
	
#endif /* ! defined(__STDC_VERSION__) */

#include <math.h>    /* NAN */
#include <stdio.h>   /* fopen(), fclose() */
#include <stdlib.h>  /* calloc(), free() */
#include <string.h>  /* strtok(), strlen(), strcnmp() */
#include <stdbool.h> /* bool, true, false */

#include "auxlib.h" /* deblank(), find_text(), is_numeric(), split() */

#define QUANTUM 2048

#if FUTURE_VERSION
struct _CSV {
    
};

/* TODO struct object-like CSV with open that opens the file and reads the 1st line */
/* TODO holds the field names, returns some columns, closes the file */

#endif /* 0 */

size_t 
read_csv_column(const char* csv_name, const char* col_name, double** column) 
{
	int rv;
    char buf[1024] = "";
    char* pbuf = (char*)NULL;
    char** row     = (char**)NULL;
    char** columns = (char**)NULL;
    double* work = NULL;
    size_t row_no = 0;
    size_t n_fields = 0;
    size_t n_columns = 0;
    size_t col_no = (size_t)-1;
    size_t total_rows = 0;
    size_t result = 0;
    FILE* csv_f = NULL;
    
    /* HINT opening the input file*/
    csv_f = fopen(csv_name, "r");
    if (NULL == csv_f) {
		/* TODO report opening problem */
		printf("ERROR Could not open file '%s'\n", csv_name);
		
        return (size_t)0;
    }
    
    /* HINT getting the header */
    pbuf = fgets(buf, sizeof(buf) - 1, csv_f);
    if (NULL == pbuf) {
		/* TODO report reading problem */
		printf("ERROR Could not read 1st line\n");
		
        return (size_t)0;
    }
	
	n_columns = split(buf, ",", &columns);
	
	rv = find_text(columns, n_columns, col_name);
	
    /* TODO if the suggested column name is not in the header, leave */
    if (-1 == rv) {
		/* TODO report reading problem */
		printf("ERROR Column '%s' was not found in header\n", col_name);
		
		puts("Columns found\n");
		for (col_no = 0; col_no < n_columns; col_no++) {
			printf("'%s' ", columns[col_no]);
		}
		
        return (size_t)0;
	}
    
    col_no = (size_t)rv;
    
    /* TODO allocate a number of elements in the workorary area */
    work = (double*)calloc(QUANTUM, sizeof(double));
    total_rows = QUANTUM;
    
    /* TODO for the rest of the file do */
    for (pbuf = fgets(buf, sizeof(buf) - 1, csv_f); 
		NULL != pbuf;
		pbuf = fgets(buf, sizeof(buf) - 1, csv_f)) { 
			 
		/* TODO break the CSV row in comma-separated values */
		n_fields = split(buf, ",", &row);
		
		/* TODO if work size is too small, realloc the work array with QUANTUM more */
		if (total_rows <= (row_no + 1)) {
			work = realloc(work, total_rows + QUANTUM);
			total_rows += QUANTUM;
		}
		
		/* TODO if the column number > number of fields, set NAN to it */
		if (col_no > (n_fields - 1)) {
			work[row_no] = NAN;
		}
		
		/* TODO if there's no element in the suggested position, set NAN to it */
		if ( ! strlen(row[col_no]) ) {
			work[row_no] = NAN;
		}
		
		/* TODO if there's no valid number in the suggested position, set NAN to it */
		if ( ! is_numeric(row[col_no]) ) {
			work[row_no] = NAN;
		}

		/* TODO add the number to the work area*/
		work[row_no] = strtod(row[col_no], NULL);

		row_no++;	
	}
    
    /* TODO reallocate the result area, using the number of elements */
    work = (double*)realloc(work, row_no*sizeof(double));
    
    /* TODO copy the work area to the result area */
    *column = work;
    
    result = row_no;
    
    /* Normal function termination */
    return result;
}
