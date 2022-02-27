Select CIS_CIP.cis,
        CIS_CIP.cip13,CIS.admin_mode,CIS.nom_court,CIS_CIP.pres,CIS_CIP.cip7, CIS_GENER.libelle_group, CIS_GENER.gener_type from CIS_CIP,CIS,CIS_GENER
        where CIS.cis = CIS_CIP.cis
        and CIS.cis = CIS_GENER.cis
        and CIS.etat_commercial="Commercialisée"
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
