create table CIS (cis VARCHAR(8), nom_court VARCHAR(100), forme VARCHAR(50), admin_mode VARCHAR(60), status VARCHAR(25), type_procedure VARCHAR(25), etat_commercial VARCHAR(15), code_document VARCHAR(10), dummy VARCHAR(1));

create table CIS_CIP (cis VARCHAR(8),cip7 VARCHAR(7), pres VARCHAR(50), status VARCHAR(25), declaration VARCHAR(50), date_declaration DATE, cip13 VARCHAR(13));

create table COMPO (cis VARCHAR(8), element VARCHAR(25), code_substance TINYINT, substance VARCHAR(50), dosage VARCHAR(9), ref_dosage VARCHAR(25), nature_composant VARCHAR(2), liaison TINYINT, dummy VARCHAR(1));

.separator \t

.import 'CIS.csv' CIS

.import 'CIS_CIP.csv' CIS_CIP

.import 'COMPO.csv' COMPO

create index cis_idx on CIS (cis);
create index cip_idx ON CIS_CIP (cis);
create index compo_idx on COMPO (cis);