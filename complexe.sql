SELECT CIS_CIP.cis,
                       CIS_CIP.cip13,CIS.admin_mode,CIS.nom_court,CIS_CIP.pres,CIS_CIP.cip7,
                       CIS_GENER.libelle_group FROM CIS
                       INNER JOIN CIS_CIP
                       ON CIS.cis = CIS_CIP.cis
                       LEFT JOIN CIS_GENER
                       ON CIS.cis = CIS_GENER.cis
                       WHERE CIS.etat_commercial="Commercialisée"
                       and CIS.admin_mode IN (
        "orale",
        "nasale",
        "cutanée",
        "sous-cutanée",
        "ophtalmiqu",
        "rectale",
        "vaginale",
        "transdermique",
        "voie buccale autre",
        "intracaverneuse",
        "oropharyngée",
        "buccogingivale",
        "inhalée",
        "intramusculaire",
        "sublinguale")