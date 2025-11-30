# Avancement

## Reste à faire

- animation

  - animation staging
    - validation des flux opérateurs (17 en cours)
  - animation production
    - mise en place d'un reporting interne / opérateurs
    - suivi des bilans hebdomadaire des données

- exploitation / maintenance

  - gestion des utilisateurs
  - gestion des données (opérateurs, aménageurs, unités d'exploitation)
  - traitement des incidents
  - reprises de données
  - traitement des bugs

- documentation

  - extension FAQ
  - mise à jour de la documentation de présentation (pages)
  - procédures (onboarding, exploitation applications/données/utilisateurs, maintenance, Tiruert)

- Prefect

  - indicateurs à ajouter
    - intégration des indicateurs autoroute et AFIR (liste des stations)
    - intégration des indicateurs d'usage et de qualité de service

- Tiruert

  - extraction des volumes d'énergie par catégorie
  - interface Enedis
  - déploiement du consentement

- API
  
  - blocage des modifications après 15 j
  - reprise des indicateurs et des données S3 depuis début Avril
  - évolution de la règle des 15j pour les sessions (passage à du temps réel avec possibilité de mettre à jour pendant 15 jours) ??

- Modèle européen

  - évolution modèle de données
  - évolution des API
  - évolution des indicateurs
  - migration/compatibilité des données (base de données + historisation + S3)
  - évolution des analyses
  - évolution interface PAN
  - gestion des tarifs (structure + dynamique-lent)

- Outils d'analyse de données

  - outil d'analyse de la qualité de service (disponibilité, occupation, qualité)
    - mesure de qualité des statuts
  - outil d'analyse de saturation
    - ajout des données VINCI (aires)
    - ajout des aires de repos
    - intégration théorème de shannon
    - intégration dans Qualicharge
    - intégration de la pleine utilisation
  - outil de prédiction
  - outil d'analyse réseau
    - adaptation de l'outil au double-sens
    - affectation du sens aux échangeurs autoroutiers
    - outil de paramétrage des jonctions et échangeurs
    - affectation du sens aux aires de service
    - optimisation de la fonction de calcul de maillage par noeuds
    - étude basculement ROUTE500 vers BDCARTO
    - intégration dans Qualicharge

- Analyse de données

  - extension de l'analyse de saturation Vinci ?
  - autres ?

## Orientations décembre (6)

- onboarding des opérateurs
  - validation de flux d'opérateurs (prévu: Z-E-N, Wewise, Zetra, Partage ma borne, Idex, Greenspot, OZECAR, Monta, Obornes, e-charge50, We-go, Indelec, Bouygues v2)
  - activité récurrente de suivi des opérateurs
  - prise en compte de la signature de l'arrêté (préparation du recalcul des indicateurs et des purges de données anciennes)
- suivi de la production
  - ajout d'un indicateur d'unicité des SIREN
- indicateurs
  - tableau de bord sur la qualité des données
  - calcul de l'indicateur de fiabilité des statuts
  - stockage des données pour les indicateurs saturation, disponibilité, occupation
- modèle de données européen
  - proposition d'évolution du modèle de données Qualicharge
- saturation
  - calcul sur les ponts de novembre (si pertinent)

## Activités novembre (10)

- onboarding des opérateurs
  - validation de flux d'opérateurs (R3-charge, Dream, Ubitricity)
  - activité récurrente de suivi des opérateurs
  - extension aux pdc sans session (AC)
- suivi de la production
  - adaptation des critères qualité aux pdc sans sessions
  - ajout d'un indicateur qualité (pdc inactifs)
  - procédure de migration d'un opérateur à un autre (cas R3 de LMS vers MONTA)
- indicateurs
  - ajout des indicateurs qualité des données
- analyse de la qualité de service (si prioritaire)
  - définition du mode de calcul des indicateurs saturation, disponibilité, occupation

## Activités octobre (14)

- onboarding des opérateurs
  - validation de flux d'opérateurs (Shell, Sowatt, Freshmile, Soregies)
  - activité récurrente de suivi des opérateurs
  - extension FAQ
- suivi de la production
  - critères qualités des données dynamiques sur Prefect (100 %)
  - reporting effectué pour tous les opérateurs en production avant le 1/9
- indicateurs
  - amélioration des perfs sur les requêtes liées aux données dynamiques
  - tableau de bord sur l'évolution des données (exploitation des indicateurs)

## Activités septembre (14)

- onboarding des opérateurs
  - validation de flux d'opérateurs (Zunder, R3, Yaway)
  - activité récurrente de suivi des opérateurs
- suivi de la production
  - critères qualités des données dynamiques sur Prefect (sauf consistence statuts-sessions)
  - démarrage d'un reporting
- analyse de la qualité de service (saturation, disponibilité, occupation)
  - fin d'étude comparative du suivi Vinci de la saturation (restitution)
  - analyse des indicateurs DGITM
  - simulateur/comparateur des indicateurs de saturation

## Activités août (11)

- animation de la qualité des données
  - validation de flux d'opérateurs (Bouygues)
  - activité récurrente de suivi des opérateurs
- suivi de la production
  - critères qualité des données statiques sur Prefect (automatisation des tests MetaBase)
- analyse de la qualité de service (saturation, disponibilité, occupation)
  - nouvelle version de l'outil d'analyse des saturations (+ intégration Métabase)
  - étude comparative du suivi Vinci de la saturation (données de juillet à mi-aout)
  - restitution de l'étude globale saturation (première version)

## Activité juillet (13)

- animation de la qualité des données
  - validation de flux d'opérateurs (Waat, QoWatt, Eoliberty, NW IEcharge, Izivia, FastNed, Driveco, TotalEnergies, SPIE City, Izivia, GEEVE)
  - activité récurrente de suivi des opérateurs
- documentation
  - Mise à jour du document de présentation du modèle de données Qualicharge
  - Mise à jour du document de présentation des indicateurs d'usage Qualicharge
- suivi de la production
  - outil de suivi des mises en production
- analyse de la qualité de service (saturation, disponibilité, occupation)
  - nouvelle version (V2) de l'outil d'analyse des saturations
  - extension au mois de juillet de l'analyse de saturation des ponts de mai

## Activités juin (15)

- animation de la qualité des données
  - activité récurrente de suivi des opérateurs
  - reporting
  - validation de flux d'opérateurs (Mobilize, Electra, Allego)
- analyse de la qualité de service (saturation, disponibilité, occupation)
  - méthodologie pour la saturation
  - report de l'analyse de l'occupation des statuts sur les sessions
  - analyse de périodes à forte charge (ponts de mai)
  - restitution des données (cartes folium, Metabase)

## Activités mai (14)

- animation de la qualité des données
  - activité récurrente de suivi des opérateurs
  - validation de flux d'opérateurs (station-E, ionity, Bump, E-Totem)
  - mise à niveau des requètes de validation (préparation au basculement sur Prefect)
- outil d'analyse réseau
  - fonction de filtrage des stations et parcs RTE-T (préparation de l'indicateur - liste des stations et parcs RTE-T)
- analyse de la qualité de service (saturation, disponibilité, occupation)
  - évolution de la définition de l'indicateur de saturation
  - fonction de calcul des indicateurs de saturation (à partir des sessions et statuts)
  - restitution cartographique de l'évolution temporelle de la saturation
  - définition de l'indicateur e3 - liste des stations et parcs RTE-T
  - test de l'analyse sur un périmètre restreint (un département / un jour)
- indicateurs
  - intégration des indicateurs de qualité de service
  - intégration des indicateurs TIRUERT

## Activités avril (14)

- animation de la qualité des données
  - activité récurrente de suivi des opérateurs
  - accord de mise en production pour les opérateurs validés (Atlante, Engie)
  - extension des critères de validation (pdc par station, station par localisation, aménageur par unité d'exploitation)
  - outil de suivi du processus d'intégration des opérateurs
- documentation
  - extension FAQ
  - modèle de données
- calcul des certificats TIRUERT
  - analyse des données à extraire
- indicateurs
  - activation des fonctions d'historisation sur Prefect (indicateurs e4, i1, i4, i7, t1, u5, u6, u9, u10, u11, u12, up)
  - indicateurs historisés sur MetaBase

## Activités mars (14)

- animation de la qualité des données
  - activité récurrente de suivi des opérateurs
  - accord de mise en production pour les opérateurs validés (Powerdot, EVzen)
  - intégration de la fraicheur des données dans les critères de validation
  - initialisation de la documentation d'une FAQ
- indicateurs
  - activation des fonctions d'historisation sur Prefect
  - premier indicateur historisé sur la base de production
  - fonction de changement d'échelle de temps pour l'historisation (up)
  - indicateurs qualité de service

## Activités Février (12,5)

- animation de la qualité des données
  - activité récurrente de suivi des opérateurs
  - formalisation de l'accord de mise en production des données opérateurs
  - accord de mise en production pour Tesla
  - étude avec le PAN de l'impact du futur modèle de données européen
- outil d'analyse réseau
  - adaptation de l'outil au double-sens
  - intégration des aires de services BD CARTO
  - affectation du sens aux aires de service
- indicateurs
  - utilisation de la vue statique
  - utilitaire de transfert des indicateurs de staging vers production
  - activation des indicateurs de production

## Activités Janvier (12,5)

- animation de la qualité des données
  - activité récurrente de suivi des opérateurs
  - proposition d'un accord de mise en production pour les opérateurs
- analyse
  - partage d'un support d'analyse du modèle de données proposée par l'AFIR
  - réflexion/lecture sur les RLD (gestionnaires de réseaux locaux de distribution)
- indicateurs
  - tableau de suivi partagé sur Resana
  - intégration des indicateurs dynamiques dans le dashboard open-data
  - création de l'historisation Prefect (voir PR) des :
    - indicateurs statiques i4, i7
    - indicateurs d'usage u5, u6, u9, u10, u11, u12, u13
    - indicateurs Tiruert c1, c2

## Activités Décembre (11)

- indicateurs
  - identification des stations Qualicharge présente sur autoroute
  - optimisation des performances des requêtes liées aux status
  - analyse de la saturation des stations autoroute
  - formalisation des indicateurs de qualité de service (définition, calcul, historisation)
  - analyse de la correspondance entre les structures de données Qualicharge et OCPI
- analyse des données
  - outil d'analyse de la cohérence des données status par rapport aux sessions
  - généralisation des outils de contrôle (28 types de contrôles paramétrés)
- animation de la qualité des données
  - bilan hebdomadaire de l'évolution des données
  - animation avec chaque opérateur de la qualité des données mises à disposition
  - intégration au dashboard "error-data-tracking" (et tableau de suivi) des nouveaux contrôles
- outil d'analyse réseau
  - tests de l'adaptation du modèle au double sens (tronçons, noeuds, stations)

## Activités Novembre

- outil d'analyse réseau:
  - étude de l'intégration de la règlementation AFIR
  - fonctions de calcul et de restitution des indicateurs AFIR (pour intégration dans les indicateurs)
  - étude de la prise en compte du double-sens dans la modèlisation du réseau
- indicateurs
  - étude de l'intégration des status / sessions
  - calcul des indicateurs de saturation des stations et de disponibilité des pdc
  - mise en place d'un dashboard open-data (données statiques)
  - mise en place du suivi des données erronées (dashboard error-data-tracking + tableau de suivi)
  - mise en place d'un dashboard pour les données dynamiques (première version)
- analyse des données status/session 2023
  - reprise des données 2023
  - mise au format QualiCharge

## Activités Octobre

- études des indicateurs AFIR
- outil d'analyse réseau:
  - intégration des aires autoroutes (ASFA)
  - intégration des échangeurs et rond-points (ROUTE500)
  - gestion des sous-réseaux autoroute et RTE-T central
  - intégration des stations IRVE aux noeuds routiers
  - stockage des réseaux par fichier
  - repository dédié
  - intégration des indicateurs AFIR
- indicateurs
  - historisation indicateur t1 (reprise fonction existante pour i1)
  - fonction de changement d'échelle d'historisation
- analyse des données status/session
  - préparation (activités à réaliser, reprise des données)

## Activités Septembre

- ajout des indicateurs t8, t9 (opérateurs), i2, i5, i8 (ratio 100 000 hab.), i3, i6, i9 (ratio 100 km2)
- principes d'historisation (définition et tests)
- définition d'une solution pour les indicateurs liés aux données historisées
- fonction d'analyse de la saturation des stations autoroute
- publication 'pip' de l'extension aux données géospatiales de 'NetworkX'

## Activité Aout

- génération de l'ensemble des fonds de carte MetaBase
- definition du premier lot d'indicateur (CDC + priorités)
- outil de génération des requêtes
- requêtes du premier lot d'indicateur
- validation des requêtes sur Metabase
- reprise de l'outil d'analyse du réseau des stations d'autoroute 'compliance-AFIR'

## Activité Juillet

- outil d'import des données 'transport' (partiel - standby)
- génération de fonds de carte Metabase (partiel)
- test des API MetaBase
- outil d'identification du code commune à partir des coordonnées (idem ST-contains)
- gestion des indicateurs (PR)
- prise de connaissance indicateur global réseau routier
