# Indicateurs de  référence

Les indicateurs de référence sont les indicateurs générés et actualisés par QualiCharge.

## Présentation

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

Un [indicateur historisé](./historisation.md) peut être représenté en fonction de sa dimension temporelle. Par exemple:

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

## Structure des indicateurs

### Types d'indicateurs

Cinq types d'indicateurs sont définis:

- indicateurs d'infrastructure : Ils décrivent le parc installé (évolution temporelle, répartition géographiques, caratéristiques, dimensionnement)
- indicateurs d'usage : Ils décrivent l'utilisation effective des infrastructures (qualité de service, volumétrie, répartition)
- indicateurs temporels : Ils analysent l'évolution des deux catégories d'indicateurs précédent sur une période temporelle
- indicateurs d'état : Ils représentent un état d'une partie des données (ex. liste des stations du réseau autoroutier)
- indicateurs étendus : Ils concernent les indicateurs obtenus avec des jeux de données en lien (ex. relevés ENEDIS)

:::{note}

Les indicateurs d'exploitation (liés aux aménageurs et enseignes) ainsi que les indicateurs liés à des attributs spécifiques (ex. accès deux roues, période d'ouverture, accès handicapés...) sont à ajouter.

:::

### Codification des indicateurs

Les indicateurs sont codifiés par une chaine de caractères : *[type]-[périmètre]-[valeur de périmètre]-[level]*
ou bien pour les indicateurs temporels : *[type]-[périodicité]-[périmètre]-[valeur de périmètre]-[level]*
avec:

- type : identifiant du type d'indicateur (ex. 'i1' : nombre de points de recharge)
- période : périodicité des données utilisées
  - y : données annuelles
  - m : données mensuelles
  - w : données hebdomadaires
  - d : données quotidiennes
- périmètre et valeur de périmètre: sous ensemble des données sur lequel appliquer l'indicateur. Les périmètres actuellement définis sont les découpages administratifs :
  - 0: national (valeur : code 00 tout, 01 métropole, 02 DOM, 03 TOM, 04 métropole et DOM)
  - 1: région (valeur : code de la région)
  - 2: département (valeur : code du département)
  - 3: EPCI (valeur : code de l'EPCI)
  - 4: commune (valeur : code de la commune)
- level : niveau de découpage du résultat (découpage administratif - voir périmètre). Les valeurs associées à un 'level' sont dénommées 'target'.

Le périmètre par défaut est l'ensemble des données.

```{admonition} Exemples
- **t4-4-74012** : Pourcentage de stations par nombre de points de recharge (t4) pour la ville (4) d'Annemasse (74012)
- **i1-1-93** : Nombre de points de recharge (i1) pour la région (1) PACA (93)
- **i1-1-93-3** : Nombre de points de recharge (i1) pour la région (1) PACA (93) par EPCI (3)
- **i1-m-1-93-3** : Nombre de points de recharge (i1) mensuel (m) pour la région (1) PACA (93) par EPCI (3)
- **t1** : Nombre de points de recharge par niveau de puissance (t1) pour l'ensemble des données (pas de périmètre choisi)
- **e1** : liste des stations du réseau autoroutier (e1)
```

### Résultat des indicateurs

Le résultat d'un indicateur peut être représenté par une structure tabulaire composée des champs suivants :

- valeur : résultat de l'indicateur pour une catégorie et une target,
- valeur additionnelle : informations associées à la valeur
- catégorie (facultative) : décomposition associée à l'indicateur
- target (facultative) : découpage associé au level choisi

Le champ 'valeur additionnelle' est utilisé pour les données structurées associées au champ 'valeur'.
Ce champ est au format JSON et concerne les informations liées à l'historisation ainsi que les données des indicateurs d'état ou bioen les .

Si aucune catégorisation et aucun level ne sont définis, le résultat se réduit à une valeur,

```{admonition} Exemple
'i1' : le résultat est le nombre de points de recharge
```

Si uniquement une catégorisation est définie, le résultat est une liste de valeurs associées à chaque catégorie.

```{admonition} Exemple
't1' : le résultat est le nombre de points de recharge par niveau de puissance (catégorie)

| nb_pdc | p_range      |
| ------ | ------------ |
| 10892  | [15.0, 26.0) |
| 4807   | [175, 360.0) |
| 3282   | [65, 175.0)  |
| 2359   | [26, 65.0)   |
| 2157   | [0, 15.0)    |
| 25     | [360, None)  |
```

Si uniquement un level est défini, le résultat est une liste de valeurs associées à chaque target.

```{admonition} Exemple
i1-1-93-2 : Nombre de points de recharge (i1) pour la région (1) PACA (93) par département (2)
La target est ici le département (représenté par son code).

| nb_pdc | target |
| ------ | ------ |
| 473    | 13     |
| 450    | 06     |
| 175    | 83     |
| 170    | 84     |
| 105    | 04     |
| 57     | 05     |
```

Si une catégorisation et un level sont définis, le résultat est une liste de valeurs associées à chaque target et à chaque catégorie.

```{admonition} Exemple
t8-1-93-2 : Nombre de stations par opérateur (t8) pour la région (1) PACA (93) par département (2)
La 'target' est ici le département (représenté par son code) et la 'catégorie' est l'opérateur.

| nb_stat | nom_operateur                   | target |
| ------- | ------------------------------- | ------ |
| 273     | IZIVIA                          | 06     |
| 31      | IZIVIA                          | 13     |
| 28      | TotalEnergies Charging Services | 13     |
| 21      | LUMI'IN                         | 84     |
| 16      | Power Dot France                | 13     |
| 10      | LUMI'IN                         | 04     |
| 8       | Last Mile Solutions             | 13     |
| 7       | CAR2PLUG                        | 83     |
| 7       | Bump                            | 13     |
| 7       | Power Dot France                | 84     |
```

## Indicateurs d'infrastructure

### Infrastructure - typologie

Objectif :

- analyse de la typologie (comparaison des ratios)

| id          | nom                                                       | Pr  | type  | historisé             |
| ----------- | --------------------------------------------------------- | --- | ----- | --------------------- |
| t1-xx-yy-zz | Nombre de points de recharge par niveau de puissance      | 1   | infra | oui (national/région) |
| t2-xx-yy-zz | Pourcentage de points de recharge par niveau de puissance | 2   | infra | synthèse              |
| t3-xx-yy-zz | Nombre stations par nombre de points de recharge          | 1   | infra | non                   |
| t4-xx-yy-zz | Pourcentage de stations par nombre de points de recharge  | 2   | infra | non                   |
| t5-xx-yy-zz | Nombre de stations par type d'implantation                | 1   | infra | oui (national/région) |
| t6-xx-yy-zz | Pourcentage de stations par type d'implantation           | 2   | infra | synthèse              |
| t7-xx-yy-zz | Densité EPCI (nb EPCI avec / nb EPCI total)               | 3   | infra | oui (national/région) |
| t8-xx-yy-zz | Nombre stations par opérateur                             | 1   | infra | oui (national/région) |
| t9-xx-yy-zz | Pourcentage de stations par opérateur                     | 2   | infra | synthèse              |

:::{note}

L'identification des opérateurs (nom) est actuellment facultative (à rendre obligatoire).
La classification des niveaux de puissances nominale est à valider (en liaison avec le type d'alimentation AC/DC). La classification retenue actuellement est la suivante : 0-15 / 15-26 / 26-65 / 65-175 / 175-360 / > 360 (valeurs de seuil choisies à partir de l'existant Qualicharge).
:::

### Infrastructure - quantitatif

Objectif:

- analyse de la répartition géographique (les ratios permettent les comparaisons)

| id          | nom                                              | Pr  | type  | historisé              |
| ----------- | ------------------------------------------------ | --- | ----- | ---------------------- |
| i1-xx-yy-zz | Nombre de points de recharge ouverts au public   | 1   | infra | oui (département/EPCI) |
| i2-xx-yy-zz | Ratio pour 100 000 habitants                     | 1   | infra | synthèse               |
| i3-xx-yy-zz | Ratio pour 100 km2                               | 2   | infra | synthèse               |
| i4-xx-yy-zz | Nombre de stations de recharge ouverts au public | 1   | infra | oui (département/EPCI) |
| i5-xx-yy-zz | Ratio pour 100 000 habitants                     | 1   | infra | synthèse               |
| i6-xx-yy-zz | Ratio pour 100 km2                               | 2   | infra | synthèse               |
| i7-xx-yy-zz | Puissance installée                              | 1   | infra | oui (département/EPCI) |
| i8-xx-yy-zz | Ratio pour 100 000 habitants                     | 1   | infra | synthèse               |
| i9-xx-yy-zz | Ratio pour 100 km2                               | 2   | infra | synthèse               |

zz : critère de répartition par périmètre (ex. 02 : répartition par département)

## Indicateurs d'infrastructure du réseau autoroutes

Objectif:

- analyse du niveau d'équipement des stations
- analyse de la couverture des trajets nationaux
- analyse de la répartition par station

### Indicateurs globaux

| id  | nom                                                                | Pr  | type  | historisé |
| --- | ------------------------------------------------------------------ | --- | ----- | --------- |
| a1  | Nombre de points de recharge (i1-xx)                               | 1   | infra | oui       |
| a2  | Nombre de stations de recharge (i4-xx)                             | 2   | infra | oui       |
| a3  | Puissance installée (i7-xx)                                        | 2   | infra | oui       |
| a4  | Nombre de points de recharge par niveau de puissance (t1-xx)       | 1   | infra | non       |
| a5  | Densité des stations équipées (nb stations équipées / nb stations) | 3   | infra | oui       |
| a6  | Distance moyenne inter-station de recharge                         | 3   | infra | oui       |

ex. Suivi du déploiement des IRVE dans les stations (nécessite de disposer du nombre de stations).
ex. Suivi temporel de la distance interstation (utilisation du graphe pour calculer les distances de recharge associée à chaque station).

:::{note}

L'appartenance d'une station au réseau autoroute est à définir (attribut spécifique et / ou proximité géographique avec les voies de circulation).
Le graphe autoroutier doit permettre d'associer plusieurs stations à un noeud (ou à un tronçon).
:::

### Indicateurs par station

| id  | nom                                    | Pr  | type  | historisé |
| --- | -------------------------------------- | --- | ----- | --------- |
| a7  | Puissance installée par station        | 2   | infra | non       |
| a8  | Nombre de points de charge par station | 2   | infra | non       |
| a9  | Distance de recharge par station       | 2   | infra | non       |

ex. Analyse de la distance interstation (zones blanches).

## Indicateurs d'usage

### Usage - quantitatif

- analyse de l'évolution temporelle de l'utilisation

| id          | nom                                  | Pr  | type  | historisé             |
| ----------- | ------------------------------------ | --- | ----- | --------------------- |
| u1-xx-yy-zz | Nombre de point de charge actif      | 2   | usage | oui (national/région) |
| u2-xx-yy-zz | Pourcentage de point de charge actif | 2   | usage | synthèse              |
| u3-xx-yy-zz | Nombre de sessions                   | 2   | usage | oui (national/région) |
| u4-xx-yy-zz | Energie distribuée                   | 2   | usage | oui (national/région) |

u1 est calculé sur une journée
u2 est calculé à partir de u1 et i1
u3 et u4 sont calculés par heure

exemple d'utilisation : Analyse du profil horaire de l'énergie fournie en fonction des périodes et de la localisation.

### Usage - qualité de service

- analyse de la disponibilité et de l'utilisation des points de recharge

| id           | nom                                                  | Pr  | type  | historisé             |
| ------------ | ---------------------------------------------------- | --- | ----- | --------------------- |
| q1-xx-yy-zz  | Durée de bon fonctionnement                          | 2   | usage | oui (national/région) |
| q2-xx-yy-zz  | Durée d'utilisation                                  | 2   | usage | oui (national/région) |
| q3-xx-yy-zz  | Durée d'ouverture                                    | 2   | usage | oui (national/région) |
| q4-xx-yy-zz  | Nombre de sessions réussies                          | 3   | usage | oui (national/région) |
| q5-xx-yy-zz  | Saturation                                           | 2   | usage | non                   |
| q6-xx-yy-zz  | Taux de disponibilité d'un point de charge actif     | 2   | usage | synthèse              |
| q7-xx-yy-zz  | Taux de disponibilité par catégorie de puissance     | 3   | usage | synthèse              |
| q8-xx-yy-zz  | Taux d'utilisation d'un point de charge actif        | 2   | usage | synthèse              |
| q9-xx-yy-zz  | Taux de sessions réussies d'un point de charge actif | 2   | usage | synthèse              |
| q10-xx-yy-zz | Taux de saturation d'une station                     | 3   | usage | non                   |

q1, q2, q3, q4 et q5 sont les valeurs cumulées sur une journée
q6, q7 sont calculé à partir de q1 et q3
q8 est calculé à partir de q2 et q3
q9 est calculé à partir de q4 et u3
q10 est calculé à partir de q5

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

## Indicateurs temporels

Les indicateurs temporels identifiés sont les suivants :

| id            | nom                                              | Pr  | base   | fonction       |
| ------------- | ------------------------------------------------ | --- | ------ | -------------- |
| d1-w-xx-yy-zz | Taux d'évolution du nombre de stations           | 1   | i4     | taux évolution |
| d2-w-xx-yy-zz | Evolution du nombre de points de recharge        | 1   | i1     | historique     |
| d3-w-xx-yy-zz | Nombre de sessions par point de recharge         | 2   | u3     | historique     |
| d4-w-xx-yy-zz | Taux de disponibilité par catégorie de puissance | 2   | q1, q3 | historique     |
| d5-w-xx-yy-zz | Taux de points de recharge avec indispo > 7 j    | 3   | q1, q3 | historique     |

Nota : Seule la périodicité est intégrée à la codification (voir chapitre 'codification'), l'intervalle doit donc être ajouté à l'indicateur.

```{admonition} Exemples
- Evolution du nombre mensuel de points de recharge pour 2024 par département : (d2-m---4, entre 01/01/2023 et le 01/01/2024)
```

## Indicateurs d'état

Les indicateurs d'état identifiés sont les suivants :

| id          | nom                                      | Pr  |
| ----------- | ---------------------------------------- | --- |
| e1-xx-yy-zz | Liste des stations du réseau autoroutier | 2   |
| e2-xx-yy-zz | Liste des stations actives               | 2   |

Nota : La périodicité d'historisation n'est pas intégrée à la codification (voir chapitre 'codification'), la date doit donc être ajouté à l'indicateur.

```{admonition} Exemples
- Liste des stations du réseau autoroutier (d2) au 31/12/2024 
```

## Indicateurs étendus

Ils concernent le couplage des données avec des jeux de données complémentaires (à définir dans un second temps):

- couplage consommation / trafic
- couplage nombre de véhicules électriques vendus/immatriculés
- couplage consommation / relevés ENEDIS des points de livraison
