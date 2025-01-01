/*
 * Header for a tiny library that reads CSV files in C
 * Created on Mon Dec 30 08:29:10 2024
 * 
 * @author: hilton
 * OBS: requires c99
 */

#if !defined(__CSV_IN_H)
#define __CSV_IN_H

#if ! defined(__STDC_VERSION__)
	#error C99 is required 
	
#else /* defined(__STDC_VERSION__) */
#	if __STDC_VERSION__ < 199901
		#error This compiler is not implementing C99
#	endif
	
#endif /* ! defined(__STDC_VERSION__) */

size_t 
read_csv_column(const char* csv_name, const char* col_name, double** column);

#endif /* !defined(__CSV_IN_H) */
