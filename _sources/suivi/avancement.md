# Avancement

## En cours

- animation de la qualité des données
  - activité récurrente de suivi des opérateurs
- indicateurs
  - intégration des indicateurs autoroute dans le dashboard open-data
  - intégration des indicateurs de qualité de service dans le dashboard open-data
  - création des indicateurs liés à l'historisation 
    - indicateur d'état e1,
    - indicateurs temporels d1, d2
    - indicateurs autoroutes a1, a2, a3, a4
    - indicateurs AFIR p0-p6, r0-r8
    - indicateurs d'usage q12-q15
  - historisation des indicateurs statiques (t5, t7, t8, i4, i7)
  - historisation des indicateurs dynamiques (q1-q11)
- outil d'analyse réseau
  - adaptation de l'outil au double-sens
  - affectation du sens aux aires de service et échangeurs autoroutiers
  - optimisation de la fonction de calcul de maillage par noeuds
  - étude basculement ROUTE500 vers BDCARTO

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
