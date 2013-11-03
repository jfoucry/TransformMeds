#/bin/sh

# ------------------------------------------------------------------------- #
# Script de mise à jour de la base de medocs                                #
#                                                                           #
# - Versionning des fichiers existant                                       #
# - récupérattion du fichier zip et dézip                                   #
# - comparaison des fichiers versionnés avec les nouveaux                   #
# -- Si les fichiers sont les mêmes -> destruction des fichiers versionnés  #
# -- Sinon utilisation des nouveaux fichiers                                #
# - traitement des nouveaux fichiers (iconv +tr)                            #
# - import dans la base des nouveaux fichiers                               #
# - requete et export CSV                                                   #
# - traitement CSV en PLIST                                                 #
# - mail pour indiquer la dispo d'un nouveau fichier Meds.PLIST             #
#                                                                           #
# Auteur    : Jacques Foucry                                                #
# Date      : 2013-04-15                                                    #
#-------------------------------------------------------------------------- #


DATUM=`/bin/date +"%F"`
MYSQLBIN=/usr/bin/mysql
SQLITEBIN=/usr/bin/sqlite3
MYSQLPASSWD=ensi031X
DATABASE=medocs
CSVOUTPUT=export.csv
RECIPIENTLIST=jacques@foucry.net

OS=`uname -s`

if [[ $OS == "Darwin" ]]; then
    DL_CMD="/usr/local/bin/wget"
    WORKDIR=/Users/jacques/AFM
    BACKUPDIR=/Users/jacques/AFM/BACKUP
    UNARJ="/usr/local/bin/unarj"
    DBF_CMD="/usr/local/bin/dbf"
    CUT_CMD="/usr/bin/cut"
    MD5_CMD="/sbin/md5"
    BASENAME_CMD="/usr/bin/basename"
    PYTHONBIN="/usr/bin/python"
    TAR_CMD="/usr/bin/tar"
    MAIL_CMD="/usr/bin/mail"
    AWK_CMD="/usr/local/bin/gawk"
    SED_CMD="/usr/bin/sed"
else
    DL_CMD="/usr/bin/wget"
    WORKDIR=/perso/AFM
    BACKUPDIR=/perso/AFM/BACKUP
    UNARJ="/usr/bin/arj"
    DBF_CMD="/usr/bin/dbf"
    CUT_CMD="/bin/cut"
    MD5_CMD="/usr/bin/md5sum"
    BASENAME_CMD="/bin/basename"
    PYTHONBIN="/usr/local/bin/python2.7"
    TAR_CMD="/bin/tar"
    MAIL_CMD="/bin/mail"
    UNAME_CMD="/bin/uname"
    AWK_CMD="/bin/awk"
    SED_CMD="/bin/sed"
fi


CURRENT_PATH=`dirname $0`

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
    $DL_CMD -P ${WORKDIR} http://agence-prd.ansm.sante.fr/php/ecodex/telecharger/fic_cis_cip.zip

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
    $DL_CMD -P ${WORKDIR} http://www.codage.ext.cnamts.fr/f_mediam/fo/bdm/AFM.EXE

    if [[ $? != 0 ]]; then
        echoerr "Error in download SS files"
        exit 255
    fi

    $UNARJ e ${WORKDIR}/AFM.EXE

    if [[ $? != 0 && $? != 1 ]]; then
        echoerr "Error in unarj SS files $?"
        exit 255
    fi

    /bin/rm ${WORKDIR}/AFM.EXE
}

convertSSFiles()
{
	set -x

    if [[ ! -x $DBF_CMD ]]; then
        echoerr "Cannot find ${DBF_CMD}. Please fix it before continue"
        exit 255
    fi

    cd ${WORKDIR}

    for dbfile in `ls BDM_*.DBF`
    do
        file=`$BASENAME_CMD ${dbfile} .DBF`
        echo "Converting ${dbfile}..."
        case $dbfile in
            BDM_CIP.DBF)
                $DBF_CMD --separator ';' --csv - ${dbfile} | /usr/bin/tail -n +2 | $AWK_CMD -F ';' 'NF==34' | /usr/bin/tr ";" "\t" > ${WORKDIR}/${file}.tmp
                ;;
            BDM_TFR.DBF)
                $DBF_CMD --separator ';' --csv - ${dbfile} | /usr/bin/tail -n +2 | $AWK_CMD -F ';' 'NF==11' | /usr/bin/tr ";" "\t" > ${WORKDIR}/${file}.tmp
                ;;
            BDM_GG.DBF)
                $DBF_CMD --separator ';' --csv - ${dbfile} | /usr/bin/tail -n +2 | $AWK_CMD -F ';' 'NF==10' | /usr/bin/tr ";" "\t" > ${WORKDIR}/${file}.tmp
                ;;
            BDM_TG.DBF)
                $DBF_CMD --separator ';' --csv - ${dbfile} | /usr/bin/tail -n +2 | $AWK_CMD -F ';' 'NF==8' | /usr/bin/tr ";" "\t" > ${WORKDIR}/${file}.tmp
                ;;
            BDM_PRIX.DBF)
                $DBF_CMD --separator ';' --csv - ${dbfile} | /usr/bin/tail -n +2 | $AWK_CMD -F ';' 'NF==9' | /usr/bin/tr ";" "\t" > ${WORKDIR}/${file}.tmp
                ;;
        esac
        /usr/bin/iconv -t UTF-8 ${WORKDIR}/${file}.tmp > ${WORKDIR}/${file}.csv
        #/bin/rm ${WORKDIR}/${dbfile}
        #/bin/rm ${WORKDIR}/${file}.tmp
    done
}

checkFiles()
{
    cd ${WORKDIR}

    for i in *.txt; do
        A=`$MD5_CMD ${i}` | $CUT_CMD -f 1
        B=`$MD5_CMD ${BACKUPDIR}/${i}.${DATUM}` | $CUT_CMD -f 1 

#       if [[ ${A} == ${B} ]]; then
#           echo "Removing ${BACKUPDIR}/${i}.${DATUM}"
#           /bin/rm ${BACKUPDIR}/${i}.${DATUM}
#           /bin/mail -s "No new Meds.plist" ${RECIPIENTLIST} <<EOF
#Salut Jacques,
#
#Il n'y a pas de nouvelle version de Meds.plist.
#
#Ton Script
#EOF
#           exit 0
#       fi
    done
}

convertFiles()
{
    cd ${WORKDIR}
    for i in `ls *.txt`; do
        filename=`$BASENAME_CMD ${i} .txt`
        echo "Converting $i into ${filename}.csv"
        #/usr/bin/iconv -f ISO8859-15 -t UTF-8 ${i} | /usr/bin/tr "\t" ";" > ${filename}.csv
        /usr/bin/iconv -f ISO8859-15 -t UTF-8 ${i} > ${filename}.csv
    done
}

importCSVFiles()
{
    cd ${WORKDIR}
    echo "Importing CSV file into database"
    if [[ ! -f ${CURRENT_PATH}/import_csv-sqlite3.sql ]]; then
        echoerr "Error in importCSVFiles, cannot find import_csv.sql file"
        exit 255
    fi
    
    # ${MYSQLBIN} -u root -p${MYSQLPASSWD} < ${WORKDIR}/import_csv.sql 
    ${SQLITEBIN} ${WORKDIR}/${DATABASE}.sqlite3 < ${CURRENT_PATH}/import_csv-sqlite3.sql

    if [[ $? != 0 ]]; then
        echoerr "Error during sql import, please check log file"
        #exit 255
    fi
}

exportSelectionToCSVFile()
{
    cd ${WORKDIR}

    echo "Exporting query result to csv file"
    if [[ -f ${WORKDIR}/${CSVOUTPUT} ]]; then
        /bin/rm ${WORKDIR}/${CSVOUTPUT}
    fi

    if [[ ! -f ${CURRENT_PATH}/requete.sql ]]; then
        echoerr "Error, cannot find requete.sql file"
        exit 255
    fi

    # ${MYSQLBIN} -u root -p${MYSQLPASSWD} ${DATABASE} < requete.sql > ${WORKDIR}/export.csv 
    ${SQLITEBIN} ${WORKDIR}/${DATABASE}.sqlite3 < ${CURRENT_PATH}/requete-sqlite3.sql > ${WORKDIR}/export.csv
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
    ${PYTHONBIN} /usr/local/bin/csv2plist.py ${WORKDIR}/export.csv ${WORKDIR}/Meds.plist dict

    if [[ $? != 0 ]]; then
        echoerr "Error during cvs2plist transform, please check log file"
        exit 255
    fi
}

compressMeds()
{
    echo "Compressing meds.plist"
    $TAR_CMD zcf ${WORKDIR}/Meds.plist.tgz ${WORKDIR}/Meds.plist
}

sendMail()
{
    echo "Sending mail"
    cat ${CURRENT_PATH}/mail.txt | $MAIL_CMD -s "Nouvelle version de Meds.plist" ${RECIPIENTLIST} < ${WORKDIR}/Meds.plist.tgz
}

#backupFiles
#downloadFiles
#downloadSSFiles
#checkFiles
#convertFiles
convertSSFiles
importCSVFiles
exportSelectionToCSVFile
#transformToMeds
#compressMeds
#sendMail

exit 0
