/**
 * Workhorse for the testing of ctsa -- prototype.
 * Created on Mon Jan 27 14:07:20 2025
 * 
 * @author: hilton
 * 
 **/

#include <stdio.h>  /* printf(), fopen(), fflush(), puts() */
#include <string.h> /* strcmp() */

/** \todo use an enum */
#define NO_ERROR           0
#define ERROR_TOO_MANY     1
#define ERROR_FILE_NOTOPENED 2

void usage(int error, int argc, char* const* argv) {
	int ind = 0;
	switch(error) {
		case NO_ERROR:
			break;
			
		case ERROR_TOO_MANY:
			printf("%s: ERROR Inform just one filename\n\n", argv[0]);
			fflush(stdout);
			
			for (ind = 1; ind < argc; ind++) {
				printf("'%s' ", argv[ind]);
			}
			puts("were informed\n\n");
			fflush(stdout);
			
			break;
			
		case ERROR_FILE_NOTOPENED:
			printf("%s: ERROR Parameter file '%s' could not be opened\n\n", 
				argv[0], argv[1]);
			fflush(stdout);
			
			break;
			
		default:
			printf("%s: WARNING Unknown error code %d was ignored\n\n", 
				argv[0], error);
			fflush(stdout);
	}
	
	printf("%s -- ctsa test runner\n\n"
			"Usage: %s [file name]\n\n"
			"where 'file name' names a file in the data/ folder\n"
			"If omitted, the default parameters will be used\n", 
			argv[0], argv[0]  
		   );
}

int main(int argc, char* const* argv) {
	FILE* param_f = (FILE*)NULL;
	
	/** \todo  if help on the command line, show usage and leave */	
	if ((argc == 2) && !strcmp(argv[1], "help")) {
		usage(NO_ERROR, argc, argv);
		
		return NO_ERROR;
	}

	/** \todo if file name was not informed */
	if (argc > 2) { 		
		/** \todo show the usage and report too many parameters */
		usage(ERROR_TOO_MANY, argc, argv);
	
		/** \todo leave */
		return ERROR_TOO_MANY;
	}
	
	/** \todo if file name was informed */
	if (argc == 2) {
		/** \todo if file not found */
		char fname[1024] = "";
		strcat("data/", argv[1]);
		
		param_f = fopen(fname, "r");
		if (NULL == param) {
			/** \todo show error usage and leave */
			usage(ERROR_FILE_NOTOPENED, argc, argv);
			
			return ERROR_FILE_NOTOPENED;
		}
		
		/** \todo download parameters and expected results from filename */
		
	/** \todo if file name was not informed */		
	} else {
		/** \todo use the default parameters */
		/** \todo save the file name as stable */
	} 
	
	/** \todo do the tests */
	
	/** \todo save the test results */
	
	/* Normal function termination */
	return 0;
}
