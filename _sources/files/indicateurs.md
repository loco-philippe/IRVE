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

- Les indicateurs d'exploitation (liés aux opérateurs et aménageurs et enseignes) ne sont pas abordés
- à compléter avec les indicateurs spécifiques (ex. accès deux roues, période d'ouverture, accès handicapés...)

:::

## Indicateurs d'infrastructure

### Infrastructure - typologie

Objectif :

- analyse de la typologie géographique (comparaison des ratios)

| id    | nom                                                       | format    | type  | nature    |
| ----- | --------------------------------------------------------- | --------- | ----- | --------- |
| t1-xx | Nombre de points de recharge par niveau de puissance      | catégorie | infra | dynamique |
| t2-xx | Pourcentage de points de recharge par niveau de puissance | catégorie | infra | dynamique |
| t3-xx | Nombre de points de recharge par station                  | catégorie | infra | dynamique |
| t4-xx | Pourcentage de points de recharge par station             | catégorie | infra | dynamique |
| t5-xx | Nombre de stations par type d'implantation                | catégorie | infra | dynamique |
| t6-xx | Pourcentage de stations par type d'implantation           | catégorie | infra | dynamique |
| t7-xx | Densité EPCI (nb EPCI avec / nb EPCI total)               | scalaire  | infra | dynamique |

xx : national, national hors autoroutes, région et département (hors autoroutes), autoroutes

### Infrastructure - quantitatif

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

xx : national, national hors autoroutes, région et département (hors autoroutes), autoroutes

## Indicateurs d'infrastructure du réseau autoroutes

Objectif:

- analyse du niveau d'équipement des stations
- analyse de la couverture des trajets nationaux
- analyse de la répartition par station

### Indicateurs globaux

| id  | nom                                                                | format   | type  | nature    |
| --- | ------------------------------------------------------------------ | -------- | ----- | --------- |
| a1  | Nombre de points de recharge                                       | scalaire | infra | historisé |
| a2  | Nombre de stations de recharge                                     | scalaire | infra | historisé |
| a3  | Puissance installée                                                | scalaire | infra | historisé |
| a4  | Puissance par point de charge                                      | scalaire | infra |           |
| a5  | Densité des stations équipées (nb stations équipées / nb stations) | scalaire | infra |           |

ex. Suivi du déploiement des IRVE dans les stations.

### Indicateurs par station

| id  | nom                                    | format    | type  | nature    |
| --- | -------------------------------------- | --------- | ----- | --------- |
| a6  | Puissance installée par station        | scalaire  | infra | historisé |
| a7  | Nombre de points de charge par station | catégorie | infra |           |
| a8  | Distance de recharge par station       | scalaire  | infra |           |

ex. Suivi temporel de la distance interstation (utilisation du graphe pour calculer les distances de recharge associée à chaque station).

## Indicateurs d'usage

### Usage - quantitatif

- analyse de l'évolution temporelle de l'utilisation

| id      | nom                                         | format    | type  | nature    |
| ------- | ------------------------------------------- | --------- | ----- | --------- |
| u1-xx-y | Nombre de point de charge actif             | scalaire  | usage | historisé |
| u2-xx-y | Pourcentage de point de charge actif        | scalaire  | usage | historisé |
| u3-xx-y | Nombre de sessions                          | scalaire  | usage | historisé |
| u3-xx-y | Répartition horaire des sessions            | scalaire  | usage | historisé |
| u4-xx-y | Répartition horaire de l'énergie distribuée | catégorie | usage | historisé |

xx : national, national hors autoroutes, région et département (hors autoroutes), autoroutes
y : jour, mois, année

ex. Analyse du profil horaire de l'énergie fournie en fonction des périodes et de la localisation.

### Usage - qualité de service

- analyse de la disponibilité et de l'utilisation des points de recharge

| id      | nom                                                           | format   | type  | nature    |
| ------- | ------------------------------------------------------------- | -------- | ----- | --------- |
| q1-xx-y | Taux de disponibilité d'un point de charge actif              | scalaire | usage | dynamique |
| q2-xx-y | Taux d'utilisation d'un point de charge actif                 | scalaire | usage | dynamique |
| q3-xx-y | Taux de sessions réussies d'un point de charge actif          | scalaire | usage | dynamique |
| q2-xx-y | Taux de saturation d'une station                              | scalaire | usage | dynamique |
| q4-xx-y | Taux mensuel de points de recharge avec indisponibilité > 7 j | scalaire | usage | dynamique |

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

Couplage des données avec des jeux de données complémentaires:

- couplage consommation / trafic
- couplage nombre de véhicules électriques vendus/immatriculés
- couplage consommation / relevés ENEDIS des points de livraison
