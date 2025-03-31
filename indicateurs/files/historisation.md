# Historisation des indicateurs

## objectif

L'historisation des indicateurs a pour objectif de disposer des données nécessaires à la mise à disposition des [indicateurs définis](./indicateurs.md) à une date donnée.

Il adresse trois besoins :

- calculer les indicateurs temporels,
- restituer les indicateurs d'état,
- fournir les indicateurs pour une ancienne date

### Indicateurs temporels

#### Caractéristiques

Il s'agit des indicateurs associés à un intervalle temporel et à une périodicité. Ils peuvent prendre plusieurs formes :

- un historique de valeurs sur l'intervalle (ex. un histogramme),
- une représentation statistique (ex. une moyenne, une interpolation linéaire)
- une analyse spécifique

On peut citer par exemple les indicateurs AVERE suivants :
  
- Taux d'évolution du nombre de stations sur 12 mois
- Evolution du nombre de points de recharge par année
- Évolution du nombre de points de recharge par mois sur deux ans
- Nombre de sessions moyen mensuel par point de recharge
- Taux de disponibilité du mois par catégorie de puissance

Le calcul des indicateurs temporels doit pouvoir être réalisé en optimisant les temps de calcul et le volume de données stockées (il serait, par exemple, couteux de calculer une valeur annuelle à partir de données horaires).

#### Principes d'historisation

:::{mermaid}
flowchart LR
    subgraph état courant
        direction RL
        dyn[("`base
        dynamique`")]
        stat[("`base
        statique`")]
    end

    subgraph historisation
        direction RL
        heure("`histo`")
        jour("`histo`")
        mois("`histo`")
        an("`histo`")

        heure -->|quotidien| jour
        jour -->|mensuel| mois
        mois -->|annuel| an
        heure -->|purge| heure
        jour -->|purge| jour
        mois -->|purge| mois
        an -->|purge| an
    end  
    dyn -->|indicateur horaire| heure   
    stat -->|indicateur quotidien| jour   
    historisation -->|indicateur temporel| restitution
:::
NOTA : Le stockage peut être identique pour toutes les périodicités.

Le schéma ci-dessus illustre les principes suivants :

- historisation des données à différentes échelles de temps (périodicité).

:::{admonition} Exemple
Pour présenter l'évolution du nombre de points de recharge par mois sur deux ans, il est nécessaire d'avoir stocké au préalable mensuellement le nombre de points de recharge.
:::

- historisation de données "scalables" (qu'on peut calculer pour une périodicité à partir de données existantes à une périodicité plus faible)

:::{admonition} Exemples

- calcul des valeurs annuelles à partir des valeurs mensuelles (et valeurs mensuelles à partir des valeurs quotidiennes).
- le taux de disponibilité qui est le ratio du temps de bon fonctionnement sur le temps d'ouverture n'est pas scalable (le taux mensuel n'est pas égal à la moyenne des taux journaliers). Par contre, le temps de bon fonctionnement et le temps d'ouverture sont scalables et on peut donc calculer le taux de disponibilité sur une période à partir du temps de bon fonctionnement sur la période et du temps d'ouverture sur la période.

:::

- purge des données anciennes.

:::{admonition} Exemple
Si le nombre de points de recharges fait l'objet de valeurs quotidiennes et de valeurs mensuelles, il n'est pas nécessaire de conserver les valeurs quotidiennes datant de plusieurs mois.
:::

#### périodicité

Les valeurs associées à une périodicité permettent de restituer deux informations principales :

- une information cumulées dont le passage à l'échelle se traduit par une somme.

```{admonition} Exemple
Le nombre annuel de sessions peut être calculée comme la somme des nombres mensuels de session eux-mêmes calculés comme la somme des nombres quotidiens de sessions,
```

- une information ajustables dont le passage à l'échelle se traduit par une moyenne.

```{admonition} Exemple
La puissance moyenne installée de l'année peut être calculée à partir des puissances moyennes installées du mois elles-mêmes calculées à partir des puissances moyennes installées quotidiennes.
La moyenne annuelle du nombre quotidien de session peut être calculé à partir des moyennes mensuelles du nombre quotidien de sessions.
```

Chaque périodicité peut être associée à une (ou plusieurs) table purgée avec une fréquence spécifique. Par exemple, les données horaires pourraient être purgées chaque semaine ou chaque mois.

Pour un indicateur, on historise à chaque niveau la valeur principale qui correspond à une valeur moyenne ainsi qu'un ensemble de valeurs additionnelles. Ces valeurs sont calculées à partir des valeurs du niveau précédent :

- valeur principale :
  - moyenne (cumul des valeurs utilisées / nombre de valeurs utilisées)
- valeurs additionnelles :
  - quantité (nombre de valeurs utilisées) -> obligatoire,
  - variance (moyenne du cumul des carrés des valeurs utilisées - carré de la moyenne des valeurs utilisées) -> optionnel
  - valeur maximale -> optionnel
  - valeur minimale -> optionnel
  - dernière valeur -> optionnel

Nota : Le cumul des valeurs utilisées se déduit de la quantité et de la moyenne ( cumul = quantité x moyenne)

```{admonition} Exemple
On a historisé les valeurs mensuelles suivantes pour un trimestre de l'indicateur du nombre de stations :

| quantite | moyenne |
| -------- | ------- |
| 30       | 50      |
| 28       | 55      |
| 31       | 60      |

La valeur historisée du nombre de stations pour le trimestre est : 

- moyenne : 55,06

La valeur additionnelle pour le trimestre est :

- quantite : 89

Les autres valeurs additionnelles ne sont calculables que si elles sont documentées au niveau précédent.
```

#### Mise en oeuvre

Le résultat de l'indicateur temporel peut prendre plusieurs formes :

- historique de valeurs
- variation (relative) : écart (relatif) entre la première et la dernière valeur
- fonction statistique appliquée à l'ensemble des valeurs (ex. écart-type)

Un indicateur temporel est donc défini par :

- l'indicateur de base à utiliser,
- l'intervalle,
- la périodicité,
- la valeur historisée,
- la fonction appliquée.

```{admonition} Exemple
L'indicateur du taux d'évolution du nombre de stations sur 12 mois au 01/01/2024 par département est défini par :

- l'indicateur de base : 'i4- - -4',
- l'intervalle : entre le 01/01/2023 et le 01/01/2024,
- la périodicité : mensuelle,
- la fonction : taux d'évolution (valeur mensuelle fin - valeur mensuelle début) / valeur mensuelle début.

Le résultat est obtenu en appliquant les traitements suivants:

- calcul quotidien de l'indicateur 'i4- - -4' sur les données statiques courantes,
- chaque jour, historisation du résultat du calcul,
- chaque mois, historisation du jeu de valeurs mensuel obtenu à partir des données quotidiennes,
- calcul du taux d'évolution sur les données de l'historisation mensuelle.
```

#### Indicateurs retenus

Les indicateurs temporels identifiés (voir présentation des indicateurs) sont les suivants :

| id          | nom                                              | Pr  | base    | fonction       |
| ----------- | ------------------------------------------------ | --- | ------- | -------------- |
| d1-w-x-yy-z | Taux d'évolution du nombre de stations           | 1   | i4      | taux évolution |
| d2-w-x-yy-z | Evolution du nombre de points de recharge        | 1   | i1      | historique     |
| d3-w-x-yy-z | Nombre de sessions par point de recharge         | 2   | u5, u11 | historique     |
| d4-w-x-yy-z | Taux de disponibilité par catégorie de puissance | 2   | q1      | historique     |
| d5-x-yy-z   | Taux d'utilisation par catégorie de puissance    | 2   | q2      | historique     |
| d6-x-yy-z   | Taux de saturation des stations                  | 2   | q3      | historique     |
| d7-x-yy-z   | Facteur de charge par catégorie de puissance     | 2   | q4      | historique     |
| d8-w-x-yy-z | Taux de points de recharge avec indispo > 7 j    | 3   | q1, q3  | historique     |

Nota : Seule la périodicité est intégrée à la codification (voir chapitre '[codification](./indicateurs.md)'), l'intervalle doit donc être ajouté à l'indicateur pour fournir un résultat.

```{admonition} Exemples
- Evolution du nombre mensuel de points de recharge pour 2024 par département : (d2-m- - -4, entre 01/01/2023 et le 01/01/2024)
```

### Indicateurs d'état

Il s'agit des indicateurs associés à un état de la base de données à un instant donné.

Il n'est imposé aucune structure spécifique pour les données incluses dans ces indicateurs.

On peut citer par exemple les besoins suivants :

- Suivre la liste des stations du réseau autoroutier
- (autres exemples à indiquer)

Le calcul des indicateurs temporels doit pouvoir être réalisé en optimisant les temps de calcul et le volume de données stockées (il serait, par exemple, couteux de calculer une valeur annuelle à partir de données horaires).

#### Historisation des indicateurs d'état

L'historisation ne fait l'objet d'aucun traitement statistique ni de retraitement temporel.

L'historisation peut s'effectuer avec une périodicité quelconque.

Pour un indicateur, on historise une valeur principale ainsi qu'un ensemble de valeurs additionnelles.

- valeur principale :
  - valeur numérique spécifique de chaque indicateur
- valeurs additionnelles :
  - ensemble de valeurs spécifiques de chaque indicateur

#### Application

Le résultat de l'indicateur d'état est identique à la valeur historisée.

Un indicateur d'état est donc défini par :

- l'indicateur de base à utiliser,
- la date de l'état pris en compte,
- la périodicité,
- la valeur historisée,

```{admonition} Exemple
L'indicateur de la liste des stations du réseau autoroutier au 01/01/2024 est défini par :

- l'indicateur de base : 'e1- - -4',
- l'intervalle : entre le 01/01/2023 et le 01/01/2024,
- la périodicité : mensuelle,
- la fonction : taux d'évolution (valeur mensuelle fin - valeur mensuelle début) / valeur mensuelle début.

Le résultat est obtenu en appliquant les traitements suivants:

- calcul quotidien de l'indicateur 'i4- - -4' sur les données statiques courantes,
- chaque jour, historisation du résultat du calcul,
- chaque mois, historisation du jeu de valeurs mensuel obtenu à partir des données quotidiennes,
- calcul du taux d'évolution sur les données de l'historisation mensuelle.
```

#### Indicateurs d'état retenus

Les indicateurs d'état identifiés (voir [présentation des indicateurs](./indicateurs.md)) sont les suivants :

| id          | nom                                      | Pr  |
| ----------- | ---------------------------------------- | --- |
| e1-xx-yy-zz | Liste des stations du réseau autoroutier | 2   |
| e2-xx-yy-zz | Liste des stations en activité           | 2   |

### Indicateurs à date

L'historisation maintient une archive des indicateurs sous sa forme exacte pour un passé récent et sous une forme agrégée (valeurs hedomadaire, mensuelle ou annuelle) sur des périodes plus longues.

L'historisation s'effectue pour une granularité définie, il est alors possible d'accéder aux indicateurs avec une granularité plus faible.

```{admonition} Exemple
Si l'indicateur 'i7' est historisé pour les communes , il est possible de restituer cet indicateur pour une date ou une période antérieure et pour tous les niveaux de regroupement (communes, département, région, EPCI) ainsi que les indicateurs dérivés 'i8' et 'i9'.
```

## Solution d'historisation

### Besoin

L'historisation s'effectue pour les indicateurs suivants (voir chapitre listant les indicateurs):

- infrastructure - typologie : t1, t1- - -1, t5, t5- - -1, t7, t8, t8- - -1
- infrastructure - quantitatif : i1- - -3, i1- - -4, i4- - -3, i4- - -4, i7- - -3, i7- - -4
- infrastructure - autoroute : a1, a2, a3
- usage - quantitatif: u1, u4, u5, u6, u7, u8, u9, u10, u11, u12, u13
- état : e1 (mensuel)

### Volumétrie

hypothèses :

- région : 20 (13 métropole + 5 ultramarins + 1 métropole + 1 national)
- niveaux de puissance : 6
- type d'implantation : 5
- nombre d'EPCI : 1255
- nombre de départements : 109
- nombre d'heures : 24
- nombre d'opérateurs : 40

Nombres de lignes :

- t1 : 120 = 20 x 6
- t5 : 100 = 20 x 5
- t7 : 1255
- t8 : 40
- i1 : 1364 = 1255 + 109
- i4 : 1364 = 1255 + 109
- i7 : 1364 = 1255 + 109
- a1, a2, a3 : 1
- u5 : 480 = 24 x 20
- u1, u4, u6, u9, u12 : 120 = 6 x 20
- u7, u8, u10, u11, u13 : 20
- e1, e2, e3, e4 : 1

Total : 6 794 lignes par historisation

Nombre d'historisations :

- Quotidienne : 62 (deux mois)
- Mensuelle : 24 (deux ans)
- Annuelle : 10 (10 ans)

Total : 652 224 lignes (96 x 6 794)

:::{note}

- L'historisation concerne le périmètre complet de chaque indicateur.
- Le volume de données peut être réduit en n'historisant que la granularité la plus faible (ex. i4- - -3 n'est pas nécessaire si i4- - -4 est présent)

:::

### Structure

Les données historisées sont regroupées sur une seule table:

Si besoin, une historisation hebdomadaire ou trimestrielle pourra être ajoutée.

La structure des historisations est identique pour toutes les périodicités :

- valeur :
  - VALUE(float) : valeur principale (instantanée ou moyenne)
  - EXTRAS(json) - optionnel : valeur additionnelle
- décomposition :
  - CATEGORY(string ou enum) - optionnel : décomposition associée à l'indicateur (ex. niveau de puissance, implantation)
  - TARGET(string) - optionnel : valeur du niveau de découpage 'level' (ex. '13200')
- indicateur (ex. 't1-01-93-04) :
  - CODE(string ou enum) : nom de la requête (ex. 't1')
  - LEVEL(int) : découpage du périmètre choisi pour l'indicateur
- Datation
  - PERIOD(enum) : périodicité de l'historisation (hour, day, week, month, year)
  - TIMESTAMP(datetime) : datation du résultat du calcul de l'indicateur

Le champ EXTRAS est json-object pour les indicateurs temporels composé des champs (key) suivants :

- QUANTITY(int) : nombre de valeurs utilisées
- VARIANCE(float) - optionnel : variance des valeurs utilisées
- MINI(float) - optionnel : valeur minimale des valeurs utilisées
- MAXI(float) - optionnel : valeur maximale des valeurs utilisées
- LAST(float) - optionnel : dernière valeur utilisée

Pour les indicateurs d'état, le champ EXTRAS est spécifique de chaque indicateur.

exemple du nombre mensuel de stations par opérateur :

| value | extras           | category | target | code | level | period | timestamp |
| ----- | ---------------- | -------- | ------ | ---- | ----- | ------ | --------- |
| 50    | {'quantity': 30} | 'oper1'  | ''     | 't8' | ''    | month  | xxxxxxx   |
| 80    | {'quantity': 30} | 'oper2'  | ''     | 't8' | ''    | month  | xxxxxxx   |
| 100   | {'quantity': 30} | 'oper3'  | ''     | 't8' | ''    | month  | xxxxxxx   |

L'opérateur 'oper1' dispose pour le mois 'xxxxxxx' d'une moyenne de 50 stations.

### Prise en compte des données temporelles

Au premier niveau de périodicité on dispose pour chaque décomposition et chaque indicateur d'une valeur. On a alors :

- QUANTITY = 1
- VARIANCE = 0.0
- MINI = MAXI = LAST = value

Le passage d'une périodicité 'n' (ex. mensuelle) à une périodicité 'n+1' (ex. annuelle) est réalisé en regroupant en une seule toutes les lignes de la périodicité 'n' qui ont des champs 'décomposition' et 'indicateurs' identiques et dont le 'timestamp' est dans la période d'historisation choisie avec les règles suivantes :

- les champs 'décomposition' et 'indicateurs' sont reconduits,
- le champ 'timestamp' prend la valeur associée à la période d'historisation,
- le champ 'periode' prend la valeur de la nouvelle périodicité
- les champs valeurs sont calculés à partir des champs valeurs des lignes à regrouper.

Les formules de calcul sont les suivantes:

- $quantity_{n+1} = \sum quantity_n$
- $value_{n+1} = \frac {\sum quantity_n . value_n} {quantity_{n+1}}$
- $variance_{n+1} = \frac {1} {quantity_{n+1}} \sum quantity_n . (variance_n + (value_{n+1} - value_n)^2)$
- $maxi_{n+1} = MAX(maxi_n)$
- $mini_{n+1} = MIN(mini_n)$
- $last_{n+1} = LAST(last_n)$

Formules corrigées :

- $size_{n+1} = \sum size_n$
- $mean_{n+1} = \frac {\sum size_n . mean_n} {size_{n+1}}$
- $var_{n+1} = \frac {1} {size_{n+1}} \sum size_n . (var_n + (mean_{n+1} - mean_n)^2)$
- $var_{n+1} = \frac {1} {size_{n+1}} \sum size_n . var_n$ +
               $mean_{n+1}^2$ -
               $\frac {2 . mean_{n+1}} {size_{n+1}} \sum mean_n$ +
               $\frac {1} {size_{n+1}} \sum size_n . mean_n^2$

Une valeur facultative à un niveau 'n+1' n'est pas présente si elle n'est pas présente au niveau 'n'

### Prise en compte des données d'état

Pour les données d'état, le champ 'valeur' est une donnée spécifique de l'indicateur (ex. pour une liste ce pourrait être le nombre de lignes) et le champ 'valeur additionnelle' également.

### Construction des indicateurs temporels

Les indicateurs temporels sont construits à partir des données historisées exclusivement suivant les règles propres à chaque indicateur.

```{admonition} Exemple
indicateur d1 : 'taux d'évolution du nombre de stations par département' sur 12 mois au 01/01/2024 '

- recherche dans la table mensuelle les lignes correspondant à 't4-00-00-04' et avec un timestamp entre le 01/01/2023 et le 01/01/2024
- calcul du taux d'évolution pour chaque département (1 - valeur moyenne du dernier mois / valeur moyenne du premier mois)
```

### Construction des indicateurs à date

Les requètes utilisées pour le calcul des indicateurs à date consistent à agréger les données VALUE pour une valeur donnée de LEVEL / TARGET tout en conservant les données CATEGORY, CODE, TIMESTAMP et PERIOD.

### Purge des données

Les données d'un niveau 'n' déjà utilisées pour calculer les données d'un niveau 'n+1' peuvent être supprimées (suppression de lignes).

Par exemple, on peut purger les données quotidiennes après deux mois, les données quotidienne constituent alors un "stock glissant" de deux mois.

Pour les données d'état, les règles de purge sont spécifiques.

### Modification de la liste des indicateurs

L'ajout d'un indicateur à historiser (ou sa suppression) est sans impact pour les données temporelles (la propagation se fait automatiquement d'un niveau d'historisation à un autre).

Pour les indicateurs d'état la situation est similaire (la suppression d'un indicateur se fera en suivant les règles de purge choisies).

### Interruption de flux

L'historisation s'applique sur la base d'un flux continu. En cas de discontinuité (ex si des données arrivent après la première historisation), il est nécessaire de modifier les données préalablement historisées.

Les règles associées restent à définir.
