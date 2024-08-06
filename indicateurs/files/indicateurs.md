# Indicateurs de  référence

Les indicateurs de référence sont les indicateurs générés et actualisés par QualiCharge.

## Structuration

Les indicateurs peuvent être:

- dynamiques (générés dynamiquement à partir de l'état courant des données),
- historisés (générés périodiquement mais accessibles également sous forme dynamique)

Quatre formats sont retenus:

- scalaire (une valeur numérique)
- temporel (une liste de valeurs associées à un index temporel),
- catégorie (une liste de valeurs associées à un index catégorisé)
- multiple (muylti-dimensionnel: une liste de valeurs associées à plusieurs index)

## Types d'indicateurs

Le tableau ci-dessous regroupe les indicateurs

Deux types d'indicateurs sont définis:

- indicateurs d'infrastructure: Ils décrivent le parc installé (évolution temporelle, répartition géographiques, caratéristiques, dimensionnement)
- indicateurs d'usage: Ils décrivent l'utilisation effective des infrastructures (qualité de service, volumétrie, répartition)

## Infrastructure
### Infrastructure - typologie

Objectif :

- Indicateurs généraux, référence nationale

| id  | nom                                                  | format    | type  | nature    |
| --- | ---------------------------------------------------- | --------- | ----- | --------- |
| t1  | Nombre de points de recharge par niveau de puissance | catégorie | infra | dynamique |
| t2  | Nombre de points de recharge par station             | catégorie | infra | dynamique |
| t3  | Nombre de stations par type d'implantation             | catégorie | infra | dynamique |

### Infrastructure - répartition

Objectif:

- analyse de la répartition géographique (comparaison des ratios)

| id    | nom                                              | format    | type  | nature    |
| ----- | ------------------------------------------------ | --------- | ----- | --------- |
| i1-xx | Nombre de points de recharge ouverts au public   | scalaire  | infra | historisé |
| i2-xx | Ratio pour 100 000 habitants                     | scalaire  | infra | dynamique |
| i3-xx | Ratio pour 100 km2                               | scalaire  | infra | dynamique |
| i4-xx | Nombre de stations de recharge ouverts au public | catégorie | infra | dynamique |
| i5-xx | Ratio pour 100 000 habitants                     | scalaire  | infra | dynamique |
| i6-xx | Ratio pour 100 km2                               | scalaire  | infra | dynamique |
| i7-xx | Puissance installée                              | catégorie | infra | dynamique |
| i8-xx | Ratio pour 100 000 habitants                     | scalaire  | infra | dynamique |
| i9-xx | Ratio pour 100 km2                               | scalaire  | infra | dynamique |

xx : national, national hors autoroutes, région et département (hors autoroutes)

## Infrastructure réseau autoroutes

Objectif:

- analyse du niveau d'équipement des stations
- analyse de la couverture des trajets nationaux
- analyse de la répartition par station

### Indicateurs globaux

| id  | nom                                      | format    | type  | nature    |
| --- | ---------------------------------------- | --------- | ----- | --------- |
| a1  | Nombre de points de recharge             | scalaire  | infra | historisé |
| a2  | Nombre de stations de recharge           | scalaire  | infra | historisé |
| a3  | Puissance installée                      | scalaire  | infra | historisé |
| a4  | Puissance par point de charge            |    scalair       |       |           |
| a4  | Taux d'équipement des stations         |    scalaire       |       |           |

### Indicateurs par station

| id  | nom                                      | format    | type  | nature    |
| --- | ---------------------------------------- | --------- | ----- | --------- |
| a3  | Puissance installée par station                      | scalaire  | infra | historisé |
| a4  | Nombre de points de charge par station   | catégorie |       |           |
| a4  | Distance de recharge |           |       |           |

ex. Analyse par histogramme


| id  | nom                                                             | format    | type  | nature    |
| --- | --------------------------------------------------------------- | --------- | ----- | --------- |
| i1  | Nombre total de points de recharge ouverts au public            | scalaire  | infra | historisé |
| i3  | Taux de disponibilité moyen d'un point de charge                | scalaire  | usage | dynamique |
| i4  | Points de recharge en moyenne pour 100 000 habitants            | scalaire  | infra | dynamique |
| i5  | Nombre de stations de recharge par région                       | catégorie | infra | dynamique |
| i6  | Nombre de points de recharge par région                         | catégorie | infra | dynamique |
| i7  | Puissance totale installée par région                           | catégorie | infra | dynamique |
| i8  | Nombre de points de recharge par site d’implantation            | catégorie | infra | dynamique |
| i9  | Nombre de points de recharge par catégorie de puissance         | catégorie | infra | dynamique |
| i10 | Taux de sessions de recharge réussies                           | scalaire  | usage | dynamique |
| i11 | Taux de disponibilité des points de recharge                    | scalaire  | usage | dynamique |
| i12 | Taux de points de recharge indisponibles depuis plus de 7 jours | scalaire  | usage | dynamique |
