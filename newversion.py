#!/usr/bin/env python
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

# Download AMM file
#ammFile = downloadFile("http://agence-prd.ansm.sante.fr/php/ecodex/telecharger/fic_cis_cip.zip")
#secuFile = downloadFile("http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm/AFM.EXE")

# unzip AMM file
#fh = open(ammFile, 'rb')
#z = zipfile.ZipFile(fh)
#for name in z.namelist():
#	outfile = open(name, 'wb')
#	outfile.write('/tmp'+z.read(name))
#	outfile.close
#fh.close

# if cmd_exists("unarj"):
#     cmd_string = ['unarj', 'e', secuFile]
#     try:
#         subprocess.check_call(cmd_string)
#     except OSError as e:
#         # logger.debug("Error in %s, exiting"% (cmd_string))
#         writeOnSTDERR("Error in %s. exiting" % (cmd_string))
#         sys.exit(1)

if cmd_exists("dbf"):
    for file in os.listdir('.'):
        if file == "BDM_CIP.DBF":
            print file
            # $DBF_CMD --separator ';' --csv - ${dbfile} | /usr/bin/tail -n +2 | $AWK_CMD -F ';' 'NF==34' | /usr/bin/tr ";" "\t" > ${WORKDIR}/${file}.tmp
        elif file == "BDM_TFR.DBF":
            # $DBF_CMD --separator ';' --csv - ${dbfile} | /usr/bin/tail -n +2 | $AWK_CMD -F ';' 'NF==11' | /usr/bin/tr ";" "\t" > ${WORKDIR}/${file}.tmp
            print file
        elif file == "BDM_GG.DBF":
            # $DBF_CMD --separator ';' --csv - ${dbfile} | /usr/bin/tail -n +2 | $AWK_CMD -F ';' 'NF==10' | /usr/bin/tr ";" "\t" > ${WORKDIR}/${file}.tmp
            print file
        elif file == "BDM_TG.DBF":
            # $DBF_CMD --separator ';' --csv - ${dbfile} | /usr/bin/tail -n +2 | $AWK_CMD -F ';' 'NF==8' | /usr/bin/tr ";" "\t" > ${WORKDIR}/${file}.tmp
            # cmd_string = ['dbf','--separator', ';', '--csv','-', file]
            try:
                db = dbf.Dbf("BDM_CIP.DBF")
                print db
                for rec in db:
                    print rec
                print
                # tg_table = dbf.Table(file, 'cip C(13); nom_court C(50); dt_effet D;gen_ind C(1);code_grp N(6,0);nom_grp C(124);code_atc C(10);classe_atc C(77)')
                # tg_table.open()
                # dbf.export(tg_table, 'tg.csv', 'cip C(13); nom_court C(50); dt_effet D;gen_ind C(1);code_grp N(6,0);nom_grp C(124);code_atc C(10);classe_atc C(77)','tab', 'utf-8')
                # tg_table.close()
            except OSError as e:
                writeOnSTDERR("Error in %s, exiting"% (cmd_string))
        elif file == "BDM_PRIX.DBF":
            print file
            # $DBF_CMD --separator ';' --csv - ${dbfile} | /usr/bin/tail -n +2 | $AWK_CMD -F ';' 'NF==9' | /usr/bin/tr ";" "\t" > ${WORKDIR}/${file}.tmp
        
