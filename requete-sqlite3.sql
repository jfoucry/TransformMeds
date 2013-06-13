.header on
.mode csv

select CIS_CIP.cis,CIS_CIP.cip13,CIS.admin_mode,CIS.nom_court,CIS_CIP.pres,CIS_CIP.cip7 from CIS_CIP,CIS where CIS.cis = CIS_CIP.cis and CIS.etat_commercial="Commercialisée" and CIS.admin_mode IN ("orale", "nasale","cutanée", "sous-cutanée","ophtalmique","rectale","vaginale","transdermique","voie buccale autre","intracaverneuse","oropharyngée","buccogingivale", "inhalée", "intramusculaire", "sublinguale");
