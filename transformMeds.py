#!/usr/bin/env python3.7
# -*-coding:utf-8 -*-


import os
import requests
import zipfile
import sys
import csv
import sqlite3
import shutil
import codecs
import re
import glob

def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def downloadFile(url):
    dummy = url.split('?')[-1]
    local_filename = dummy.split('=')[1]
    file = requests.get(url, stream=True)
    print ("Downloading %s" % local_filename)
    with open(local_filename, 'wb') as f:
        for chunk in file.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return local_filename


def writeOnSTDERR(msg):
        sys.stderr.write(msg)

def convert_to_utf8(sourceFileName, targetFileName):
    print ("Convert %s into UTF-8" % sourceFileName)
    BLOCKSIZE = 1048576 # or some other, desired size in bytes
    with codecs.open(sourceFileName, "r", "ISO-8859-15") as sourceFile:
        with codecs.open(targetFileName, "w", "utf-8") as targetFile:
            while True:
                contents = sourceFile.read(BLOCKSIZE)
                if not contents:
                    break
                targetFile.write(contents)
def cleanning():
    for filePath in glob.glob("CIS*"):
        if os.path.isfile(filePath):
            os.remove(filePath)
    try:
        os.remove("complete.db")
    except OSError:
        pass

    try:
        os.remove("drugs.db")
    except OSError:
        pass

    try:
        os.remove("all-drugs.sqlite3")
    except OSError:
        pass

    try:
        os.remove("myfile.csv")
    except OSError:
        pass

def truncate_string(string):
    parts = string.split("-",1)[0]
    dummy = parts.replace("équivalant à", "⇔")

    return (re.sub(' +', ' ', dummy).rstrip(', '))


def main():
    cleanning()

    cis_file = downloadFile("http://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_bdpm.txt")
    cis_cip_file = downloadFile("http://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_CIP_bdpm.txt")
    cis_gener_file = downloadFile ("http://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_GENER_bdpm.txt")
    cis_compo_file= downloadFile("http://base-donnees-publique.medicaments.gouv.fr/telechargement.php?fichier=CIS_COMPO_bdpm.txt")

    connexion = sqlite3.connect("all-drugs.sqlite3")
    connexion.text_factory = str
    cursor = connexion.cursor()

    cursor.execute("PRAGMA encoding = 'UTF-8';")

    # Create tables

    # CIS
    cursor.execute("create table CIS (cis VARCHAR(8), nom_court VARCHAR(100), forme VARCHAR(50), admin_mode VARCHAR(60), etat_commercial VARCHAR(25))")

    # CIS_CIP
    cursor.execute("create table CIS_CIP (cis VARCHAR(8),cip7 VARCHAR(7), pres VARCHAR(50), cip13 VARCHAR(13))")

    # CIS_GENER
    cursor.execute("create table CIS_GENER (libelle_group VARCHAR(255), cis VARCHAR(8))")
    connexion.commit()

    # Insert CSV files into database

    convert_to_utf8("CIS_bdpm.txt", "CIS.csv")
    convert_to_utf8("CIS_CIP_bdpm.txt", "CIS_CIP.csv")
    convert_to_utf8("CIS_GENER_bdpm.txt", "CIS_GENER.csv")
    convert_to_utf8("CIS_COMPO_bdpm.txt", "CIS_COMPO.csv")

    print ("Insert CIS.csv into CIS table")

    columns = ['cis', 'nom_court', 'forme', 'admin_mode', 'status', 'type_procedure', 'etat_commercial', 'code_document', 'dummy']

    data = []
    with open("CIS.csv") as f:
        for row in csv.DictReader(f, fieldnames=columns, delimiter='\t'):
            data.append(row)

    #with open("fake_cis.txt") as f:
    #    for row in csv.DictReader(f, fieldnames=columns,delimiter=','):
    #        data.append(row)

    for rec in data:
        cis             = rec[u"cis"]
        nom_court       = rec[u"nom_court"]
        forme           = rec[u"forme"]
        admin_mode      = rec[u"admin_mode"]
        etat_commercial = rec[u"etat_commercial"]

        cursor.execute("INSERT INTO CIS(cis,nom_court,forme,admin_mode, etat_commercial)\
            VALUES(:cis,:nom_court,:forme,:admin_mode,:etat_commercial)",\
            {'cis':cis,\
            'nom_court':nom_court,\
            'forme':forme,\
            'admin_mode':admin_mode,\
            'etat_commercial':etat_commercial\
            })

    cursor.execute('''create index cis_idx on CIS (cis)''')
    connexion.commit()

    print ("Insert CIS_CIP.csv into CIS_CIP table")

    columns = ['cis','cip7', 'pres', 'status', 'declaration', 'date_declaration', 'cip13']

    data = []
    with open("CIS_CIP.csv") as f:
        for row in csv.DictReader(f, fieldnames=columns, delimiter='\t'):
            data.append(row)

    #with open("fake_cis_cip.txt") as f:
    #    for row in csv.DictReader(f, fieldnames=columns,delimiter=','):
    #        data.append(row)

    for rec in data:
        cis              = rec['cis']
        cip7             = rec["cip7"]
        pres             = rec["pres"]
        cip13            = rec["cip13"]

        cursor.execute("INSERT INTO CIS_CIP(cis,cip7,pres,cip13)\
            VALUES(:cis,:cip7,:pres,:cip13)",\
            {'cis':cis,\
            'cip7':cip7,\
            'pres':pres,\
            'cip13':cip13})

    cursor.execute("create index cip_idx ON CIS_CIP (cis)")
    connexion.commit()

    columns = ['id_group', 'libelle_group', 'cis', 'dummy_num1', 'dummy_num2']
    data = []
    with open("CIS_GENER.csv") as f:
        for row in csv.DictReader(f, fieldnames=columns, delimiter='\t'):
            data.append(row)

    for rec in data:
        dummy           = rec['libelle_group']
        libelle_group = truncate_string(dummy)
        cis             = rec['cis']

        cursor.execute("INSERT INTO CIS_GENER(libelle_group,cis)\
            VALUES(:libelle_group,:cis)",\
            {'libelle_group':libelle_group,\
            'cis':cis})

    cursor.execute("create index gener_idx ON CIS_GENER (cis)")
    connexion.commit()

    # sauvegarde de la base complète pour tests

    with connexion:
        connexion.row_factory = sqlite3.Row

        cursor = connexion.cursor()
        print("Complete Database")

        cursor.execute("select CIS_CIP.cis,\
        CIS_CIP.cip13,CIS.admin_mode,CIS.nom_court,CIS_CIP.pres,CIS_CIP.cip7, CIS_GENER.libelle_group from CIS_CIP,CIS,CIS_GENER \
        where CIS.cis = CIS_CIP.cis \
        and CIS.cis = CIS_GENER.cis \
        and CIS.etat_commercial=\"Commercialisée\"\
        ")

        rows = cursor.fetchall()
    connexion.close()

    data = []
    datalist = []
    for row in rows:
        ligne = [row["cis"],row["cip13"],row["cip7"],row["admin_mode"],row["nom_court"],row["pres"], row["libelle_group"]]
        datalist.append(ligne)

    # Create new database for Android project

    connexion = sqlite3.connect(r"complete.db")
    connexion.text_factory = str
    cursor = connexion.cursor()

    cursor.execute("PRAGMA encoding = 'UTF-8'")

    # Create tables

    cursor.execute("create table medicaments (_id INTEGER PRIMARY KEY, cis VARCHAR(8), \
        cip13 VARCHAR(13), cip7 VARCHAR(7), mode_administration VARCHAR(60),\
        nom VARCHAR(100), presentation VARCHAR(50), libelle_group VARCHAR(255))")

    cursor.execute("create table android_metadata (locale TEXT)")
    cursor.execute("INSERT INTO android_metadata(locale) VALUES ('en-US')")

    i = 0

    for rec in datalist:
        i+=1
        _id = i
        cis = rec[0]
        cip13 = rec[1]
        cip7 = rec[2]
        mode_administration = rec[3]
        nom = rec[4]
        presentation = rec[5]
        libelle_group = rec[6]

        if len(cip7) == 0:
            cip7 = cip13[5:12]

        cursor.execute("INSERT INTO medicaments(_id, cis, cip13, cip7, mode_administration, nom, presentation, libelle_group) \
            VALUES(:_id,:cis,:cip13,:cip7,:mode_administration,:nom,:presentation, :libelle_group)",\
            {'_id':_id,\
            'cis':cis,\
            'cip13':cip13,\
            'cip7':cip7,\
            'mode_administration':mode_administration,\
            'nom':nom,\
            'presentation':presentation,\
            'libelle_group':libelle_group})

    cursor.execute("create index cip13_idx ON medicaments (cip13)")

    connexion.commit()
    connexion.close()

    # Requête sql pour avoir les médicaments qui m'interessent

    connexion = sqlite3.connect("all-drugs.sqlite3")
    with connexion:
        connexion.row_factory = sqlite3.Row

        cursor = connexion.cursor()

        print ("Fetching medocs")
        cursor.execute("select CIS_CIP.cis,\
        CIS_CIP.cip13,CIS.admin_mode,CIS.nom_court,CIS_CIP.pres,CIS_CIP.cip7, CIS_GENER.libelle_group from CIS_CIP,CIS,CIS_GENER \
        where CIS.cis = CIS_CIP.cis \
        and CIS.cis = CIS_GENER.cis \
        and CIS.etat_commercial=\"Commercialisée\"\
        and CIS.admin_mode IN (\
        \"orale\",\
        \"nasale\",\
        \"cutanée\",\
        \"sous-cutanée\",\
        \"ophtalmique\",\
        \"rectale\",\
        \"vaginale\",\
        \"transdermique\",\
        \"voie buccale autre\",\
        \"intracaverneuse\",\
        \"oropharyngée\",\
        \"buccogingivale\",\
        \"inhalée\",\
        \"intramusculaire\",\
        \"sublinguale\")\
        ")

        rows = cursor.fetchall()
    connexion.close()

    data = []
    datalist = []
    for row in rows:
        line = [row["cis"],row["cip13"],row["cip7"],row["admin_mode"],row["nom_court"],row["pres"], row["libelle_group"]]
        datalist.append(line)

    # Create new database for Android project

    connexion = sqlite3.connect(r"drugs.db")
    connexion.text_factory = str
    cursor = connexion.cursor()

    cursor.execute("PRAGMA encoding = 'UTF-8'")

    # Create tables

    cursor.execute("create table drugs (_id INTEGER PRIMARY KEY, cis VARCHAR(8), \
        cip13 VARCHAR(13), cip7 VARCHAR(7), administration_mode VARCHAR(60),\
        name VARCHAR(100), presentation VARCHAR(50), label_group VARCHAR(255))")

    cursor.execute("create table android_metadata (locale TEXT)")
    cursor.execute("INSERT INTO android_metadata(locale) VALUES ('en-US')")

    i = 0

    for rec in datalist:
        i+=1
        _id = i
        cis = rec[0]
        cip13 = rec[1]
        cip7 = rec[2]
        administration_mode = rec[3]
        name = rec[4]
        presentation = rec[5]
        label_group = rec[6]

        if len(cip7) == 0:
            cip7 = cip13[5:12]

        cursor.execute("INSERT INTO drugs(_id, cis, cip13, cip7, administration_mode, name, presentation, label_group) \
            VALUES(:_id,:cis,:cip13,:cip7,:administration_mode,:name,:presentation,:label_group)",\
            {'_id':_id,\
            'cis':cis,\
            'cip13':cip13,\
            'cip7':cip7,\
            'administration_mode':administration_mode,\
            'name':name,\
            'presentation':presentation,\
            'label_group':label_group})

    cursor.execute("create index cip13_idx ON drugs (cip13)")

    connexion.commit()
    connexion.close()

    csvfile = "myfile.csv"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n', delimiter=";", doublequote=True)
        for val in datalist:
            writer.writerow([val])

    #cleanning()


if __name__ == '__main__':
    main()
