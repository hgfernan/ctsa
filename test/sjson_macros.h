/**
 * Simple macros to present JSON data using a buffer string 
 * Created on Thu Feb  6 17:14:49 2025
 * 
 * @author: hilton
 * 
 */
 
#if !defined(SJSON_MACROS_H) 
#define SJSON_MACROS_H

#include <stdio.h>   /* sprintf() */
#include <string.h>  /* strcat() */
#include <stdbool.h> /* bool, false, true */

#define SJSON_MACROS_VARS \
int _sjm_depth = -1;\
bool _sjm_has_sibling[128] = {false};\
char _sjm_prefix[128] = "";\
char* _sjm_pbuf = (char*)NULL;

#define SJM_OPEN_ALL(buf) {\
	strcat(buf, "{\n");\
	_sjm_depth++;\
	strcat(_sjm_prefix, "\t");\
	_sjm_pbuf = buf;\
}

#define SJM_CLOSE_ALL(buf) {\
	strcat(buf, "\n}\n");\
	_sjm_depth = -1;\
	_sjm_prefix[0] = '\0';\
}

#define SJM_OPEN_STRUCT(name, buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, ",\n");\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s\"%s\": {\n", _sjm_prefix, name);\
	_sjm_has_sibling[_sjm_depth] = true;\
	_sjm_depth++;\
	strcat(_sjm_prefix, "\t");\
}

#define SJM_CLOSE_STRUCT(buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, "\n");\
	_sjm_has_sibling[_sjm_depth] = false;\
	_sjm_prefix[_sjm_depth] = '\0';\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s}", _sjm_prefix);\
	_sjm_depth--;\
}

#define SJM_ADD_PAIR_STR(key, value, buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, ",\n");\
	_sjm_has_sibling[_sjm_depth] = true;\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s\"%s\": \"%s\"", _sjm_prefix, key, value);\
}

#define SJM_ADD_PAIR_INT(key, value, buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, ",\n");\
	_sjm_has_sibling[_sjm_depth] = true;\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s\"%s\": %d", _sjm_prefix, key, value);\
}

#define SJM_ADD_PAIR_UINT(key, value, buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, ",\n");\
	_sjm_has_sibling[_sjm_depth] = true;\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s\"%s\": %lu", _sjm_prefix, key, value);\
}

#define SJM_ADD_PAIR_DBL(key, value, buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, ",\n");\
	_sjm_has_sibling[_sjm_depth] = true;\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s\"%s\": %g", _sjm_prefix, key, value);\
}

#define SJM_ADD_PAIR_BOOL(key, value, buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, ",\n");\
	_sjm_has_sibling[_sjm_depth] = true;\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s\"%s\": %s", _sjm_prefix, key,\
		value? "true", "false");\
}

#define SJM_ADD_PAIR_CHAR(key, value, buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, ",\n");\
	_sjm_has_sibling[_sjm_depth] = true;\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s\"%s\": '%c'", _sjm_prefix, key, value);\
}

#define SJM_OPEN_ARRAY(name, buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, ",\n");\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s\"%s\": [\n", _sjm_prefix, name);\
	_sjm_has_sibling[_sjm_depth] = true;\
	_sjm_depth++;\
	strcat(_sjm_prefix, "\t");\
}

#define SJM_CLOSE_ARRAY(buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, "\n");\
	_sjm_has_sibling[_sjm_depth] = false;\
	_sjm_prefix[_sjm_depth] = '\0';\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s]", _sjm_prefix);\
	_sjm_depth--;\
}

#define SJM_ADD_ELMT_STR(value, buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, ",\n");\
	_sjm_has_sibling[_sjm_depth] = true;\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s\"%s\"", _sjm_prefix, value);\
}

#define SJM_ADD_ELMT_UINT(value, buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, ",\n");\
	_sjm_has_sibling[_sjm_depth] = true;\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s%lu", _sjm_prefix, value);\
}

#define SJM_ADD_ELMT_DBL(value, buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, ",\n");\
	_sjm_has_sibling[_sjm_depth] = true;\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s%g", _sjm_prefix, value);\
}

#define SJM_ADD_ELMT_INT(value, buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, ",\n");\
	_sjm_has_sibling[_sjm_depth] = true;\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s%d", _sjm_prefix, value);\
}

#define SJM_ADD_ELMT_BOOL(value, buf) {\
	if (_sjm_has_sibling[_sjm_depth]) strcat(buf, ",\n");\
	_sjm_has_sibling[_sjm_depth] = true;\
	_sjm_pbuf = buf + strlen(buf);\
	sprintf(_sjm_pbuf, "%s%s", _sjm_prefix, value? "true", "false");\
}

#endif /* !defined(SJSON_MACROS_H) */
