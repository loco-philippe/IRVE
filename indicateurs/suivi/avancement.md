# Avancement

## En cours

- animation de la qualité des données
  - activité récurrente de suivi des opérateurs
  - validation des flux opérateurs
  - extension FAQ
  - calcul des critères sur Prefect (automatisation des tests MetaBase)
- indicateurs
  - intégration des indicateurs autoroute dans le dashboard open-data
  - intégration des indicateurs de qualité de service dans le dashboard open-data
  - création des indicateurs liés à l'historisation 
    - indicateurs de densité i2, i3, i5, i6, i8, i9
    - indicateurs de typologie t6, t7
    - indicateurs d'état e1 - e4, p1 - p6
    - indicateurs TIRUERT c1, c2, c3
    - indicateurs autoroutes a1, a2, a3, a5
    - indicateurs AFIR p0-p6, r0-r8
    - indicateurs d'usage u4, u7, u8, u13
    - indicateurs de qualité de service q1, q2, q3, q4, q5
- analyse de la qualité de service (saturation, disponibilité, occupation)
  - méthodologie
  - définition des indicateurs
  - analyse de périodes à forte charge (ex. ponts de mai)
- outil d'analyse réseau
  - adaptation de l'outil au double-sens
  - affectation du sens aux aires de service et échangeurs autoroutiers
  - optimisation de la fonction de calcul de maillage par noeuds
  - étude basculement ROUTE500 vers BDCARTO

## Orientations juin (14)

- animation de la qualité des données
  - activité récurrente de suivi des opérateurs
  - validation de flux d'opérateurs (prévu: Bouygues, Electra, Izivia, Allego, TotalEnergies)
  - extension FAQ
  - calcul des critères sur Prefect (automatisation des tests MetaBase)
- outil d'analyse réseau
  - affectation du sens aux échangeurs autoroutiers
  - outil de paramétrage des jonctions et échangeurs
- analyse de la qualité de service (saturation, disponibilité, occupation)
  - méthodologie
  - analyse de périodes à forte charge (ex. ponts de mai)
- indicateurs
  - intégration des indicateurs de qualité de service
  - intégration des indicateurs TIRUERT

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
