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
	FOREIGN KEY("model_id") REFERENCES "models"("model_id"),
	PRIMARY KEY("argumentlim_id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "codes";
CREATE TABLE IF NOT EXISTS "codes" (
	"code_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"filename"	TEXT NOT NULL,
	"datafile_id"	INTEGER NOT NULL,
	"param_id"	INTEGER NOT NULL,
	"template_id"	INTEGER NOT NULL,
	PRIMARY KEY("code_id" AUTOINCREMENT),
	FOREIGN KEY("datafile_id") REFERENCES "datafiles"("datafile_id"),
	FOREIGN KEY("template_id") REFERENCES "templates"("template_id"),
	FOREIGN KEY("param_id") REFERENCES "params"("param_id")
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
	FOREIGN KEY("code_id") REFERENCES "codes"("code_id"),
	PRIMARY KEY("exec_id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "tests";
CREATE TABLE IF NOT EXISTS "tests" (
	"test_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"left_exec_id"	INTEGER NOT NULL,
	"right_exec_id"	INTEGER NOT NULL,
	"tolerance"	NUMERIC NOT NULL,
	"value"	TEXT NOT NULL,
	PRIMARY KEY("test_id" AUTOINCREMENT),
	FOREIGN KEY("left_exec_id") REFERENCES "execs"("exec_id"),
	FOREIGN KEY("right_exec_id") REFERENCES "execs"("exec_id")
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
	PRIMARY KEY("argument_id" AUTOINCREMENT),
	FOREIGN KEY("model_id") REFERENCES "models"("model_id")
);
DROP TABLE IF EXISTS "templates";
CREATE TABLE IF NOT EXISTS "templates" (
	"template_id"	INTEGER,
	"timestamp"	TEXT NOT NULL DEFAULT (datetime()),
	"description"	TEXT NOT NULL,
	"text"	TEXT NOT NULL,
	"capability_id"	INTEGER NOT NULL,
	FOREIGN KEY("capability_id") REFERENCES "capabilities"("capability_id"),
	PRIMARY KEY("template_id" AUTOINCREMENT)
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
	PRIMARY KEY("param_id" AUTOINCREMENT),
	FOREIGN KEY("capability_id") REFERENCES "capabilities"("capability_id"),
	FOREIGN KEY("template_id") REFERENCES "templates"("template_id"),
	FOREIGN KEY("argument_id") REFERENCES "arguments"("argument_id")
);
INSERT INTO "datafiles" ("datafile_id","timestamp","from_name","total_recs","description") VALUES (297,'2025-02-24 22:41:28','../data/1m-20241125_001625-20241125_165625.csv',1000,'../testdata/0001.csv'),
 (298,'2025-02-24 22:41:28','../data/1m-20241125_001625-20241125_165625.txt',1000,'../testdata/0002.csv'),
 (299,'2025-02-24 22:41:28','../data/dowjones.dat',78,'../testdata/0003.csv'),
 (300,'2025-02-24 22:41:28','../data/e1m.dat',76,'../testdata/0004.csv'),
 (301,'2025-02-24 22:41:28','../data/e6.dat',107,'../testdata/0005.csv'),
 (302,'2025-02-24 22:41:28','../data/e6m.dat',107,'../testdata/0006.csv'),
 (303,'2025-02-24 22:41:29','../data/eusm.txt',300,'../testdata/0007.csv'),
 (304,'2025-02-24 22:41:30','../data/huron.dat',98,'../testdata/0008.csv'),
 (305,'2025-02-24 22:41:31','../data/islm.dat',112,'../testdata/0009.csv'),
 (306,'2025-02-24 22:41:31','../data/itdaily.txt',51,'../testdata/0010.csv'),
 (307,'2025-02-24 22:41:31','../data/lynx.txt',114,'../testdata/0011.csv'),
 (308,'2025-02-24 22:41:31','../data/ohlc_min.csv',10,'../testdata/0012.csv'),
 (309,'2025-02-24 22:41:31','../data/ohlc_min.txt',10,'../testdata/0013.csv'),
 (310,'2025-02-24 22:41:31','../data/seriesA.txt',197,'../testdata/0014.csv'),
 (311,'2025-02-24 22:41:31','../data/seriesB.txt',369,'../testdata/0015.csv'),
 (312,'2025-02-24 22:41:31','../data/seriesC.txt',226,'../testdata/0016.csv'),
 (313,'2025-02-24 22:41:32','../data/seriesD.txt',310,'../testdata/0017.csv'),
 (314,'2025-02-24 22:41:32','../data/seriesF.txt',70,'../testdata/0018.csv'),
 (315,'2025-02-24 22:41:32','../data/seriesG.txt',144,'../testdata/0019.csv'),
 (316,'2025-02-24 22:41:32','../data/signal.txt',256,'../testdata/0020.csv'),
 (317,'2025-02-24 22:41:32','../data/sine.txt',1000,'../testdata/0021.csv'),
 (318,'2025-02-24 22:41:32','../data/sp500_transf.dat',10136,'../testdata/0022.csv'),
 (319,'2025-02-24 22:41:32','../data/sunspots.txt',235,'../testdata/0023.csv'),
 (320,'2025-02-24 22:41:32','../data/taylor.txt',4032,'../testdata/0024.csv'),
 (321,'2025-02-24 22:41:32','../data/us-daily.csv',43,'../testdata/0025.csv'),
 (322,'2025-02-24 22:41:32','../data/usdaily.txt',43,'../testdata/0026.csv'),
 (323,'2025-02-24 22:41:32','../data/wineind.txt',176,'../testdata/0027.csv');
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
