/**
 * A tiny lib of functions to manipulate strings C misses
 * Created on Sun Dec 29 21:34:24 2024
 * 
 * @author: hilton
 * 
 **/
 
#include <stdlib.h> /* calloc(), realloc(), free() */
#include <string.h> /* strcpy(), strlen() */
#include <regex.h>  /* regex_t, regmatch_t, regcomp(), regexec() */

#include "auxlib.h"
 
char* 
deblank(const char* input) 
{
	int start = 0;
	int stop = 0;
	size_t length = 0;
	size_t full_length = 0;
	char* result = (char*)NULL;
	
	if (!input) return NULL;
	
	full_length = strlen(input);
	if (0 == full_length) {
		return (char*)calloc(1, sizeof(char*));
	}
	
	for (start = 0; *(input + start) == ' '; start++)
		;
	
	for (stop = full_length - 1; stop > 0; stop--) {
		if (*(input + stop) != ' ') break;
	} 
	
	length = full_length - start + 1; 
	length -= full_length - stop;
	
	result = (char*)calloc(length + 1, sizeof(char));
	strncpy(result, input + start, length);
	
	/* Normal function termination */
	return result;
}


int 
is_numeric(const char* input) 
{
	int rv;
	int result;
	char* deb = (char*)NULL;
	regex_t regex;
	regmatch_t pmatch[3];         // Up to 3 sub-expressions
	
	rv = regcomp(&regex, NUMERIC_MASK, REG_EXTENDED | REG_ICASE | REG_NEWLINE);
	if (rv) {
		return 0;
	}

	/* printf("input '%s'\n", input); */
	deb = deblank(input);
	
	/* printf("deb '%s'\n", deb); */
	rv = regexec(&regex, deb, ARRAY_SIZE (pmatch), pmatch, 0);
	
	if (rv) {
		return 0;
	}
	
	result = (int)
		(strlen(deb) == (size_t)(pmatch[0].rm_eo - pmatch[0].rm_so));
	
	/* Normal function termination */
	return result; 
}

size_t 
split(const char* text, const char* sep, char*** fields) 
{
	char*  buf    = (char*)NULL;
	char*  token  = (char*)NULL;
	char**  work  = (char**)NULL;
	size_t result = 0;
	size_t n_field = 0;
	
	buf = (char*)calloc(strlen(text) + 1, sizeof(char));
	strcpy(buf, text);
	
	token = strtok(buf, sep);
    /* TODO if separator not found, leave */
    if (!token) {
		/* TODO report reading problem */
        return 0;
	}
	// printf("1st token '%s'\n", token);
	
	work = (char**)calloc(1024, sizeof(char*));

    /* TODO get all elements */
	while (token) {
		work[n_field] = 
			(char*)calloc(strlen(token) + 1, sizeof(char*));
		strcpy(work[n_field], token);
		
		n_field++;
		token = strtok(NULL, sep);
		// printf("token %ld '%s'\n", n_field, token);
	}

	result = n_field;
	
	free(buf);
	work = (char**)realloc(work, result * sizeof(char*));
	
	*fields = work;
	
	/* Normal function termination */
	return result;
}

int 
find_text(char* const* texts, size_t n_texts, const char* key) 
{
	size_t ind;
	
	/* if there's not where to find, return nothing was found */
	if ((NULL == texts) || (0 == n_texts)) {
		return -1;
	}
	
	/* if there's not what to find, return nothing was found */
	if ((NULL == texts) || (0 == n_texts)) {
		return -1;
	}
	
	for (ind = 0; ind < n_texts; ind++) {
		if (!strcmp(texts[ind], key)) {
			return ind;
		}
	}
	
	return -1;
}
