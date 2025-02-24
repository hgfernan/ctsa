BEGIN TRANSACTION;
DROP TABLE IF EXISTS "datafiles";
CREATE TABLE IF NOT EXISTS "datafiles" (
	"datafile_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"from_name"	TEXT NOT NULL,
	"total_recs"	INTEGER NOT NULL,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("datafile_id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "argumentlims";
CREATE TABLE IF NOT EXISTS "argumentlims" (
	"argumentlim_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"extreme_min"	TEXT NOT NULL,
	"extreme_max"	TEXT NOT NULL,
	"created_min"	TEXT NOT NULL,
	"created_max"	TEXT NOT NULL,
	"model_id"	INTEGER NOT NULL,
	PRIMARY KEY("argumentlim_id" AUTOINCREMENT),
	FOREIGN KEY("model_id") REFERENCES "models"("model_id")
);
DROP TABLE IF EXISTS "codes";
CREATE TABLE IF NOT EXISTS "codes" (
	"code_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"filename"	TEXT NOT NULL,
	"datafile_id"	INTEGER NOT NULL,
	"param_id"	INTEGER NOT NULL,
	"template_id"	INTEGER NOT NULL,
	FOREIGN KEY("param_id") REFERENCES "params"("param_id"),
	FOREIGN KEY("template_id") REFERENCES "templates"("template_id"),
	PRIMARY KEY("code_id" AUTOINCREMENT),
	FOREIGN KEY("datafile_id") REFERENCES "datafiles"("datafile_id")
);
DROP TABLE IF EXISTS "execs";
CREATE TABLE IF NOT EXISTS "execs" (
	"exec_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"code_id"	INTEGER NOT NULL,
	"sys_desc"	TEXT NOT NULL,
	"exit_code"	INTEGER NOT NULL,
	"elapsed_time"	NUMERIC NOT NULL,
	"process_time"	NUMERIC NOT NULL,
	"value"	TEXT NOT NULL,
	PRIMARY KEY("exec_id" AUTOINCREMENT),
	FOREIGN KEY("code_id") REFERENCES "codes"("code_id")
);
DROP TABLE IF EXISTS "tests";
CREATE TABLE IF NOT EXISTS "tests" (
	"test_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"left_exec_id"	INTEGER NOT NULL,
	"right_exec_id"	INTEGER NOT NULL,
	"tolerance"	NUMERIC NOT NULL,
	"value"	TEXT NOT NULL,
	FOREIGN KEY("left_exec_id") REFERENCES "execs"("exec_id"),
	FOREIGN KEY("right_exec_id") REFERENCES "execs"("exec_id"),
	PRIMARY KEY("test_id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "models";
CREATE TABLE IF NOT EXISTS "models" (
	"model_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"name"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("model_id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "libraries";
CREATE TABLE IF NOT EXISTS "libraries" (
	"library_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"name"	TEXT NOT NULL,
	"version"	TEXT NOT NULL,
	PRIMARY KEY("library_id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "capabilities";
CREATE TABLE IF NOT EXISTS "capabilities" (
	"capability_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"model_id"	INTEGER NOT NULL,
	"library_id"	INTEGER NOT NULL,
	PRIMARY KEY("capability_id" AUTOINCREMENT),
	FOREIGN KEY("model_id") REFERENCES "models"("model_id"),
	FOREIGN KEY("library_id") REFERENCES "libraries"("library_id")
);
DROP TABLE IF EXISTS "arguments";
CREATE TABLE IF NOT EXISTS "arguments" (
	"argument_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"description"	TEXT NOT NULL,
	"model_id"	INTEGER NOT NULL,
	"value"	TEXT NOT NULL,
	FOREIGN KEY("model_id") REFERENCES "models"("model_id"),
	PRIMARY KEY("argument_id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "templates";
CREATE TABLE IF NOT EXISTS "templates" (
	"template_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"description"	TEXT NOT NULL,
	"text"	TEXT NOT NULL,
	"capability_id"	INTEGER NOT NULL,
	PRIMARY KEY("template_id" AUTOINCREMENT),
	FOREIGN KEY("capability_id") REFERENCES "capabilities"("capability_id")
);
DROP TABLE IF EXISTS "params";
CREATE TABLE IF NOT EXISTS "params" (
	"param_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"description"	TEXT NOT NULL,
	"value"	TEXT NOT NULL,
	"argument_id"	INTEGER NOT NULL,
	"capability_id"	INTEGER NOT NULL,
	"template_id"	INTEGER NOT NULL,
	FOREIGN KEY("capability_id") REFERENCES "capabilities"("capability_id"),
	FOREIGN KEY("template_id") REFERENCES "templates"("template_id"),
	PRIMARY KEY("param_id" AUTOINCREMENT),
	FOREIGN KEY("argument_id") REFERENCES "arguments"("argument_id")
);
INSERT INTO "models" ("model_id","timestamp","name","description") VALUES (1,'2025-02-24 15:37:02','AR','Autoregressive model'),
 (2,'2025-02-24 15:38:19','ARIMA','Autoregressive integrated moving average model'),
 (3,'2025-02-24 15:39:50','SARIMA','Seasonal autoregressive integrated moving average model'),
 (4,'2025-02-24 15:42:17','ARMA','Autoregressive moving average model'),
 (5,'2025-02-24 15:45:24','SARIMAX','Seasonal autoregressive integrated moving Average plus exogenous variables');
INSERT INTO "libraries" ("library_id","timestamp","name","version") VALUES (1,'2025-02-24 16:01:10','ctsa','0.1.0'),
 (2,'2025-02-24 16:02:45','forecast','8.23.0'),
 (3,'2025-02-24 16:06:33','pmdarima','2.0.4'),
 (4,'2025-02-24 16:07:37','statsmodels','0.14.4');
INSERT INTO "capabilities" ("capability_id","timestamp","model_id","library_id") VALUES (1,'2025-02-24 16:31:21',1,1);
INSERT INTO "arguments" ("argument_id","timestamp","description","model_id","value") VALUES (1,'2025-02-24 17:22:45','argument_ar_0001.json',1,'{ "parameters": { "init": { "L": 5, "n_rows": 10, "method": 0 } } }');
INSERT INTO "templates" ("template_id","timestamp","description","text","capability_id") VALUES (1,'2025-02-24 16:54:43','ctsa_ar_templ1.c','TO BE DEFINED',1);
INSERT INTO "params" ("param_id","timestamp","description","value","argument_id","capability_id","template_id") VALUES (1,'2025-02-24 18:26:26','param_ar_0001.json','{ "parameters": { "init": { "L": 5, "n_rows": 10, "method": 0 } } }',1,1,1);
COMMIT;
