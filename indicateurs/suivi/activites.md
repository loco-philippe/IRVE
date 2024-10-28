# Activités à planifier

## Indicateurs

### Indicateurs infrastructure

Les activités à mener sont :

| activité             | objet                                       | priorité | objectif  |
| -------------------- | ------------------------------------------- | -------- | --------- |
| indicateur t7        | Densité EPCI (nb EPCI avec / nb EPCI total) | 3        | à décider |
| niveaux de puissance | Liste de valeurs à valider                  | 2        | à décider |
| extensions           | Autres catégories (ex accessibilité)        | 3        | à décider |

### Indicateurs réseau

Les activités à mener sont :

| activité       | objet                                  | priorité | objectif  |
| -------------- | -------------------------------------- | -------- | --------- |
| identification | Clarifier la gestion autoroute/RTET    | 1        | à décider |
| acquisition    | intégration des données analyse réseau | 2        | à décider |
| a1 - a6        | indicateurs globaux                    | 1        | en cours  |
| a7 - a9        | indicateurs par station                | 2        | en cours  |

### Indicateurs d'usage

Les activités à mener sont :

| activité             | objet                                               | priorité | objectif  |
| -------------------- | --------------------------------------------------- | -------- | --------- |
| identification       | Clarifier la typologie status / session             | 1        | à décider |
| définition           | Clarifier les notion de disponibilité / utilisation | 1        | à décider |
| intégration          | Prise en compte TimeScale                           | 1        | à décider |
| indicateurs u1 - u4  | indicateurs quantitatifs                            | 2 - 3    | à décider |
| indicateurs q1 - q10 | indicateurs qualité de service                      | 2 - 3    | à décider |

### Indicateurs temporels

Les activités à mener sont :

| activité      | objet                                          | priorité | objectif  |
| ------------- | ---------------------------------------------- | -------- | --------- |
| historisation | Clarifier les données 'extras' des indicateurs | 1        | à décider |
| prefect       | Intégration prefect des indicateurs            | 1        | à décider |
| d1 - d5       | indicateurs                                    | 1 - 3    | à décider |

### Indicateurs AFIR

Les activités à mener sont :

| activité   | objet                       | priorité | objectif  |
| ---------- | --------------------------- | -------- | --------- |
| définition | Clarifier le mode de calcul | 1        | à engager |
| définition | Définir les indicateurs     | 1        | à décider |
| xxx        | construire les indicateurs  | 1 - 3    | à décider |

### Indicateurs d'état

Les activités à mener sont :

| activité | objet              | priorité | objectif  |
| -------- | ------------------ | -------- | --------- |
| e1 - e2  | Listes de stations | 2        | à décider |

## Analyse réseau

### Réseau RTE-T

Les activités à mener sont :

| activité         | objet                                          | priorité | objectif  |
| ---------------- | ---------------------------------------------- | -------- | --------- |
| réseau           | Passage à un réseau 'digraph'                  | 1        | à engager |
| troncons         | Actualisation 'roads_GL2017'                   | 2        | à décider |
| troncons         | Fusion des troncons linéaires                  | 1        | à engager |
| aires de service | BDcarto (complément au données ASFA)           | 2        | à décider |
| aires de service | Identification du sens                         | 2        | à décider |
| échangeurs       | passage de ROUTE500 à BDcarto                  | 2        | à décider |
| échangeurs       | Identification du sens                         | 2        | à décider |
| rond-point       | passage de ROUTE500 à BDcarto                  | 2        | à décider |
| rond-point       | Identification du sens                         | 2        | à décider |
| carrefour        | Intégration                                    | 3        | à décider |
| doublons         | Suppression des doublons echangeurs-rond-point | 3        | à décider |

### Stations

Les activités à mener sont :

| activité | objet                         | priorité | objectif  |
| -------- | ----------------------------- | -------- | --------- |
| stations | Intégration données transport | 3        | à décider |
| stations | gestion p_max, p_cum          | 1        | à engager |
| stations | Identification du sens        | 2        | à décider |

### Analyse

Les activités à mener sont :

| activité | objet                                    | priorité | objectif  |
| -------- | ---------------------------------------- | -------- | --------- |
| AFIR     | méthode de calcul par noeuds             | 1        | à engager |
| AFIR     | gestion des cas véhicule, core, échéance | 1        | à engager |
| AFIR     | calcul indicateur AFIR                   | 2        | à engager |
| AFIR     | indicateur AFIR mensuel                  | 3        | à engager |

## Status et sessions

Les activités à mener sont :

| activité     | objet                                                   | priorité | objectif  |
| ------------ | ------------------------------------------------------- | -------- | --------- |
| données 2023 | jeu de données unique (insert_bq_xxxx.ipynb)            | 1        | à engager |
| données 2023 | mapping des status                                      | 2        | à engager |
| données 2023 | Identifier les stations / mapping qualicharge           | 3        | à engager |
| données 2023 | calcul de disponibilité                                 | 2        | à engager |
| données 2023 | calcul de saturation (dispo station)                    | 4        | à engager |
| données 2023 | indicateur facteur de charge (consommée / consoimmable) | 3        | à engager |
