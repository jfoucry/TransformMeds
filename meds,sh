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


WORKDIR=/home/jfoucry/AFM
BACKUPDIR=/home/jfoucry/AFM/BACKUP
DATUM=`/bin/date +"%F"`

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
	/usr/bin/wget -P ${WORKDIR} http://agence-prd.ansm.sante.fr/php/ecodex/telecharger/fic_cis_cip.zip

	if [[ $? != 0 ]]; then
		echo "Error in download"
		exit 255
	fi

	/usr/bin/unzip ${WORKDIR}/fic_cis_cip.zip -d ${WORKDIR}

	if [[ $? != 0 ]]; then
		echo "Error in unziping file"
		exit 255
	fi
}

checkFiles()
{
	cd ${WORKDIR}

	for i in `ls *.txt`; do
		A=`/usr/bin/md5sum ${i}` | /bin/cut -f 1
		B=`/usr/bin/md5sum ${BACKUPDIR}/${i}.${DATUM}` | /bin/cut -f 1 

		echo ${A}
		echo ${B}

		if [[ ${A} == ${B} ]]; then
			/bin/rm ${BACKUPDIR}/${i}.${DATUM}
		fi
	done
}

convertFiles()
{
	cd ${WORKDIR}
	for i in `ls *.txt`; do
		filename=`/bin/basename ${i} .txt`
		/usr/bin/iconv -f ISO8859-15 -t UTF-8 ${i} | /usr/bin/tr "\t" ";" > ${filename}.csv
	done
}
backupFiles
downloadFiles
checkFiles
convertFiles

exit 0
