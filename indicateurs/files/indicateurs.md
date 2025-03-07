# Indicateurs de référence

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
- Indicateurs AFIR : Ce sont les indicateurs associés à la règlementation européenne AFIR
- indicateurs étendus : Ils concernent les indicateurs obtenus avec des jeux de données en lien (ex. relevés ENEDIS)

:::{note}

Les indicateurs d'exploitation (liés aux aménageurs et enseignes) ainsi que les indicateurs liés à des attributs spécifiques (ex. accès deux roues, période d'ouverture, accès handicapés...) sont à ajouter.

:::

### Codification des indicateurs

Les indicateurs sont codifiés par une chaine de caractères : *[type]-[périmètre]-[valeur de périmètre]-[level]*
ou bien pour les indicateurs temporels : *[type]-[période]-[périmètre]-[valeur de périmètre]-[level]*
avec:

- type : identifiant du type d'indicateur (ex. 'i1' : nombre de points de recharge)
- période : périodicité des données utilisées (agrégation : somme, moyenne, maximum, dernière)
  - y : données annuelles
  - m : données mensuelles
  - w : données hebdomadaires
  - d : données quotidiennes
  - h : données horaires
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
- **u5-h-1-93** : Nombre de sessions (u5) cumulées sur une heure (h) pour la région (1) PACA (93)
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
Ce champ est au format JSON et concerne les informations liées à l'historisation ainsi que les données des indicateurs d'état.

Si aucune catégorisation et aucun level ne sont définis, le résultat se réduit à une valeur.

```{admonition} Exemple
'i1' : le résultat est le nombre de points de recharge (valeur)
```

Si uniquement une catégorisation est définie, le résultat est une liste de valeurs associées à chaque catégorie.

```{admonition} Exemple
't1' : le résultat est le nombre de points de recharge (valeur : nb_pdc) par niveau de puissance (catégorie : p_range)

| nb_pdc | p_range      |
| ------ | ------------ |
| 10892  | [7.4, 22.0) |
| 4807   | [150, 350.0) |
| 3282   | [50, 150.0)  |
| 2359   | [22, 50.0)   |
| 2157   | [0, 7.4)    |
| 25     | [350, None)  |
```

Si uniquement un level est défini, le résultat est une liste de valeurs associées à chaque target.

```{admonition} Exemple
i1-1-93-2 : Nombre de points de recharge (i1) pour la région (1) PACA (93) par département (2)
Le résultat est le nombre de points de recharge (valeur : nb_pdc) par département (target : code du département).

| nb_pdc | code   |
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
La 'target' est ici le département (représenté par son code) et la 'catégorie' est l'opérateur (nom_operateur).

| nb_stat | nom_operateur                   | code   |
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

| id        | nom                                                       | Pr  | type  | historisé             |
| --------- | --------------------------------------------------------- | --- | ----- | --------------------- |
| t1-x-yy-z | Nombre de points de recharge par niveau de puissance      | 1   | infra | oui (national/région) |
| t2-x-yy-z | Pourcentage de points de recharge par niveau de puissance | 2   | infra | synthèse              |
| t3-x-yy-z | Nombre stations par nombre de points de recharge          | 1   | infra | non                   |
| t4-x-yy-z | Pourcentage de stations par nombre de points de recharge  | 2   | infra | non                   |
| t5-x-yy-z | Nombre de stations par type d'implantation                | 1   | infra | oui (national/région) |
| t6-x-yy-z | Pourcentage de stations par type d'implantation           | 2   | infra | synthèse              |
| t7-x-yy-z | Densité EPCI (nb EPCI avec / nb EPCI total)               | 3   | infra | oui (national/région) |
| t8-x-yy-z | Nombre stations par opérateur                             | 1   | infra | oui (national/région) |
| t9-x-yy-z | Pourcentage de stations par opérateur                     | 2   | infra | synthèse              |

:::{note}

L'identification des opérateurs (nom) est actuellment facultative (à rendre obligatoire).
La classification des niveaux de puissances nominale est à valider (en liaison avec le type d'alimentation AC/DC). La classification retenue actuellement est la suivante : 0-7.4 / 7.4-22 / 22-50 / 50-150 / 150-350 / > 350 (valeurs de seuil choisies à partir du baromètre Avere).
:::

### Infrastructure - quantitatif

Objectif:

- analyse de la répartition géographique (les ratios permettent les comparaisons)

| id        | nom                                              | Pr  | type  | historisé              |
| --------- | ------------------------------------------------ | --- | ----- | ---------------------- |
| i1-x-yy-z | Nombre de points de recharge ouverts au public   | 1   | infra | oui (département/EPCI) |
| i2-x-yy-z | Ratio pour 100 000 habitants                     | 1   | infra | synthèse               |
| i3-x-yy-z | Ratio pour 100 km2                               | 2   | infra | synthèse               |
| i4-x-yy-z | Nombre de stations de recharge ouverts au public | 1   | infra | oui (département/EPCI) |
| i5-x-yy-z | Ratio pour 100 000 habitants                     | 1   | infra | synthèse               |
| i6-x-yy-z | Ratio pour 100 km2                               | 2   | infra | synthèse               |
| i7-x-yy-z | Puissance installée                              | 1   | infra | oui (département/EPCI) |
| i8-x-yy-z | Ratio pour 100 000 habitants                     | 1   | infra | synthèse               |
| i9-x-yy-z | Ratio pour 100 km2                               | 2   | infra | synthèse               |

## Indicateurs d'infrastructure du réseau autoroutes

Objectif:

- analyse du niveau d'équipement des stations
- analyse de la couverture des trajets nationaux
- analyse de la répartition par station

### Indicateurs globaux

| id  | nom                                                          | Pr  | type  | historisé |
| --- | ------------------------------------------------------------ | --- | ----- | --------- |
| a1  | Nombre de points de recharge (i1-xx)                         | 1   | infra | oui       |
| a2  | Nombre de stations de recharge (i4-xx)                       | 2   | infra | oui       |
| a3  | Puissance installée (i7-xx)                                  | 2   | infra | oui       |
| a4  | Nombre de points de recharge par niveau de puissance (t1-xx) | 1   | infra | non       |
| a5  | Densité des aires de service équipées                        | 3   | infra | oui       |
| a6  | Distance moyenne inter-station de recharge                   | 3   | infra | non       |

ex. Suivi du déploiement des IRVE dans les stations (nécessite de disposer du nombre de stations).
ex. Suivi temporel de la distance interstation (utilisation du graphe pour calculer les distances de recharge associée à chaque station).

:::{note}

L'appartenance d'une station au réseau autoroute est à définir (attribut spécifique et / ou proximité géographique avec les voies de circulation).
Le graphe autoroutier doit permettre d'associer plusieurs stations à un noeud (ou à un tronçon).
:::

### Indicateurs par aire

| id  | nom                                 | Pr  | type  | historisé |
| --- | ----------------------------------- | --- | ----- | --------- |
| a7  | Puissance installée par aire        | 2   | infra | non       |
| a8  | Nombre de points de charge par aire | 2   | infra | non       |
| a9  | Distance de recharge par aire       | 2   | infra | non       |

ex. Analyse de la distance interstation (zones blanches).

## Indicateurs d'usage

### Usage - quantitatif

- analyse de l'évolution temporelle de l'utilisation

| id         | nom                                                                     | Pr  | type  | historisé             |
| ---------- | ----------------------------------------------------------------------- | --- | ----- | --------------------- |
| u1-x-yy-z  | Durée de dysfonctionnement des pdc par catégorie de puissance (état HS) | 2   | usage | oui (national/région) |
| u2-x-yy-z  | Durée d'utilisation des pdc(état occupé)                                | 2   | usage | non                   |
| u3-x-yy-z  | Durée de non utilisation des pdc (état libre)                           | 2   | usage | non                   |
| u4-x-yy-z  | Durée d'ouverture des pdc par catégorie de puissance                    | 2   | usage | oui (national/région) |
| u5-x-yy-z  | Répartition horaire des sessions (nombre)                               | 3   | usage | oui (national/région) |
| u6-x-yy-z  | Durée des sessions par catégorie de puissance                           | 2   | usage | oui (national/région) |
| u7-x-yy-z  | Durée d'activité des stations (état saturé, active ou inactive)         | 2   | usage | oui (national/région) |
| u8-x-yy-z  | Durée de saturation des stations                                        | 2   | usage | oui (national/région) |
| u9-x-yy-z  | Energie distribuée par catégorie de puissance                           | 2   | usage | oui (national/région) |
| u10-x-yy-z | Nombre de sessions                                                      | 2   | usage | oui (national/région) |
| u11-x-yy-z | Nombre de sessions réussies                                             | 2   | usage | oui (national/région) |
| u12-x-yy-z | Nombre de pdc en activité par catégorie de puissance                    | 2   | usage | oui (national/région) |
| u13-x-yy-z | Puissance des points de recharge en activité                            | 2   | usage | oui (national/région) |

u1, u2, u3, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13 sont les valeurs cumulées (ex. moyenne, somme)

u1 et u4 sont calculés par catégorie de puissance

u4 est la durée de 24h multipliée par le nombre de points de recharge dans l'état "en activité"

u5 est le nombre de sessions démarrées dans la période concernée

u6 est la part de la durée dans la période des sessions démarrées ou terminées dans la période

u9 est la part de l'énergie (au prorata de la durée passée dans la période) des sessions

u12 et u13 sont calculés à partir de e2

exemple d'utilisation : Analyse du profil horaire de l'énergie fournie en fonction des périodes et de la localisation.

### Usage - qualité de service

- analyse de l'utilisation de la recharge (pour une période donnée et sur un périmètre géographique) :

| id        | nom                                              | Pr  | type  | historisé |
| --------- | ------------------------------------------------ | --- | ----- | --------- |
| q1-x-yy-z | Taux de disponibilité par catégorie de puissance | 3   | usage | synthèse  |
| q2-x-yy-z | Taux d'utilisation par catégorie de puissance    | 2   | usage | synthèse  |
| q3-x-yy-z | Taux de saturation des stations                  | 2   | usage | synthèse  |
| q4-x-yy-z | Facteur de charge par catégorie de puissance     | 2   | usage | synthèse  |
| q5-x-yy-z | Taux de sessions réussies                        | 2   | usage | synthèse  |

q1 est calculé à partir de u1 et u4

q2 est calculé à partir de u6, u1 et u4

q3 est calculé à partir de u8 et u7

q4 est calculé à partir de u9 et u12

q5 est calculé à partir de u11 et u10

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

### Usage - calcul TIRUERT

- énergie distribuée (pour une période donnée et sur un périmètre géographique) :

| id        | nom                              | Pr  | type  | historisé             |
| --------- | -------------------------------- | --- | ----- | --------------------- |
| c1-x-yy-z | Nombre de sessions par opérateur | 2   | usage | oui (national/région) |
| c2-x-yy-z | Energie distribuée par opérateur | 2   | usage | oui (national/région) |

## Indicateurs temporels

Les indicateurs temporels identifiés sont les suivants :

| id          | nom                                              | Pr  | base    | fonction       |
| ----------- | ------------------------------------------------ | --- | ------- | -------------- |
| d1-w-x-yy-z | Taux d'évolution du nombre de stations           | 1   | i4      | taux évolution |
| d2-w-x-yy-z | Evolution du nombre de points de recharge        | 1   | i1      | historique     |
| d3-w-x-yy-z | Nombre de sessions par point de recharge         | 2   | u5, u11 | historique     |
| d4-w-x-yy-z | Taux de disponibilité par catégorie de puissance | 2   | q1      | historique     |
| d5-x-yy-z   | Taux d'utilisation                               | 2   | q2      | historique     |
| d6-x-yy-z   | Taux de saturation des stations                  | 2   | q3      | historique     |
| d7-x-yy-z   | Facteur de charge                                | 2   | q4      | historique     |
| d8-w-x-yy-z | Taux de points de recharge avec indispo > 7 j    | 3   | q1, q3  | historique     |

:::{note}

- Seule la périodicité est intégrée à la codification (voir chapitre 'codification'), l'intervalle doit donc être ajouté à l'indicateur.

:::

```{admonition} Exemples
- Evolution du nombre mensuel de points de recharge pour 2024 par département : (d2-m---4, entre 01/01/2023 et le 01/01/2024)
```

## Indicateurs d'état

Les indicateurs d'état identifiés sont les suivants :

| id        | nom                                        | Pr  |
| --------- | ------------------------------------------ | --- |
| e1-x-yy-z | Liste des stations du réseau autoroutier   | 2   |
| e2-x-yy-z | Liste des stations du réseau RTE-T central | 2   |
| e3-x-yy-z | Liste des stations du réseau RTE-T global  | 2   |
| e4-x-yy-z | Liste des points de recharge en activité   | 2   |

:::{note}

- La périodicité d'historisation n'est pas intégrée à la codification (voir chapitre 'codification'), la date doit donc être ajouté à l'indicateur.

:::

```{admonition} Exemples
- Liste des stations du réseau autoroutier (e1) au 31/12/2024 
```

## Indicateurs AFIR

Les indicateurs AFIR identifiés sont les suivants :

| id      | nom                                | Pr  |
| ------- | ---------------------------------- | --- |
| p1-x-yy | Liste des stations des parcs p300  | 2   |
| p2-x-yy | Liste des stations des parcs p400  | 2   |
| p3-x-yy | Liste des stations des parcs p600  | 2   |
| p4-x-yy | Liste des stations des parcs p1400 | 2   |
| p5-x-yy | Liste des stations des parcs p1500 | 2   |
| p6-x-yy | Liste des stations des parcs p1600 | 2   |

| id  | nom                               | Pr  |
| --- | --------------------------------- | --- |
| r1  | Ratio AFIR d60 / p400 / central   | 2   |
| r2  | Ratio AFIR d60 / p600 / central   | 2   |
| r3  | Ratio AFIR d60 / p300 / global    | 2   |
| r4  | Ratio AFIR d60 / p600 / global    | 2   |
| r5  | Ratio AFIR d120 / p1400 / global  | 2   |
| r6  | Ratio AFIR d120 / p2800 / central | 2   |
| r7  | Ratio AFIR d60 / p3600 / central  | 2   |
| r8  | Ratio AFIR d100 / p1500 / global  | 2   |

:::{note}

- La notion de `level` ne s'applique pas pour les indicateurs AFIR
- Les indicateurs 'px' peuvent être regroupés par périmètre contrairement aux indicateurs 'rx'.

:::

```{admonition} Exemples
- Liste des stations du réseau RTE-T associées à un parc de plus de 300 kW dont un pdc a plus de 150 kW (p1) au 31/12/2024
- Ratio des tronçons du réseau RTE-T central associés à des parcs d'une puissance de 400 kW dont un des pdc a plus de 150 kW et distant de moins de 60 km (r1)
```

## Indicateurs étendus

Ils concernent le couplage des données avec des jeux de données complémentaires (à définir dans un second temps):

- couplage consommation / trafic
- couplage nombre de véhicules électriques vendus/immatriculés
- couplage consommation / relevés ENEDIS des points de livraison
