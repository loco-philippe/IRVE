# Indicateurs de  référence

Les indicateurs de référence sont les indicateurs générés et actualisés par QualiCharge.

## Structuration

Les indicateurs sont constitués d'une liste de valeurs. On distingue les types suivants :

- scalaire (une seule valeur numérique)
- temporel (une liste de valeurs associées à un index temporel),
- catégorie (une liste de valeurs associées à un index catégoriel)
- multiple (multi-dimensionnel: une liste de valeurs associées à plusieurs index)

Les indicateurs peuvent être:

- dynamiques : générés dynamiquement à partir de l'état courant des données,
- historisés : générés périodiquement (heure, jour, mois ou année) et stockés pour être réutilisés.

Par exemple, le nombre de points de recharge est un indicateur dynamique mais si l'on souhaite disposer d'un indicateur de l'évolution du nombre de points de recharges, celui-ci doit être historisé.

Un indicateur peut être visualisé suivant différentes représentations. Par exemple, un indicateur de type 'catégorie' peut être représenté par :

- un tableau à deux colonnes,
- un diagramme en barres,
- un diagramme circulaire,
- une carte choroplèthe (si l'index de l'indicateur est associé à une carte).

Un indicateur historisé peut être représenté en fonction de sa dimension temporelle. Par exemple:

- une moyenne sur une période,
- un historique sur une période,
- état courant.

Le mode de représentation d'un indicateur n'est pas abordé.

## Exemple - baromètre AVERE

Les indicateurs présentés dans le {term}`Baromètre AVERE` sont les suivants :

- chiffres clés :
  - Nombre total de points de recharge ouverts au public
  - Taux d'évolution sur 12 mois
  - Taux de disponibilité moyen d'un point de charge
  - Points de recharge en moyenne pour 100 000 habitants
- répartition spatiale (cartes choroplèthes) :
  - Nombre de stations de recharge par région
  - Nombre de points de recharge par région
  - Puissance totale installée par région
- typologie (diagrammes circulaires) :
  - Répartition des points de recharge par type de site d’implantation
  - Recharge selon la catégorie de puissance
  - Recharge selon la catégorie de puissance par région (diagramme en barres empilées)
- évolution (diagramme en barre)
  - Evolution du nombre de points de recharge par année
  - Évolution du nombre de points de recharge par mois
- usage (diagramme en barres)
  - Nombre de sessions moyen mensuel par point de recharge
  - Taux de disponibilité du mois par catégorie de puissance

## Types d'indicateurs

Trois types d'indicateurs sont définis:

- indicateurs d'infrastructure : Ils décrivent le parc installé (évolution temporelle, répartition géographiques, caratéristiques, dimensionnement)
- indicateurs d'usage : Ils décrivent l'utilisation effective des infrastructures (qualité de service, volumétrie, répartition)
- indicateurs étendus : Ils concernent les indicateurs obtenus avec des jeux de données en lien (ex. relevés ENEDIS)

:::{note}

Les indicateurs d'exploitation (liés aux opérateurs et aménageurs et enseignes) ainsi que les indicateurs liés à des attributs spécifiques (ex. accès deux roues, période d'ouverture, accès handicapés...) sont à ajouter.

:::

## Indicateurs d'infrastructure

### Infrastructure - typologie

Objectif :

- analyse de la typologie (comparaison des ratios)

| id    | nom                                                       | format    | type  | nature             |
| ----- | --------------------------------------------------------- | --------- | ----- | ------------------ |
| t1-xx | Nombre de points de recharge par niveau de puissance      | catégorie | infra | mensuel (national) |
| t2-xx | Pourcentage de points de recharge par niveau de puissance | catégorie | infra | dynamique          |
| t3-xx | Nombre de points de recharge par station                  | catégorie | infra | dynamique          |
| t4-xx | Pourcentage de points de recharge par station             | catégorie | infra | dynamique          |
| t5-xx | Nombre de stations par type d'implantation                | catégorie | infra | mensuel (national) |
| t6-xx | Pourcentage de stations par type d'implantation           | catégorie | infra | dynamique          |
| t7-xx | Densité EPCI (nb EPCI avec / nb EPCI total)               | scalaire  | infra | mensuel (national) |

xx : national, national hors autoroutes, région et département (hors autoroutes), autoroutes

### Infrastructure - quantitatif

Objectif:

- analyse de la répartition géographique (comparaison des ratios)

| id    | nom                                              | format    | type  | nature    |
| ----- | ------------------------------------------------ | --------- | ----- | --------- |
| i1-xx | Nombre de points de recharge ouverts au public   | scalaire  | infra | mensuel   |
| i2-xx | Ratio pour 100 000 habitants                     | scalaire  | infra | dynamique |
| i3-xx | Ratio pour 100 km2                               | scalaire  | infra | dynamique |
| i4-xx | Nombre de stations de recharge ouverts au public | catégorie | infra | mensuel   |
| i5-xx | Ratio pour 100 000 habitants                     | scalaire  | infra | dynamique |
| i6-xx | Ratio pour 100 km2                               | scalaire  | infra | dynamique |
| i7-xx | Puissance installée                              | catégorie | infra | mensuel   |
| i8-xx | Ratio pour 100 000 habitants                     | scalaire  | infra | dynamique |
| i9-xx | Ratio pour 100 km2                               | scalaire  | infra | dynamique |

xx : national, national hors autoroutes, région et département (hors autoroutes), autoroutes

## Indicateurs d'infrastructure du réseau autoroutes

Objectif:

- analyse du niveau d'équipement des stations
- analyse de la couverture des trajets nationaux
- analyse de la répartition par station

### Indicateurs globaux

| id  | nom                                                                | format    | type  | nature    |
| --- | ------------------------------------------------------------------ | --------- | ----- | --------- |
| a1  | Nombre de points de recharge                                       | scalaire  | infra | mensuel   |
| a2  | Nombre de stations de recharge                                     | scalaire  | infra | mensuel   |
| a3  | Puissance installée                                                | scalaire  | infra | mensuel   |
| a4  | Puissance par point de charge                                      | scalaire  | infra | dynamique |
| a5  | Densité des stations équipées (nb stations équipées / nb stations) | scalaire  | infra | mensuel   |
| a6  | Distance moyenne inter-station de recharge                         | catégorie | infra | mensuel   |

ex. Suivi du déploiement des IRVE dans les stations (nécessite de disposer du nombre de stations).
ex. Suivi temporel de la distance interstation (utilisation du graphe pour calculer les distances de recharge associée à chaque station).

### Indicateurs par station

| id  | nom                                    | format    | type  | nature    |
| --- | -------------------------------------- | --------- | ----- | --------- |
| a7  | Puissance installée par station        | catégorie | infra | dynamique |
| a8  | Nombre de points de charge par station | catégorie | infra | dynamique |
| a9  | Distance de recharge par station       | catégorie | infra | dynamique |

ex. Analyse de la distance interstation (zones blanches ).

## Indicateurs d'usage

### Usage - quantitatif

- analyse de l'évolution temporelle de l'utilisation

| id      | nom                                         | format    | type  | nature                       |
| ------- | ------------------------------------------- | --------- | ----- | ---------------------------- |
| u1-xx-y | Nombre de point de charge actif             | scalaire  | usage | mensuel (national)           |
| u2-xx-y | Pourcentage de point de charge actif        | scalaire  | usage | dynamique                    |
| u3-xx-y | Nombre de sessions                          | scalaire  | usage | quotidien/mensuel (national) |
| u4-xx-y | Répartition horaire des sessions            | scalaire  | usage | dynamique                    |
| u5-xx-y | Répartition horaire de l'énergie distribuée | catégorie | usage | dynamique                    |

xx : national, national hors autoroutes, région et département (hors autoroutes), autoroutes
y : jour, mois, année

Les sessions sont par nature historisées.
L'historisation du nombre de sessions est à définir en fonction de l'historique conservé des sessions.

ex. Analyse du profil horaire de l'énergie fournie en fonction des périodes et de la localisation.

### Usage - qualité de service

- analyse de la disponibilité et de l'utilisation des points de recharge

| id      | nom                                                           | format   | type  | nature    |
| ------- | ------------------------------------------------------------- | -------- | ----- | --------- |
| q1-xx-y | Taux de disponibilité d'un point de charge actif              | scalaire | usage | quotidien |
| q2-xx-y | Taux d'utilisation d'un point de charge actif                 | scalaire | usage | quotidien |
| q3-xx-y | Taux de sessions réussies d'un point de charge actif          | scalaire | usage | dynamique |
| q4-xx-y | Taux de saturation d'une station                              | scalaire | usage | dynamique |
| q5-xx-y | Taux mensuel de points de recharge avec indisponibilité > 7 j | scalaire | usage | mensuel   |

xx : national, national hors autoroutes, région et département (hors autoroutes), autoroutes
y : jour, mois, année

:::{note}

Les indicateurs suivants ont été formalisés par l'AFIREV:

- {term}`Taux de sessions de recharge réussies (définition AFIREV)`
- {term}`Taux de disponibilité des points de recharge (définition AFIREV)`
- {term}`Taux de bon fonctionnement des systèmes informatiques (définition AFIREV)`
- {term}`Taux de points de charge disponibles 99% du temps (définition AFIREV)`
- {term}`Taux de points de charge indisponibles depuis plus de 7 jours (définition AFIREV)`

:::

:::{note}

- le mode de calcul du taux de disponibilité et du taux d'utilisation est précisé dans le chapitre lié aux [états des points de recharge](./etats.md).
:::

## Indicateurs étendus

Ils concernent le couplage des données avec des jeux de données complémentaires (à définir dans un second temps):

- couplage consommation / trafic
- couplage nombre de véhicules électriques vendus/immatriculés
- couplage consommation / relevés ENEDIS des points de livraison

## Historisation des données

L'historisation des données est prévue par un stockage de données sous un format simple (valeur numérique) ou structuré (JSON) dans une table intégrant un index temporel.

L'exemple ci-dessous montre l'enregistrement du nombre de stations, de points de charge et la puissance installée pour chaque commune, département, opérateur et région.

```json
{
    "timestamp": "now",
    "totals": {
        "stations": 12424,
        "psoc": 2312314,
        "power": 1e19
    },
    "counts": {
        "city": [
            {
                "code_insee": "01311",
                "stations": 12,
                "poc": 132,
                "power": 30000,
            },
            {
                "code_insee": "13411",
                "stations": 15,
                "poc": 132,
                "power": 30000
            }
        ],
        "department": [
            {
                "code_insee": "01",
                "stations": 12,
                "poc": 132,
                "power": 30000
            },
            {
                "code_insee": "13",
                "stations": 15,
                "poc": 132,
                "power": 30000
            }
        ],
        "region": [
            {
                "code_insee": "13",
                "stations": 15
                "poc": 132,
                "power": 30000
            },            
        ],
        "operational_unit": [
            {
                "name": "FRFAS",
                "stations": 12,
                "poc": 142,
                "power": 30000
            },
            {
                "name": "FRS77",
                "stations": 114,
                "poc": 1445,
                "power": 30000
            },
        ]
    }
}
```

```
# iStatic table database fields
timestamp: date time
total_stations: int
total_poc: int
total_power: long float
city: json
department: json
region: json
operational_unit: json
```
