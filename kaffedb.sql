BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "kaffegård" (
	"kaffegårdID"	INTEGER,
	"navn"	TEXT,
	"region"	TEXT,
	"land"	TEXT,
	"m.o.h."	INTEGER,
	PRIMARY KEY("kaffegårdID")
);
CREATE TABLE IF NOT EXISTS "foredlingsmetode" (
	"foredlingsmetodeID"	INTEGER,
	"navn"	TEXT,
	"beskrivelse"	TEXT,
		PRIMARY KEY("foredlingsmetodeID")
);
CREATE TABLE IF NOT EXISTS "kaffebønne" (
	"kaffebønneID"	INTEGER,
	"navn"	TEXT,
	"art"	TEXT,
	PRIMARY KEY("kaffebønneID"),
	CHECK(art = "arabica" OR art = "robusta" OR art = "liberica" OR art = "robusta")
);

CREATE TABLE IF NOT EXISTS "kaffebønneDyrkesPåGård" (
	"kaffegårdID"	INTEGER,
	"kaffebønneID"	INTEGER,
	PRIMARY KEY("kaffegårdID","kaffebønneID"),
	FOREIGN KEY("kaffegårdID") REFERENCES "kaffebønneDyrkesPåGård"("kaffegårdID"),
	FOREIGN KEY("kaffebønneID") REFERENCES "kaffebønne"("kaffebønneID")
);

CREATE TABLE IF NOT EXISTS "kaffepartiBestårAv" (
	"kaffepartiID"	INTEGER,
	"kaffebønneID"	INTEGER,
	PRIMARY KEY("kaffepartiID","kaffebønneID"),
	FOREIGN KEY("kaffepartiID") REFERENCES "kaffeparti"("kaffepartiID"),
	FOREIGN KEY("kaffebønneID") REFERENCES "kaffebønne"("kaffebønneID")

);
CREATE TABLE IF NOT EXISTS "kaffesmaking" (
	"brukerID"	INTEGER,
	"kaffeID"	INTEGER,
	"smaksnotater"	TEXT,
	"poengsum"	INTEGER,
	"smaksdato"	TEXT,
	PRIMARY KEY("kaffeID","brukerID"),
	FOREIGN KEY("kaffeID") REFERENCES "ferdigbrentKaffe"("kaffeID"),
	FOREIGN KEY("brukerID") REFERENCES "bruker"("brukerID"),
	CHECK(poengsum > -1 and poengsum < 11)
);
CREATE TABLE IF NOT EXISTS "bruker" (
	"brukerID"	INTEGER,
	"epostadresse"	TEXT UNIQUE,
	"navn"	TEXT,
	"passord"	TEXT,
	PRIMARY KEY("brukerID")
);
CREATE TABLE IF NOT EXISTS "ferdigbrentKaffe" (
	"kaffeID"	INTEGER,
	"navn"	TEXT,
	"kaffebrennerinavn"	TEXT,
	"brenningsgrad"	INTEGER,
	"brennedato"	TEXT,
	"beskrivelse"	TEXT,
	"kgpris_nok"	REAL,
	"kaffepartiID"	INTEGER,
	"kaffebønneID"	INTEGER,
	UNIQUE("navn","kaffebrennerinavn"),
	PRIMARY KEY("kaffeID"),
	FOREIGN KEY("kaffepartiID") REFERENCES "kaffeparti",
	FOREIGN KEY("kaffebønneID") REFERENCES "kaffebønne"("kaffebønneID"),
	CHECK(brenningsgrad > 0 AND brenningsgrad < 4)
);
CREATE TABLE IF NOT EXISTS "kaffeparti" (
	"kaffepartiID"	INTEGER,
	"innhøstingsår"	TEXT,
	"kgpris_usd"	REAL,
	"foredlingsmetodeID"	INTEGER,
	"kaffegårdID"	INTEGER,
	PRIMARY KEY("kaffepartiID"),
	FOREIGN KEY("kaffegårdID") REFERENCES "kaffegård"("kaffegårdID"),
	FOREIGN KEY("foredlingsmetodeID") REFERENCES "foredlingsmetode"("foredlingsmetodeID")
);
COMMIT;
