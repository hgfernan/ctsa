BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "datafiles" (
	"datafile_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	"filename"	TEXT NOT NULL,
	"total_recs"	INTEGER NOT NULL,
	"description"	TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "params" (
	"param_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"model"		TEXT NOT NULL,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	"value"		TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "paramlims" (
	"paramlim_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"model"		TEXT NOT NULL,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	"extreme_min"	TEXT NOT NULL,
	"extreme_max"	TEXT NOT NULL,
	"created_min"	TEXT NOT NULL,
	"created_max" 	TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "codes" (
	"code_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	"language"	TEXT NOT NULL,
	"datafile_id"	INTEGER NOT NULL,
	"param_id"	INTEGER NOT NULL,
	FOREIGN KEY (datafile_id) REFERENCES datafiles(datafile_id),	
	FOREIGN KEY (param_id) REFERENCES params(param_id)
);

CREATE TABLE IF NOT EXISTS "execs" (
	"exec_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	"code_id"	INTEGER NOT NULL,
	"sys_desc"	TEXT NOT NULL,
	"elapsed_time"	NUMERIC NOT NULL,
	"process_time"	NUMERIC NOT NULL,
	"value"	    TEXT NOT NULL,
	FOREIGN KEY (code_id) REFERENCES codes(code_id)
);

CREATE TABLE IF NOT EXISTS "tests" (
	"test_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	"left_exec_id"	INTEGER NOT NULL,
	"right_exec_id"	INTEGER NOT NULL,
	"tolerance"	NUMERIC NOT NULL,	
	"value"	    TEXT NOT NULL,
	FOREIGN KEY (left_exec_id) REFERENCES execs(exec_id),	
	FOREIGN KEY (right_exec_id) REFERENCES execs(exec_id)
);

CREATE TABLE IF NOT EXISTS "models" (
	"model_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	"description"	TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "libraries" (
	"library_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	"description"	TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "capabilities" (
	"capability_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	'model_id' INTEGER NOT NULL,
	'library_id' INTEGER NOT NULL,
	FOREIGN KEY (model_id) REFERENCES models(model_id),	
	FOREIGN KEY (library_id) REFERENCES libraries(library_id)
);

CREATE TABLE IF NOT EXISTS "arguments" (
	"argument_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"timestamp"		TEXT NOT NULL DEFAULT 'date()',
	"description"	TEXT NOT NULL,
	'model_id'		INTEGER NOT NULL,
	"value"			TEXT NOT NULL, 
	FOREIGN KEY (model_id) REFERENCES models(model_id)
);
CREATE TABLE IF NOT EXISTS "templates" (
	"template_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	"description"	TEXT NOT NULL,
	"text"		TEXT NOT NULL,
	"capability_id"	TEXT NOT NULL,
	FOREIGN KEY (capability_id) REFERENCES capabilities(capability_id)
);


CREATE TABLE IF NOT EXISTS "parameters" (
	"parameter_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"timestamp"		TEXT NOT NULL DEFAULT 'date()',
	"value"			TEXT NOT NULL,
	"argument_id"	TEXT NOT NULL,
	"capability_id"	TEXT NOT NULL,
	FOREIGN KEY (argument_id) REFERENCES arguments(argument_id),	
	FOREIGN KEY (capability_id) REFERENCES capabilities(capability_id)
);

COMMIT;
