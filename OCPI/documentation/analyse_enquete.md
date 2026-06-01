# Initialisation des données des tarifs

## Analyse des données fournies par l'enquête


Bilan des données reçues:

| **Origine** | **structure**                             | **types**                               | **restrictions**                                       | **remarques**                                                                |
| ----------- | ----------------------------------------- | --------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------- |
| Citeos      | 5 elements                                | ENERGY,   TIME,   PARKING\_TIME         | time,   duration                                       |                                                                              |
| Zunder      | simple (1 element)   complexe 3 elements) | ENERGY                                  | time,   day                                            | pas de distinction REGULAR, AD\_HOC\_PAYMENT                                 |
| FastNed     | 1 element                                 | ENERGY                                  | non                                                    | REGULAR                                                                      |
| Atlante     | 1 element                                 | ENERGY                                  | power                                                  | Pas encore passé sous OCPI (mais prévu)                                      |
| Electra     | 1 element                                 | ENERGY                                  | non                                                    | structure complète   end\_date non fixée                                     |
| Driveco     | 2 elements                                | FLAT,   ENERGY,   TIME,   PARKING\_TIME | time,   duration,   parking\_time                      | ressemble à des exemples                                                     |
| Tesla       | 3 elements ou 7 (variation horaire)       | ENERGY,   CONGESTION\_TIME              | time,   day,   duration,   vehicule\_soc,   congestion | JSON de 28 000 lignes !! mais structure identique (simple) pour chaque tarif |
| IE Charge   |                                           |                                         |                                                        | demande transmise à Dassine IKDOUMI                                          |
| Shell       | 7 elements                                | ENERGY                                  | time,   duration,   day                                | se résume à 1 élément simple de type ENERGY. Attente retour Cindy            |
| EV cars     |                                           |                                         |                                                        | demande transmise en interne                                                 |
| Total       | 2 - 6 elements                            | ENERGY,   TIME,   PARKING\_TIME         | time,   date,   duration                               | 10 exemples complets. Utilisation de max\_price. end\_date non fixée.        |
| allego      |                                           |                                         |                                                        | relancé                                                                      |
| lidl        | 1 element                                 | ENERGY                                  | non                                                    | pas de gestion à date                                                        |
| engie       |                                           | ENERGY,   TIME,   PARKING\_TIME         | pas de restrictions                                    | CSV envoyé (pas de JSON encore dispo)                                        |
| plug-inn    | 3 elements                                | ENERGY,   PARKING\_TIME                 | duration                                               | structure complète                                                           |
| powerdot    | 1 element                                 | ENERGY                                  | non                                                    | pas de gestion à date                                                        |
| ionity      |                                           |                                         |                                                        | en cours (Dennis Möllmann)                                                   |
| bp          |                                           |                                         |                                                        | relancé                                                                      |
| obornes     | 1 element                                 | ENERGY                                  | non                                                    | type non précisé                                                             |

## Typologie des données 

- 1 : données complètes 
  - tarifs au format OCPI
  - tous les tarifs fournis
  - liens avec les pdc fournis
- 2 : données tarifs complètes
  - tarifs au format OCPI
  - tous les tarifs fournis
- 3 : données tarifs complètes à corriger
  - tarifs au format OCPI à corriger
  - tous les tarifs fournis
- 4 : données tarifs incomplètes
  - exemples de tarifs au format OCPI
- 5 : données tarifs incomplètes à corriger
  - exemples de tarifs au format OCPI à corriger
- 6 : données tarifs hors OCPI
  - exemples de tarifs hors format OCPI
- 7 : pas de données

## Actions à mener 

- convertion des tarifs en dataframe Qualicharge au format Parquet (rapide)
- convertion des liens tarif-pdc en dataframe Qualicharge au format parquet (rapide)
- script de chargement des tables tarifs et pointdechargetarif (à faire par erwan)
- par opérateur
  - fourniture / actualisation / correction / extension de leurs tarifs (suivant les cas)
  - fourniture / actualisation / correction / extension des liens pdc-tarif (suivant les cas)

## Données disponibles
  - 1 : Tesla (262 tarifs et stations)
  - 2 : 
  - 3 : Total (65 tarifs) : corrections sur $date, _id, vat=0.2, type=REGULAR
  - 4 : 
    - Powerdot (3 tarifs représentatifs), 
    - Fastned (1 exemple représentatif à maj via eco-movement)
  - 5 : 
    - Electra (1 tarif à prix fixe, variable à fournir) : corrections sur vat=0
    - Cieos (1 tarif) : champs obligatoires manquant (country_code, party_id)
    - Zunder (1 simple, 1 complexe) : correction à faire (type REGULAR indiqué) 
    - Driveco (85 exemples non représentatifs) : champs obligatoires manquant (country_code, party_id)
    - Shell (1 exemple non représentatif)
  - 6 :
    - Atlante (format spécifique)
    - Engie (format CSV)
  - 7 : Allego, EVcars, NW IECharge




## TESLA

### données

2 fichiers (locations et tariffs)

- locations : 262 stations
- tariffs : 262 tarifs

Exemple

- locations/evses/evse_id : "FR\*TSL\*EA4QY2C"
  - location/evses/connectors/tariff_ids : "5fa1c37d-9aa9-4778-805b-8a1c1299765d" (id du tariff dans le fichier des tarifs)
- tariffs/5fa1c37d-9aa9-4778-805b-8a1c1299765d :
  - "start_date_time": "2026-03-25T23:00:00Z"
  - "last_updated": "2026-03-26T01:20:54Z"
- qualicharge : FRTSLEA4QY2C (id_pdc_itinerance)

### prise en compte

- convertion des tarifs en dataframe Qualicharge au format Parquet
- convertion des liens tarif-pdc en dataframe qualicharge au format parquet
- demande à Tesla d'une version actualisée
