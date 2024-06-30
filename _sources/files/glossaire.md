# Glossaire

Glossaire des principaux termes utilisés

```{glossary}
[Baromètre AVERE](https://www.avere-france.org/wp-content/uploads/2024/06/Barometres_2024-05_20240606-Barometre-IRVE-Mai-2024-Externe-combine.pdf)
    Indicateurs IRVE publiés mensuellement par l'AVERE

[schéma de données statiques](https://schema.data.gouv.fr/etalab/schema-irve-statique/2.3.1/documentation.html)
    Spécification du fichier d'échange relatif aux données concernant la localisation géographique et les caractéristiques techniques des stations et des points de recharge pour véhicules électriques.

[Point de recharge (journal officiel)](https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000043475376)
    Une interface associée à un emplacement de stationnement qui permet de recharger un seul véhicule électrique à la fois

[Station de recharge (journal officiel)](https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000043475376) 
    Une zone comportant une borne de recharge associée à un ou des emplacements de stationnement ou un ensemble de bornes de recharge associées à des emplacements de stationnement, exploitée par un ou plusieurs opérateurs.

[Borne de recharge (journal officiel)](https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000043475376)
    Un appareil fixe raccordé à un point d'alimentation électrique, comprenant un ou plusieurs points de recharge et pouvant intégrer notamment des dispositifs de communication, de comptage, de contrôle ou de paiement.

[Taux de sessions de recharge réussies (définition AFIREV)](https://www.observatoire-recharge-afirev.fr/wp-content/uploads/2023/06/ObsAFIREV2023_AnnexesMethodologiques-1.pdf)
    Le taux de sessions de recharge réussies est le rapport entre le nombre des sessions de recharge réussies et le nombre total de sessions de recharge sur la période considérée. Sont considérées comme « réussies », les sessions de recharge respectant un des deux critères suivants :

    - Les sessions de recharge ayant duré plus de 2 minutes ET ayant fourni une énergie supérieure à 0,5 kWh.
    - Les sessions de recharge ayant été interrompues volontairement par le client.

    Seules les sessions de recharge démarrées après authentification puis autorisation du superviseur sont prises en compte dans le calcul (présentant un « start » ou autre statut équivalent permettant d’identifier le lancement de la recharge depuis l’outil de supervision des bornes). Les sessions de recharge sur des prises de type EF sont intégrées au calcul.

[Taux de disponibilité des points de recharge (définition AFIREV)](https://www.observatoire-recharge-afirev.fr/wp-content/uploads/2023/06/ObsAFIREV2023_AnnexesMethodologiques-1.pdf)
    Le taux de disponibilité des points de recharge est le rapport entre le temps de disponibilité des points de recharge et le temps total de la période étudiée. Sont considérées comme « indisponible » un point de recharge dont l’état est :

    - En statut erreur (« Faulted » ou « OutOfOrder »)
    - En statut inconnu, c’est-à-dire en perte de communication (« Unknown ») depuis plus de 24h.
    - Dont l’accès est impossible à l’usager peu importe la cause (ex : maintenance)
    
    Seule la disponibilité lors des horaires d’ouverture commerciaux de la station (horaires communiqués à l’usager) est prise en compte. Dans ce cas, au dénominateur de l’indicateur, le temps total de la période étudiée est le temps total d’ouverture de la station sur la période étudiée.  Le calcul du temps de disponibilité d’un point de recharge s’effectue comme une moyenne du temps de disponibilité des connecteurs de ce point de recharge.

[Taux de bon fonctionnement des systèmes informatiques (définition AFIREV)](https://www.observatoire-recharge-afirev.fr/wp-content/uploads/2023/06/ObsAFIREV2023_AnnexesMethodologiques-1.pdf)
    Le taux de bon fonctionnement des systèmes informatiques est le rapport entre le temps disponible des systèmes informatiques et le temps total observé.  Un système est considéré comme disponible lorsqu’il fonctionne sans interruption (notion Uptime). Les systèmes informatiques considérés dans le calcul sont l’ensemble des services qui sont nécessaires à la réalisation des services au client final en temps réel.  Les cas de maintenances programmées sont exclus dans la mesure où ils ont donné lieu à information des partenaires concernés. 

[Taux de points de charge disponibles 99% du temps (définition AFIREV)](https://www.observatoire-recharge-afirev.fr/wp-content/uploads/2023/06/ObsAFIREV2023_AnnexesMethodologiques-1.pdf)
    Le taux de points de charge disponibles 99% du temps est le nombre de points de charge réputés disponibles plus de 99% du temps par rapport au nombre total de points de charge en interopérabilité dans la plateforme Gireve. La définition d’un point de charge indisponible est celle de la charte qualité de l’AFIREV:

    - est considéré indisponible un point de charge en statut Hors Service.

[Taux de points de charge indisponibles depuis plus de 7 jours (définition AFIREV)](https://www.observatoire-recharge-afirev.fr/wp-content/uploads/2023/06/ObsAFIREV2023_AnnexesMethodologiques-1.pdf)
    Le taux de points de charge indisponibles depuis plus de 7 jours est le nombre de points de charge indisponibles depuis plus de 7 jours par rapport au nombre total de points de charge en interopérabilité dans la plateforme Gireve. La définition d’un point de charge indisponible est celle de la charte qualité de l’AFIREV:

    - est considéré indisponible un point de charge en statut Hors Service.
```
