#!/usr/bin/env python2.7
# -*-coding:utf-8 -*-

# --------------------------------------------------------------------- #
#																		#
# Ré-éciture du script de traitement des bases de médicaments en 		#
# python																#
#																		#
#-----------------------------------------------------------------------#


from plistlib import *
import os
import requests
import zipfile
import sys
import subprocess
import csv
from dbfpy import dbf
import sqlite3
import shutil

def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def downloadFile(url):
	local_filename = url.split('/')[-1]
	file = requests.get(url, stream=True)
	with open(local_filename, 'wb') as f:
		for chunk in file.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				f.flush()
	return local_filename


def writeMedsPlist():
	myArray = readPlist(os.path.expanduser("/home/jfoucry/AFM/Meds.plist"))
	newDict = {}

	for aDict in myArray:
		key = aDict["cip7"]
		#print key
		newDict[key] = aDict

	#print newDict
	writePlist(newDict, os.path.expanduser("/home/jfoucry/AFM/newMeds.plist"))

def writeOnSTDERR(msg):
        sys.stderr.write(msg)

def convert_to_utf8(filename):
    # gather the encodings you think that the file may be
    # encoded inside a tuple
    encodings = ('iso-8859')
 
    # try to open the file and exit if some IOError occurs
    try:
        f = open(filename, 'r').read()
    except Exception:
        sys.exit(1)
 
    # now start iterating in our encodings tuple and try to
    # decode the file
    for enc in encodings:
        try:
            # try to decode the file with the first encoding
            # from the tuple.
            # if it succeeds then it will reach break, so we
            # will be out of the loop (something we want on
            # success).
            # the data variable will hold our decoded text
            data = f.decode(enc)
            break
        except Exception:
            # if the first encoding fail, then with the continue
            # keyword will start again with the second encoding
            # from the tuple an so on.... until it succeeds.
            # if for some reason it reaches the last encoding of
            # our tuple without success, then exit the program.
            if enc == encodings[-1]:
                sys.exit(1)
            continue
 
    # now get the absolute path of our filename and append .bak
    # to the end of it (for our backup file)
    fpath = os.path.abspath(filename)
    newfilename = fpath + '.bak'
    # and make our backup file with shutil
    shutil.copy(filename, newfilename)
 
    # and at last convert it to utf-8
    f = open(filename, 'w')
    try:
        f.write(data.encode('utf-8'))
    except Exception, e:
        print e
    finally:
        f.close()

# Download AMM file
# ammFile = downloadFile("http://agence-prd.ansm.sante.fr/php/ecodex/telecharger/fic_cis_cip.zip")
# secuFile = downloadFile("http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm/AFM.EXE")

# unzip AMM file
# fh = open(ammFile, 'rb')
# z = zipfile.ZipFile(fh)
# for name in z.namelist():
# 	outfile = open(name, 'wb')
# 	outfile.write('/tmp'+z.read(name))
# 	outfile.close
# fh.close

# if cmd_exists("unarj"):
#     cmd_string = ['unarj', 'e', secuFile]
#     try:
#         subprocess.check_call(cmd_string)
#     except OSError as e:
#         # logger.debug("Error in %s, exiting"% (cmd_string))
#         writeOnSTDERR("Error in %s. exiting" % (cmd_string))
#         sys.exit(1)

# if cmd_exists("dbf"):
#     for file in os.listdir('.'):
#         if file == "BDM_CIP.DBF":
#             try:
#                 db_cip = dbf.Dbf("BDM_CIP.DBF")
#             except OSError as e:
#                 writeOnSTDERR("Error is %s, exiting"% e.ValueError)
#         elif file == "BDM_TFR.DBF":
#             try:
#                 db_tfr = dbf.Dbf("BDM_TFR.DBF")
#             except OSError as e:
#                 writeOnSTDERR("Error is %s, exiting"% e.ValueError)
#         elif file == "BDM_GG.DBF":
#             try:
#                 db_gg = dbf.Dbf("BDM_GG.DBF")
#             except OSError as e:
#                 writeOnSTDERR("Error is %s, exiting"% e.ValueError)
#         elif file == "BDM_TG.DBF":
#             try:
#                 db_tg = dbf.Dbf("BDM_TG.DBF")
#             except OSError as e:
#                 writeOnSTDERR("Error in %s, exiting"% e.ValueError)
#         elif file == "BDM_PRIX.DBF":
#             try:
#                 db_prix = dbf.Dbf("BDM_PRIX.DBF")
#             except OSError as e:
#                 writeOnSTDERR("Error is %s, exiting"% e.ValueError)
# Create SQLite Database

con = sqlite3.connect(":memory:")
con = sqlite3.connect("meds.sqlite3")
con.text_factory = str
cursor = con.cursor()

# Create tables

cursor.execute('''
    create table CIS (cis VARCHAR(8), nom_court VARCHAR(100), forme VARCHAR(50), admin_mode VARCHAR(60), status VARCHAR(25), 
type_procedure VARCHAR(25), etat_commercial VARCHAR(15), code_document VARCHAR(10), dummy VARCHAR(1))
''')

cursor.execute('''
    create table CIS_CIP (cis VARCHAR(8),cip7 VARCHAR(7), pres VARCHAR(50), status VARCHAR(25), declaration VARCHAR(50), 
    date_declaration DATE, cip13 VARCHAR(13))
''')

# # BDM_CIP
# cursor.execute('''
#     create table BDM_CIP (cip VARCHAR(13),cip7 VARCHAR(7),cip_ucd VARCHAR(13), nature VARCHAR(1), nom_court VARCHAR(50), indic_cond VARCHAR(2), debut_remb DATE,
# fin_remb DATE, code_liste TINYINT, code_forme VARCHAR(10), forme VARCHAR(40), code_cplt VARCHAR(10), cplt_forme VARCHAR(60), dosage_sa VARCHAR(17), unite_sa VARCHAR(17),
# nb_unite VARCHAR(10), code_atc VARCHAR(10), classe_atc VARCHAR(77), code_eph VARCHAR(10), classe_eph VARCHAR(77), labo VARCHAR(30),
# nom_long1 VARCHAR(114), nom_long2 VARCHAR(113), suivi VARCHAR(1), date_effet DATE, seuil_aler TINYINT, seuil_reje TINYINT, presc_rest VARCHAR(1),
# exceptions VARCHAR(1), type VARCHAR(2), sexe TINYINT, interact TINYINT, pih VARCHAR(2), pecp VARCHAR(2))
# ''')

# # BDM_TFR
# cursor.execute('''
#     create table BDM_TFR (cip VARCHAR(13), nom_court VARCHAR(50), code_grp TINYINT, nom_grp VARCHAR(124), code_atc VARCHAR(10), classe_atc VARCHAR(77),
# pfht TINYINT, ppttc TINYINT, trf TINYINT, dt_deb DATE, dt_fin DATE)
# ''')

# # BDN_GG
# cursor.execute('''
#     create table BDM_GG (cip VARCHAR(13), nom_court VARCHAR(50), code_grp TINYINT, nom_grp VARCHAR(124), code_atc VARCHAR(10), classe_atc VARCHAR(77),
# dt_deb_afs DATE, dt_fin_afs DATE, debut_remb DATE, fin_remb DATE)
# ''')

# # BDM_TG
# cursor.execute('''
#     create table BDM_TG (cip VARCHAR(13), nom_court VARCHAR(50), dt_effet DATE, gen_ind VARCHAR(1), code_grp TINYINT, nom_grp VARCHAR(124), 
# code_atc VARCHAR(10), classe_atc VARCHAR(77))
# ''')

# # BDM_PRIX
# cursor.execute('''
#     create table BDM_PRIX (cip VARCHAR(13), CIP7 VARCHAR(7), prix_f TINYINT, prix_e TINYINT, fab_ht_f TINYINT, fab_ht_e TINYINT, taux VARCHAR(3), date_appli DATE, date_jo DATE)
# ''')
# con.commit()

# # insert into BDM_CIP
# print "Insert into BDM_CIP"
# for rec in db_cip:
#     cip        = rec["CIP"]
#     cip7       = rec["CIP7"]
#     cip_ucd    = rec["CIP_UCD"]
#     nature     = rec["NATURE"]
#     nom_court  = rec["NOM_COURT"]
#     indic_cond = rec["INDIC_COND"]
#     debut_remb = rec["DEBUT_REMB"]
#     fin_remb   = rec["FIN_REMB"]
#     code_liste = rec["CODE_LISTE"]
#     code_forme = rec["CODE_FORME"]
#     forme      = rec["FORME"]
#     code_cplt  = rec["CODE_CPLT"]
#     cplt_forme = rec["CPLT_FORME"]
#     dosage_sa  = rec["DOSAGE_SA"]
#     unite_sa   = rec["UNITE_SA"]
#     nb_unite   = rec["NB_UNITES"]
#     code_atc   = rec["CODE_ATC"]
#     classe_atc = rec["CLASSE_ATC"]
#     code_eph   = rec["CODE_EPH"]
#     classe_eph = rec["CLASSE_EPH"]
#     labo       = rec["LABO"]
#     nom_long1  = rec["NOM_LONG1"]
#     nom_long2  = rec["NOM_LONG2"]
#     suivi      = rec["SUIVI"]
#     date_effet = rec["DATE_EFFET"]
#     seuil_aler = rec["SEUIL_ALER"]
#     seuil_reje = rec["SEUIL_REJE"]
#     presc_rest = rec["PRESC_REST"]
#     exceptions = rec["EXCEPTIONS"]
#     type         = rec["TYPE"]
#     sexe       = rec["SEXE"]
#     interact   = rec["INTERACT"]
#     pih        = rec["PIH"]
#     pecp       = rec["PECP"]

#     cursor.execute('''
#         INSERT INTO BDM_CIP(cip,cip7,cip_ucd,nature,nom_court,indic_cond,debut_remb,fin_remb,code_liste,code_forme,forme,code_cplt,cplt_forme,dosage_sa,unite_sa,nb_unite,
#             code_atc,classe_atc,code_eph,classe_eph,labo,nom_long1,nom_long2,suivi,date_effet,seuil_aler,seuil_reje,presc_rest,exceptions,type,sexe,interact,pih,pecp)
#         VALUES(:cip,:cip7,:cip_ucd,:nature,:nom_court,:indic_cond,:debut_remb,:fin_remb,:code_liste,:code_forme,:forme,:code_cplt,:cplt_forme,:dosage_sa,:unite_sa,:nb_unite,
#             :code_atc,:classe_atc,:code_eph,:classe_eph,:labo,:nom_long1,:nom_long2,:suivi,:date_effet,:seuil_aler,:seuil_reje,:presc_rest,:exceptions,:type,:sexe,:interact,:pih,:pecp)''',
#         {'cip':cip,
#         'cip7':cip7,
#         'cip_ucd':cip_ucd,
#         'nature':nature,
#         'nom_court':nom_court,
#         'indic_cond':indic_cond,
#         'debut_remb':debut_remb,
#         'fin_remb':fin_remb,
#         'code_liste':code_liste,
#         'code_forme':code_forme,
#         'forme':forme,
#         'code_cplt':code_cplt,
#         'cplt_forme':cplt_forme,
#         'dosage_sa':dosage_sa,
#         'unite_sa':unite_sa,
#         'nb_unite':nb_unite,
#         'code_atc':code_atc,
#         'classe_atc':classe_atc,
#         'code_eph':code_eph,
#         'classe_eph':classe_eph,
#         'labo':labo,
#         'nom_long1':nom_long1,
#         'nom_long2':nom_long2,
#         'suivi':suivi,
#         'date_effet':date_effet,
#         'seuil_aler':seuil_aler,
#         'seuil_reje':seuil_reje,
#         'presc_rest':presc_rest,
#         'exceptions':exceptions,
#         'type':type,
#         'sexe':sexe,
#         'interact':interact,
#         'pih':pih,
#         'pecp':pecp}
#         )

# # insert into BDM_TFR
# print "Insert into BDM_TFR"
# for rec in db_tfr:
#     cip        = rec["CIP"]
#     nom_court  = rec["NOM_COURT"]
#     code_grp   = rec["CODE_GRP"]
#     nom_grp    = rec["NOM_GRP_G"]
#     code_atc   = rec["CODE_ATC"]
#     classe_atc = rec["CLASSE_ATC"]
#     pfht       = rec["PFHT"]
#     ppttc      = rec["PPTTC"]
#     tfr        = rec["TFR"]
#     dt_deb     = rec["DT_DEB"]
#     dt_fin     = rec["DT_FIN"]

#     cursor.execute('''
#         INSERT INTO BDM_TFR(cip,nom_court,code_grp,nom_grp,code_atc,classe_atc,pfht,ppttc,dt_deb,dt_fin)
#         VALUES(:cip,:nom_court,:code_grp,:nom_grp,:code_atc,:classe_atc,:pfht,:ppttc,:dt_deb,:dt_fin)''',
#         {'cip':cip,
#         'nom_court':nom_court,
#         'code_grp':code_grp,
#         'nom_grp':nom_grp,
#         'code_atc':code_atc,
#         'classe_atc':classe_atc,
#         'pfht':pfht,
#         'ppttc':ppttc,
#         'dt_deb':dt_deb,
#         'dt_fin':dt_fin}
#         )

# # # insert into BDM_GG
# print "Insert into BDM_GG"
# for rec in db_gg:
#     cip        = rec["CIP"]
#     nom_court  = rec["NOM_COURT"]
#     code_grp   = rec["CODE_GRP"]
#     nom_grp    = rec["NOM_GRP_G"]
#     code_atc   = rec["CODE_ATC"]
#     classe_atc = rec["CLASSE_ATC"]
#     dt_deb_afs = rec["DT_DEB_AFS"]
#     dt_fin_afs = rec["DT_FIN_AFS"]
#     debut_remb = rec["DEBUT_REMB"]
#     fin_remb   = rec["FIN_REMB"]

#     cursor.execute('''
#         INSERT INTO BDM_GG(cip,nom_court,code_grp,nom_grp,code_atc,classe_atc,dt_deb_afs, dt_fin_afs, debut_remb,fin_remb)
#         VALUES(:cip,:nom_court,:code_grp,:nom_grp,:code_atc,:classe_atc,:dt_deb_afs,:dt_fin_afs,:debut_remb,:fin_remb)''',
#         {'cip':cip,
#         'nom_court':nom_court,
#         'code_grp':code_grp,
#         'nom_grp':nom_grp,
#         'code_atc':code_atc,
#         'classe_atc':classe_atc,
#         'dt_deb_afs':dt_deb_afs,
#         'dt_fin_afs':dt_fin_afs,
#         'debut_remb':debut_remb,
#         'fin_remb':fin_remb}
#         )

# # # insert into BDM_TG
# print "Insert into BDM_TG"
# for rec in db_tg:
#     cip        = rec["CIP"]
#     nom_court  = rec["NOM_COURT"]
#     dt_effet   = rec["DT_EFFET"]
#     gen_ind    = rec["GEN_IND"]
#     code_grp   = rec["CODE_GRP"]
#     nom_grp    = rec["NOM_GRP_G"]
#     code_atc   = rec["CODE_ATC"]
#     classe_atc = rec["CLASSE_ATC"]

#     cursor.execute('''
#         INSERT INTO BDM_TG(cip, nom_court, dt_effet, gen_ind,code_grp,nom_grp,code_atc,classe_atc)
#         VALUES(:cip,:nom_court,:dt_effet,:gen_ind,:code_grp,:nom_grp,:code_atc,:classe_atc)''',
#         {'cip':cip,
#         'nom_court':nom_court,
#         'dt_effet':dt_effet,
#         'gen_ind':gen_ind,
#         'code_grp':code_grp,
#         'nom_grp':nom_grp,
#         'code_atc':code_atc,
#         'classe_atc':classe_atc})

# # insert into BDM_PRIX
# print "Insert into BDM_PRIX"

# for rec in db_prix:
#     cip        = rec["CIP"]
#     cip7       = rec["CIP7"]
#     prix_f     = rec["PRIX_F"]
#     prix_e     = rec["PRIX_E"]
#     fab_ht_f   = rec["FAB_HT_F"]
#     fab_ht_e   = rec["FAB_HT_E"]
#     taux       = rec["TAUX"]
#     date_appli = rec["DATE_APPLI"]
#     date_jo    = rec["DATE_JO"]
    
#     cursor.execute('''
#         INSERT INTO BDM_PRIX(cip,cip7,prix_f,prix_e,fab_ht_f,fab_ht_e,taux,date_appli,date_jo)
#         VALUES(:cip,:cip7,:prix_f,:prix_e,:fab_ht_f,:fab_ht_e,:taux,:date_appli,:date_jo)''',
#         {'cip':cip,
#         'cip7':cip7,
#         'prix_f':prix_f,
#         'prix_e':prix_e,
#         'fab_ht_f':fab_ht_f,
#         'fab_ht_e':fab_ht_e,
#         'taux':taux,
#         'date_appli':date_appli,
#         'date_jo':date_jo})

# con.commit()

# Insert CSV files into database

# convert_to_utf8("CIS.txt")
# convert_to_utf8("CIS_CIP.txt")

print "Insert CIS.txt into CIS table"

columns = ['cis', 'nom_court', 'forme', 'admin_mode', 'status', 'type_procedure', 'etat_commercial', 'code_document', 'dummy']

data = []
with open("CIS.txt") as f:
    for row in csv.DictReader(f, fieldnames=columns, delimiter='\t'):
        data.append(row)    

for rec in data:
    cis             = rec["cis"]
    nom_court       = rec["nom_court"]
    forme           = rec["forme"]
    admin_mode      = rec["admin_mode"]
    status          = rec["status"]
    type_procedure  = rec["type_procedure"]
    etat_commercial = rec["etat_commercial"]
    code_document   = rec["code_document"]
    dummy           = rec["dummy"]

    cursor.execute('''
        INSERT INTO CIS(cis,nom_court,forme,admin_mode,status,type_procedure,etat_commercial,code_document,dummy)
        VALUES(:cis,:nom_court,:forme,:admin_mode,:status,:type_procedure,:etat_commercial,:code_document,:dummy)''',
        {'cis':cis,
        'nom_court':nom_court,
        'forme':forme,
        'admin_mode':admin_mode,
        'status':status,
        'type_procedure':type_procedure,
        'etat_commercial':etat_commercial,
        'code_document':code_document,
        'dummy':dummy})

con.commit()

print "Insert CIS_CIP.txt into CIS_CIP table"

columns = ['cis','cip7', 'pres', 'status', 'declaration', 'date_declaration', 'cip13']

data = []
with open("CIS_CIP.txt") as f:
    for row in csv.DictReader(f, fieldnames=columns, delimiter='\t'):
        data.append(row)

for rec in data:
    cis              = rec['cis']
    cip7             = rec["cip7"]
    pres             = rec["pres"]
    status           = rec["status"]
    declaration      = rec["declaration"]
    date_declaration = rec["date_declaration"]
    cip13            = rec["cip13"]

    cursor.execute('''
        INSERT INTO CIS_CIP(cis,cip7,pres,status,declaration,date_declaration,cip13)
        VALUES(:cis,:cip7,:pres,:status,:declaration,:date_declaration,:cip13)''',
        {'cis':cis,
        'cip7':cip7,
        'pres':pres,
        'status':status,
        'declaration':declaration,
        'date_declaration':date_declaration,
        'cip13':cip13})

con.commit()

# Requête sql pour avoir les médicaments qui m'interessent

# cursor.execute("select CIS_CIP.cis,CIS_CIP.cip13,CIS.admin_mode,CIS.nom_court,CIS_CIP.pres,CIS_CIP.cip7 from CIS_CIP,CIS where CIS.cis = CIS_CIP.cis and CIS.etat_commercial=\"Commercialisée\" and CIS.admin_mode IN (\"orale\", \"nasale\",\"cutanée\", \"sous-cutanée\",\"ophtalmique\",\"rectale\",\"vaginale\",\"transdermique\",\"voie buccale autre\",\"intracaverneuse\",\"oropharyngée\",\"buccogingivale\", \"inhalée\", \"intramusculaire\",\"sublinguale\")"
#     )

# rows = cursor.fetchall()



# for row in rows:
#    print row

con.close()
