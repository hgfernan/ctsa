/**
 * Header for a tiny lib of functions to manipulate strings C misses
 * Created on Sun Dec 29 21:34:24 2024
 * 
 * @author: hilton
 * 
 **/

#if !defined(__TINY_LIB)
#define __TINY_LIB

#define NUMERIC_MASK "[+-]?[0-9]\\.?[0-9]*(e[+-]?[0-9]+)?"

#define ARRAY_SIZE(x)  ( sizeof(x) / sizeof(x[0]) )

 
char*  deblank(const char* input); 
int    is_numeric(const char* input);
size_t split(const char* text, const char* sep, char*** fields);
int    find_text(char* const* texts, size_t n_texts, const char* key); 

#endif /* !defined(__TINY_LIB) */
