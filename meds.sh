#/bin/sh

# ------------------------------------------------------------------------- #
# Script de mise à jour de la base de medocs								#
#																			#
# - Versionning des fichiers existant										#
# - récupérattion du fichier zip et dézip									#
# - comparaison des fichiers versionnés avec les nouveaux					#
# -- Si les fichiers sont les mêmes -> destruction des fichiers versionnés	#
# -- Sinon utilisation des nouveaux fichiers								#
# - traitement des nouveaux fichiers (iconv +tr)							#
# - import dans la base des nouveaux fichiers								#
# - requete et export CSV													#
# - traitement CSV en PLIST													#
# - mail pour indiquer la dispo d'un nouveau fichier Meds.PLIST 			#
#																			#
# Auteur	: Jacques Foucry												#
# Date		: 2013-04-15													#
#-------------------------------------------------------------------------- #


WORKDIR=/perso/AFM
BACKUPDIR=/perso/AFM/BACKUP
DATUM=`/bin/date +"%F"`
MYSQLBIN=/usr/bin/mysql
SQLITEBIN=/usr/bin/sqlite3
MYSQLPASSWD=ensi031X
DATABASE=medocs
CSVOUTPUT=export.csv
PYTHONBIN=/usr/local/bin/python2.7
RECIPIENTLIST=jacques@foucry.net

echoerr()
{ 
	echo "$@" 1>&2;
}

backupFiles()
{
	if [[ ! -d ${BACKUPDIR} ]]; then
		/bin/mkdir ${BACKUPDIR}
	fi

	if [[ -f ${WORKDIR}/CIS.txt ]]; then
		/bin/mv ${WORKDIR}/CIS.txt ${BACKUPDIR}/CIS.txt.${DATUM}
	fi
	if [[ -f ${WORKDIR}/CIS_CIP.txt ]]; then
		/bin/mv ${WORKDIR}/CIS_CIP.txt ${BACKUPDIR}/CIS_CIP.txt.${DATUM}
	fi
	if [[ -f ${WORKDIR}/COMPO.txt ]]; then
		/bin/mv ${WORKDIR}/COMPO.txt ${BACKUPDIR}/COMPO.txt.${DATUM}
	fi

	if [[ -f ${WORKDIR}/fic_cis_cip.zip ]]; then
		/bin/rm ${WORKDIR}/fic_cis_cip.zip
	fi
}

downloadFiles()
{
	echo "Downloading files"
	/usr/bin/wget -P ${WORKDIR} http://agence-prd.ansm.sante.fr/php/ecodex/telecharger/fic_cis_cip.zip

	if [[ $? != 0 ]]; then
		echoerr "Error in download" 
		exit 255
	fi

	/usr/bin/unzip ${WORKDIR}/fic_cis_cip.zip -d ${WORKDIR}

	if [[ $? != 0 ]]; then
		echoerr "Error in unziping file"
		exit 255
	fi
}

downloadSSFiles()
{
	echo "Downloading SS files..."
	/usr/bin/wget -P ${WORKDIR} http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm/AFM.EXE

	if [[ $? != 0 ]]; then
		echoerr "Error in download SS files"
		exit 255
	fi

	/usr/bin/arj e ${WORKDIR}/AFM.EXE ${WORKDIR} -u -y

	if [[ $? != 0 && $? != 1 ]]; then
		echoerr "Error in unarj SS files $?"
		exit 255
	fi

	/bin/rm ${WORKDIR}/AFM.EXE
}

convertSSFiles()
{

	if [[ ! -x /usr/bin/dbf ]]; then
		echoerr "Cannot find /usr/bin/dbf. Please fix it before continue"
		exit 255
	fi

	cd ${WORKDIR}

	for dbfile in `ls BDM_*.DBF`
	do
		file=`/bin/basename ${dbfile} .DBF`
		echo "Converting ${dbfile}..."
		/usr/bin/dbf --separator ';' --csv - ${dbfile} | /usr/bin/tail -n +2 | /usr/bin/tr ";" "\t" > ${WORKDIR}/${file}.tmp
		/usr/bin/iconv -t UTF-8 ${WORKDIR}/${file}.tmp > ${WORKDIR}/${file}.csv
		# /bin/rm ${WORKDIR}/${dbfile}
		# /bin/rm ${WORKDIR}/${file}.tmp
	done
}

checkFiles()
{
	cd ${WORKDIR}

	for i in *.txt; do
		A=`/usr/bin/md5sum ${i}` | /bin/cut -f 1
		B=`/usr/bin/md5sum ${BACKUPDIR}/${i}.${DATUM}` | /bin/cut -f 1 

#		if [[ ${A} == ${B} ]]; then
#			echo "Removing ${BACKUPDIR}/${i}.${DATUM}"
#			/bin/rm ${BACKUPDIR}/${i}.${DATUM}
#			/bin/mail -s "No new Meds.plist" ${RECIPIENTLIST} <<EOF
#Salut Jacques,
#
#Il n'y a pas de nouvelle version de Meds.plist.
#
#Ton Script
#EOF
#			exit 0
#		fi
	done
}

convertFiles()
{
	cd ${WORKDIR}
	for i in `ls *.txt`; do
		filename=`/bin/basename ${i} .txt`
		echo "Converting $i into ${filename}.csv"
		#/usr/bin/iconv -f ISO8859-15 -t UTF-8 ${i} | /usr/bin/tr "\t" ";" > ${filename}.csv
		/usr/bin/iconv -f ISO8859-15 -t UTF-8 ${i} > ${filename}.csv
	done
}

importCSVFiles()
{
	cd ${WORKDIR}
	echo "Importing CSV file into database"
	if [[ ! -f ${WORKDIR}/import_csv-sqlite3.sql ]]; then
		echoerr "Error in importCSVFiles, cannot find import_csv.sql file"
		exit 255
	fi
	
	# ${MYSQLBIN} -u root -p${MYSQLPASSWD} < ${WORKDIR}/import_csv.sql 
	${SQLITEBIN} ${WORKDIR}/${DATABASE}.sqlite3 < ${WORKDIR}/import_csv-sqlite3.sql

	if [[ $? != 0 ]]; then
		echoerr "Error during sql import, please check log file"
		exit 255
	fi
}

exportSelectionToCSVFile()
{
	cd ${WORKDIR}

	echo "Exporting query result to csv file"
	if [[ -f ${WORKDIR}/${CSVOUTPUT} ]]; then
		/bin/rm ${WORKDIR}/${CSVOUTPUT}
	fi

	if [[ ! -f ${WORKDIR}/requete.sql ]]; then
		echoerr "Error, cannot find requete.sql file"
		exit 255
	fi

	# ${MYSQLBIN} -u root -p${MYSQLPASSWD} ${DATABASE} < requete.sql > ${WORKDIR}/export.csv 
	${SQLITEBIN} ${WORKDIR}/${DATABASE}.sqlite3 < ${WORKDIR}/requete-sqlite3.sql > ${WORKDIR}/export.csv
	if [[ $? != 0 ]]; then
		echoerr "Error in exportSelectionToCSVFile, please check log file"
		exit 255
	fi

	# Add headers
	# /bin/sed -i '1d' ${WORKDIR}/export.csv 
	# /bin/sed -i '1icis,cip13,admin,nom,pres,cip7' ${WORKDIR}/export.csv

}

transformToMeds()
{
	cd ${WORKDIR}

	echo "Transforming CVS into Plist"
	${PYTHONBIN} /usr/local/bin/cvs2plist.py ${WORKDIR}/export.csv ${WORKDIR}/Meds.plist dict

	if [[ $? != 0 ]]; then
		echoerr "Error during cvs2plist transform, please check log file"
		exit 255
	fi
}

compressMeds()
{
	echo "Compressing meds.plist"
	/bin/tar zcf ${WORKDIR}/Meds.plist.tgz ${WORKDIR}/Meds.plist
}

sendMail()
{
	echo "Sending mail"
	cat ${WORKDIR}/mail.txt | /bin/mail -s "Nouvelle version de Meds.plist" ${RECIPIENTLIST} < ${WORKDIR}/Meds.plist.tgz
}

backupFiles
downloadFiles
downloadSSFiles
checkFiles
convertFiles
convertSSFiles
importCSVFiles
exportSelectionToCSVFile
transformToMeds
ompressMeds
sendMail

exit 0
