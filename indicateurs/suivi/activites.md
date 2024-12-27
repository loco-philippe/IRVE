# Roadmap et activités à planifier

## Roadmap

Proposition :

- V0 : déploiement pour tous les opérateurs cibles 1 et 2 fin T1 2025
  - plateforme de production à créer (+ outils d'exploitation)
  - fonctions d'historisation à compléter
  - indicateurs à compléter
  - interface RTE et aide au contrôle de la TIRUERT
  - processus de validation des opérateurs pour mise en production (utilisation API, cohérence des données, administratif)
  - documentation à construire

- V1 : nouvelle version (évolution modèle de données) fin T2 2025
  - anglicisation des noms de champs ?
  - évolution europe
  - cycle de vie (déclaré / en activité / désactivé)
  - ajout de contrôles et règles supplémentaires
  - entité pdl à créer ?
  - entité pool à créer ou "station de stations" ?
  - identification stations autoroute et stations RTE-T

- V2 : version fin T3 2025
  - intégration des indicateurs AFIR et autoroute
  - automatisation calcul/contrôle TIRUERT
  - analyses de données
  - ouverture open-data ?

- V3 : version fin 2025
  - à définir

- intégration de fonctions spécifiques à chaque version en fonction de l'avancement

## Indicateurs

### Indicateurs infrastructure

Les activités à mener sont :

| activité             | objet                                       | priorité | objectif  |
| -------------------- | ------------------------------------------- | -------- | --------- |
| niveaux de puissance | Liste de valeurs à valider                  | 2        | ok ?      |
| indicateur t7        | Densité EPCI (nb EPCI avec / nb EPCI total) | 3        | à décider |
| extensions           | Autres catégories (ex accessibilité)        | 3        | à décider |

### Indicateurs réseau

Les activités à mener sont :

| activité       | objet                                  | priorité | objectif |
| -------------- | -------------------------------------- | -------- | -------- |
| identification | Clarifier la gestion autoroute/RTET    | 1        | V1       |
| acquisition    | intégration des données analyse réseau | 2        | V1       |
| a1 - a6        | indicateurs globaux                    | 1        | V1       |
| a7 - a9        | indicateurs par station                | 2        | V1       |

### Indicateurs d'usage

Les activités à mener sont :

| activité             | objet                                               | priorité | objectif |
| -------------------- | --------------------------------------------------- | -------- | -------- |
| identification       | Clarifier la typologie status / session             | 1        | ok       |
| définition           | Clarifier les notion de disponibilité / utilisation | 1        | ok       |
| indicateurs u1 - u12 | indicateurs quantitatifs                            | 2 - 3    | V0       |
| indicateurs q1 - q5  | indicateurs qualité de service                      | 2 - 3    | V0       |

### Indicateurs temporels

Les activités à mener sont :

| activité      | objet                                          | priorité | objectif  |
| ------------- | ---------------------------------------------- | -------- | --------- |
| historisation | Clarifier les données 'extras' des indicateurs | 1        | V0 |
| prefect       | Intégration prefect des indicateurs            | 1        | V0        |
| d1 - d5       | indicateurs                                    | 1 - 3    | V0        |

### Indicateurs AFIR

Les activités à mener sont :

| activité          | objet                       | priorité | objectif |
| ----------------- | --------------------------- | -------- | -------- |
| définition        | Clarifier le mode de calcul | 1        | ok       |
| définition        | Définir les indicateurs     | 1        | ok       |
| indicateurs p0-p6 | liste des stations RTE-T    | 1        | V1       |
| indicateurs r1-r8 | ratio AFIR                  | 1        | V2       |

### Indicateurs d'état

Les activités à mener sont :

| activité | objet              | priorité | objectif |
| -------- | ------------------ | -------- | -------- |
| e1 - e4  | Listes de stations | 2        | V1       |

## Analyse réseau

### Réseau RTE-T

Les activités à mener sont :

| activité         | objet                                          | priorité | objectif  |
| ---------------- | ---------------------------------------------- | -------- | --------- |
| réseau           | Passage à un réseau 'digraph'                  | 1        | V1        |
| troncons         | Fusion des troncons linéaires                  | 1        | V1        |
| aires de service | BDcarto (complément au données ASFA)           | 2        | V1        |
| aires de service | Identification du sens                         | 2        | V1        |
| échangeurs       | passage de ROUTE500 à BDcarto                  | 2        | V1        |
| échangeurs       | Identification du sens                         | 2        | V1        |
| rond-point       | passage de ROUTE500 à BDcarto                  | 2        | V2        |
| rond-point       | Identification du sens                         | 2        | V2        |
| troncons         | Actualisation 'roads_GL2017'                   | 2        | à décider |
| carrefour        | Intégration                                    | 3        | à décider |
| doublons         | Suppression des doublons echangeurs-rond-point | 3        | à décider |

### Stations

Les activités à mener sont :

| activité | objet                         | priorité | objectif  |
| -------- | ----------------------------- | -------- | --------- |
| stations | gestion p_max, p_cum          | 1        | V1        |
| stations | Identification du sens        | 2        | V1        |
| stations | Intégration données transport | 3        | à décider |

### Analyse

Les activités à mener sont :

| activité | objet                                    | priorité | objectif |
| -------- | ---------------------------------------- | -------- | -------- |
| AFIR     | gestion des cas véhicule, core, échéance | 1        | V1       |
| AFIR     | méthode de calcul par noeuds             | 1        | V2       |
| AFIR     | calcul indicateur AFIR                   | 2        | V2       |
| AFIR     | indicateur AFIR mensuel                  | 3        | V2       |

## Status et sessions

Les activités à mener sont :

| activité     | objet                                                   | priorité | objectif  |
| ------------ | ------------------------------------------------------- | -------- | --------- |
| données 2023 | jeu de données unique (insert_bq_xxxx.ipynb)            | 1        | à décider |
| données 2023 | mapping des status                                      | 2        | à décider |
| données 2023 | Identifier les stations / mapping qualicharge           | 3        | à décider |
| données 2023 | calcul de disponibilité                                 | 2        | à décider |
| données 2023 | calcul de saturation (dispo station)                    | 4        | à décider |
| données 2023 | indicateur facteur de charge (consommée / consoimmable) | 3        | à décider |
