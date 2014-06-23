#!/usr/bin/env python

from plistlib import *
import os
import requests
import zipfile
import sys
import subprocess

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

# Download AMM file
#ammFile = downloadFile("http://agence-prd.ansm.sante.fr/php/ecodex/telecharger/fic_cis_cip.zip")

# unzip AMM file
#fh = open(ammFile, 'rb')
#z = zipfile.ZipFile(fh)
#for name in z.namelist():
#	outfile = open(name, 'wb')
#	outfile.write('/tmp'+z.read(name))
#	outfile.close
#fh.close

apath = cmd_exists("unarj")

print apath