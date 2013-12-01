drop table if exists CIS;
drop table if exists CIS_CIP;
-- drop table if exists COMPO;
drop table if exists BDM_CIP;
drop table if exists BDM_TFR;
drop table if exists BDM_GG;
drop table if exists BDM_TG;
drop table if exists BDM_PRIX;

.echo OFF

create table CIS (cis VARCHAR(8), nom_court VARCHAR(100), forme VARCHAR(50), admin_mode VARCHAR(60), status VARCHAR(25), type_procedure VARCHAR(25), etat_commercial VARCHAR(15), code_document VARCHAR(10), dummy VARCHAR(1));

create table CIS_CIP (cis VARCHAR(8),cip7 VARCHAR(7), pres VARCHAR(50), status VARCHAR(25), declaration VARCHAR(50), date_declaration DATE, cip13 VARCHAR(13));

-- create table COMPO (cis VARCHAR(8), element VARCHAR(25), code_substance TINYINT, substance VARCHAR(50), dosage VARCHAR(9), ref_dosage VARCHAR(25), nature_composant VARCHAR(2), liaison TINYINT, dummy VARCHAR(1));

create table BDM_CIP (cip VARCHAR(13),cip7 VARCHAR(7),cip_ucd VARCHAR(13), nature VARCHAR(1), nom_court VARCHAR(50), indic_cond VARCHAR(2), debut_remb DATE,
fin_remb DATE, code_liste TINYINT, code_forme VARCHAR(10), forme VARCHAR(40), code_cplt VARCHAR(10), cplt_forme VARCHAR(60), dosage_sa VARCHAR(17), unite_sa VARCHAR(17),
nb_unite VARCHAR(10), code_atc VARCHAR(10), classe_atc VARCHAR(77), code_eph VARCHAR(10), classe_eph VARCHAR(77), labo VARCHAR(30),
nom_long1 VARCHAR(114), nom_long2 VARCHAR(113), suivi VARCHAR(1), date_effet DATE, seuil_aler TINYINT, seuil_reje TINYINT, presc_rest VARCHAR(1),
exceptions VARCHAR(1), type VARCHAR(2), sexe TINYINT, interact TINYINT, pih VARCHAR(2), pecp VARCHAR(2));

create table BDM_TFR (cip VARCHAR(13), nom_court VARCHAR(50), code_grp TINYINT, nom_grp VARCHAR(124), code_atc VARCHAR(10), classe_atc VARCHAR(77),
pfht TINYINT, ppttc TINYINT, trf TINYINT, dt_deb DATE, dt_fin DATE);

create table BDM_GG (cip VARCHAR(13), nom_court VARCHAR(50), code_grp TINYINT, nom_grp VARCHAR(124), code_atc VARCHAR(10), classe_atc VARCHAR(77),
dt_deb_afs DATE, dt_fin_afs DATE, debut_remb DATE, fin_remb DATE);

create table BDM_TG (cip VARCHAR(13), nom_court VARCHAR(50), dt_effet DATE, gen_ind VARCHAR(1), code_grp TINYINT, nom_grp VARCHAR(124), 
code_atc VARCHAR(10), classe_atc VARCHAR(77));

create table BDM_PRIX (cip VARCHAR(13), CIP7 VARCHAR(7), prix_f TINYINT, prix_e TINYINT, fab_ht_e TINYINT, prix_ht_e TINYINT, taux VARCHAR(3), date_appli DATE, date_jo DATE);

.separator \t

.import 'CIS.csv' CIS

.import 'CIS_CIP.csv' CIS_CIP

-- .import 'COMPO.csv' COMPO

.import 'BDM_CIP.csv' BDM_CIP

.import 'BDM_TFR.csv' BDM_TFR

.import 'BDM_GG.csv' BDM_GG

.import 'BDM_TG.csv' BDM_TG

.import 'BDM_PRIX.csv' BDM_PRIX

create index cis_idx on CIS (cis);
create index cip_idx ON CIS_CIP (cis);
-- create index compo_idx on COMPO (cis);
create index bdm_cip_idx on BDM_CIP (cip);
create index bdm_tfr_idx on BDM_TFR (cip);
create index bdm_gg_idx on BDM_GG (cip);
create index bdm_tg_idx on BDM_TG (cip);
create index bdm_prix_idx on BDM_PRIX (cip);