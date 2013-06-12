drop database medocs if exists;
drop table if exists CIS, CIS_CIP, COMPO;
drop table if exists BDM_CIP;
drop table if exists BDM_TRF;

create table CIS (cis VARCHAR(8), nom_court VARCHAR(100), forme VARCHAR(50), admin_mode VARCHAR(60), status VARCHAR(25), type_procedure VARCHAR(25), etat_commercial VARCHAR(15), code_document VARCHAR(10)) default CHARSET=utf8;

create table CIS_CIP (cis VARCHAR(8),cip7 VARCHAR(7), pres VARCHAR(50), status VARCHAR(25), declaration VARCHAR(50), date_declaration DATE, cip13 VARCHAR(13)) default CHARSET=utf8;

create table COMPO (cis VARCHAR(8), element VARCHAR(25), code_substance TINYINT, substance VARCHAR(50), dosage VARCHAR(9), ref_dosage VARCHAR(25), nature_composant VARCHAR(2), liaison TINYINT);

create table BDM_CIP (cip VARCHAR(13),cip7 VARCHAR(7),cip_ucd VARCHAR(13), nature VARCHAR(1), nom_court VARCHAR(50), indic_cond VARCHAR(2), debut_remb DATE,
fin_remb DATE, code_liste TINYINT, code_forme VARCHAR(10), code_cplt VARCHAR(10), cplt_forme VARCHAR(60), dosage_sa VARCHAR(17), unite_sa VARCHAR(17),
nb_unite VARCHAR(10), code_atc VARCHAR(10), classe_atc VARCHAR(77), code_eph VARCHAR(10), classe_eph VARCHAR(77), labo VARCHAR(30),
nom_long1 VARCHAR(114), nom_long2 VARCHAR(113) suivi VARCHAR(1), date_effet DATE, seuil_aler TINYINT, seuil_reje TINYINT, presc_rest VARCHAR(1),
exceptions VARCHAR(1), type VARCHAR(2), sexe TINYINT, interact TINYINT, pih VARCHAR(2), pecp VARCHAR(2));

create table BND_TRF (cip VARCHAR(13), nom_court VARCHAR(50), code_grp TINYINT, nom_grp VARCHAR(124), code_atc VARCHAR(10), classe_atc VARCHAR(77),
pfht TINYINT, ppttc TINYINT, trf TINYINT, dt_deb DATE, dt_fin DATE);

load data local infile 'CIS.csv' into table CIS fields terminated by ';' escaped by '\\' lines terminated by '\n' (cis, nom_court, forme, admin_mode, status, type_procedure, etat_commercial, code_document);

load data local infile 'CIS_CIP.csv' into table CIS_CIP fields terminated by ';' escaped by '\\' lines terminated by '\n' (cis, cip7, pres, status, declaration, date_declaration, cip13);

load data local infile 'COMPO.csv' into table COMPO fields terminated by ';' escaped by '\\' lines terminated by '\n' (cis, element, code_substance, substance, dosage, ref_dosage, nature_composant, liaison);

load data local infile 'BDM_CIP.csv' into table BDM_CIP fields terminated by ';' escaped by '\\' lines terminated by '\n' (cip, cip7, cip_ucd nature,
nom_court, indic_cond, debut_remb, fin_remb, code_liste, code_forme, code_cplt, cplt_forme, dosage_sa, unite_sa, nb_unite, code_atc, classe_atc,
code_eph, classe_eph, labo, nom_long1, nom_long2, suivi, date_effet, seuil_aler, seuil_reje, presc_rest, exceptions, type, sexe, interact, pih, pecp);

load data local infile 'BDM_TRF.csv' into table BDM_TRF fields terminated by ';' escaped by '\\' lines terminated by '\n' (cip, nom_court, code_grp,
nom_grp, code_atc, classe_atc pfht, ppttc, trf, dt_deb, dt_fin);


create index idx_cis on CIS_CIP (cis);
create index idx_cis on CIS (cis);
create index idx_cis on COMPO (cis);
