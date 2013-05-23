drop database medocs if exists;
drop table if exists CIS, CIS_CIP, COMPO;

create table CIS (cis VARCHAR(8), nom_court VARCHAR(100), forme VARCHAR(50), admin_mode VARCHAR(60), status VARCHAR(25), type_procedure VARCHAR(25), etat_commercial VARCHAR(15), code_document VARCHAR(10)) default CHARSET=utf8;

create table CIS_CIP (cis VARCHAR(8),cip7 VARCHAR(7), pres VARCHAR(50), status VARCHAR(25), declaration VARCHAR(50), date_declaration DATE, cip13 VARCHAR(13)) default CHARSET=utf8;

create table COMPO (cis VARCHAR(8), element VARCHAR(25), code_substance TINYINT, substance VARCHAR(50), dosage VARCHAR(9), ref_dosage VARCHAR(25), nature_composant VARCHAR(2), liaison TINYINT);

load data local infile 'CIS.csv' into table CIS fields terminated by ';' escaped by '\\' lines terminated by '\n' (cis, nom_court, forme, admin_mode, status, type_procedure, etat_commercial, code_document);

load data local infile 'CIS_CIP.csv' into table CIS_CIP fields terminated by ';' escaped by '\\' lines terminated by '\n' (cis, cip7, pres, status, declaration, date_declaration, cip13);

load data local infile 'COMPO.csv' into table COMPO fields terminated by ';' escaped by '\\' lines terminated by '\n' (cis, element, code_substance, substance, dosage, ref_dosage, nature_composant, liaison);

create index idx_cis on CIS_CIP (cis);
create index idx_cis on CIS (cis);
create index idx_cis on COMPO (cis);
