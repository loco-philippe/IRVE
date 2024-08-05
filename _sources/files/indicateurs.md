# Indicateurs de référence

Les indicateurs de référence sont les indicateurs générés et actualisés par QualiCharge.

## Types d'indicateurs

Deux types d'indicateurs sont définis:

- indicateurs d'infrastructure: Ils décrivent le parc installé (évolution temporelle, répartition géographiques, caratéristiques, dimensionnement)
- indicateurs d'usage: Ils décrivent l'utilisation effective des infrastructures (qualité de service, volumétrie, répartition)

## Structuration

Les indicateurs peuvent être:

- dynamiques (générés dynamiquement à partir de l'état courant des données),
- historisés (générés périodiquement mais accessibles également sous forme dynamique)

Quatre formats sont retenus:

- scalaire (une valeur numérique)
- temporel (une liste de valeurs associées à un index temporel),
- catégorie (une liste de valeurs associées à un index catégorisé)
- multiple (muylti-dimensionnel: une liste de valeurs associées à plusieurs index)

## Catalogue

Le tableau ci-dessous regroupe les indicateurs

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
