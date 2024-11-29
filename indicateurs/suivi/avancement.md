# Avancement

## En cours

- indicateurs
  - intégration des indicateurs autoroute dans le dashboard open-data
  - optimisation des requêtes liées aux status
  - intégration facteur de charge dans le dashboard open-data
  - création indicateurs d'état e1, temporels d1, d2 et d'autoroutes a1, a2, a3, a4
  - historisation indicateurs t5, t7, t8, i4, i7, e1, p0-p6, r0-r8
- analyse des données
  - outil d'analyse de la cohérence des données status par rapport aux sessions
  - bilan hebdomadaire des données erronées et de l'évolution des données statiques et dynamiques
- outil d'analyse réseau
  - prise en compte du double sens (tronçons, noeuds, stations)
  - adaptation de l'outil au double-sens
  - optimisation de la fonction de calcul de maillage par noeuds
  - étude basculement ROUTE500 vers BDCARTO

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
