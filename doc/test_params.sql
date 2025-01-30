BEGIN TRANSACTION;
DROP TABLE datafiles;
CREATE TABLE IF NOT EXISTS "datafiles" (
	"datafile_id"	INTEGER NOT NULL UNIQUE,
	"timestamp"	    TEXT NOT NULL DEFAULT 'date()',
	"filename"		TEXT NOT NULL,
	"total_recs"	INTEGER NOT NULL,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("datafile_id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "params" (
	"param_id"	INTEGER NOT NULL UNIQUE,
	"algorithm"	TEXT NOT NULL,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	"value"		TEXT NOT NULL,
	PRIMARY KEY("param_id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "code" (
	"code_id"	INTEGER NOT NULL UNIQUE,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	"language"	TEXT NOT NULL,
	"datafile_id"	INTEGER NOT NULL,
	"param_id"	INTEGER NOT NULL,
	FOREIGN KEY (datafile_id) REFERENCES datafiles(datafile_id),	
	FOREIGN KEY (param_id) REFERENCES params(param_id),	
	PRIMARY KEY("detail_id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "execs" (
	"exec_id"	INTEGER NOT NULL UNIQUE,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	"code_id"	INTEGER NOT NULL,
	"sys_desc"	TEXT NOT NULL,
	"duration"	NUMERIC NOT NULL,
	"value"	    TEXT NOT NULL,
	FOREIGN KEY (code_id) REFERENCES codes(code_id),	
	PRIMARY KEY("exec_id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "tests" (
	"test_id"	INTEGER NOT NULL UNIQUE,
	"timestamp"	TEXT NOT NULL DEFAULT 'date()',
	"left_exec_id"	INTEGER NOT NULL,
	"right_exec_id"	INTEGER NOT NULL,
	"value"	    TEXT NOT NULL,
	FOREIGN KEY (left_exec_id) REFERENCES execs(exec_id),	
	FOREIGN KEY (right_exec_id) REFERENCES execs(exec_id),	
	PRIMARY KEY("detail_id" AUTOINCREMENT)
);

COMMIT;
