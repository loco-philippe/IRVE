# Historisation des données

## objectif

L'historisation des données a pour objectif de conserver un état des données à une date donnée.

Il adresse deux besoins :

- calculer les indicateurs temporels (voir indicateurs),
- restituer un état partiel des données (ex. une liste de stations)

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

Les principes proposés sont présentés dans le schéma ci-dessous :

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
        heure("`histo
         heure`")
        jour("`histo
         jour`")
        mois("`histo
         mois`")
        an("`histo
         année`")

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

- historisation des données à différentes échelles de temps (périodicité).

```{admonition} Exemple
Pour présenter l'évolution du nombre de points de recharge par mois sur deux ans, il est nécessaire d'avoir stocké au préalable mensuellement le nombre de points de recharge.
```

- historisation de données "scalables" (qu'on peut calculer pour une périodicité à partir de données existantes à une périodicité plus faible)

```{admonition} Exemples
- calcul des valeurs annuelles à partir des valeurs mensuelles (et valeurs mensuelles à partir des valeurs quotidiennes).
- le taux de disponibilité qui est le ratio du temps de bon fonctionnement sur le temps d'ouverture n'est pas scalable (le taux mensuel n'est pas égal à la moyenne des taux journaliers). Par contre, le temps de bon fonctionnement et le temps d'ouverture sont scalables et on peut donc calculer le taux de disponibilité sur une période à partir du temps de bon fonctionnement sur la période et du temps d'ouverture sur la période.
```

- purge des données anciennes.

```{admonition} Exemple
Si le nombre de points de recharges fait l'objet de valeurs quotidiennes et de valeurs mensuelles, il n'est pas nécessaire de conserver les valeurs quotidiennes datant de plusieurs mois.
```

#### périodicité

Les valeurs associées à une périodicité permettent de restituer deux informations principales :

- une information cumulées dont le passage à l'échelle se traduit par une somme.

```{admonition} Exemple
Le nombre annuel de sessions peut être calculée comme la somme des nombres mensuels de session eux-mêmes calculés comme la somme des nombres mensuels de sessions,
```

- une information ajustables dont le passage à l'échelle se traduit par une moyenne.

```{admonition} Exemple
La puissance moyenne installée de l'année peut être calculée à partir des puissances moyennes installées du mois elles-mêmes calculées à partir des puissances moyennes installées quotidiennes.
La moyenne annuelle du nombre quotidien de session peut être calculé à partir des moyennes mensuelles du nombre quotidien de sessions.
```

Chaque périodicité peut être associée à une (ou plusieurs) table purgée avec une fréquence spécifique. Par exemple, un stockage horaire pourrait être purgé chaque semaine ou chaque mois.

Pour un indicateur, on historise à chaque niveau une valeur principale qui correspond à une valeur moyenne ainsi qu'un ensemble de valeurs additionnelles.  Ces valeurs sont calculées à partir des valeurs du niveau précédent :

- valeur principale :
  - moyenne (cumul des valeurs utilisées / nombre de valeurs utilisées)
- valeurs additionnelles :
  - quantité (nombre de valeurs utilisées) -> obligatoire,
  - variance (moyenne du cumul des carrés des valeurs utilisées - carré de la moyenne des valeurs utilisées) -> optionnel
  - valeur maximale -> optionnel
  - valeur minimale -> optionnel
  - dernière valeur -> optionnel

Nota : Le cumul des valeurs utilisées se déduit de la quantité et de la moyenne ( cumul = quantité x moyenne)

Le passage d'une périodicité 'n' à une périodicité 'n+1' est réalisé de façon automatique avec :

- $quantite_{n+1} = \sum quantite_n$
- $moyenne_{n+1} = \frac {\sum quantite_n . moyenne_n} {\sum quantite_n}$
- $variance_{n+1} = \frac {1} {quantite_{n+1}} \sum quantite_n . (variance_n + (moyenne_{n+1} - moyenne_n)^2)$
- $maxi_{n+1} = MAX(maxi_n)
- $mini_{n+1} = MIN(mini_n)
- $dernier_{n+1} = LAST(dernier_n)

Au premier niveau (une seule valeur) , quantité = 1, variance = 0 et moyenne = mini = maxi = dernier = valeur de l'indicateur

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

- l'indicateur de base : 'i4---04',
- l'intervalle : entre le 01/01/2023 et le 01/01/2024,
- la périodicité : mensuelle,
- la fonction : taux d'évolution (valeur mensuelle fin - valeur mensuelle début) / valeur mensuelle début.

Le résultat est obtenu en appliquant les traitements suivants:

- calcul quotidien de l'indicateur 'i4--04' sur les données statiques courantes,
- chaque jour, historisation du résultat du calcul,
- chaque mois, historisation du jeu de valeurs mensuel obtenu à partir des données quotidiennes,
- calcul du taux d'évolution sur les données de l'historisation mensuelle.
```

#### Indicateurs retenus

Les indicateurs temporels identifiés (voir présentation des indicateurs) sont les suivants :

| id  | nom                                              | Pr  | base   | fonction       |
| --- | ------------------------------------------------ | --- | ------ | -------------- |
| d1  | Taux d'évolution du nombre de stations           | 1   | i4     | taux évolution |
| d2  | Evolution du nombre de points de recharge        | 1   | i1     | historique     |
| d3  | Nombre de sessions par point de recharge         | 2   | u3     | historique     |
| d4  | Taux de disponibilité par catégorie de puissance | 2   | q1, q3 | historique     |
| d5  | Taux de points de recharge avec indispo > 7 j    | 3   | q1, q3 | historique     |

Nota : Seule la périodicité est intégrée à la codification (voir chapitre 'codification'), l'intervalle doit donc être ajouté à l'indicateur pour fournir un résultat.

```{admonition} Exemples
- Evolution du nombre mensuel de points de recharge pour 2024 par département : (d2-m---04, entre 01/01/2023 et le 01/01/2024)
```

### Indicateurs d'état

Il s'agit des indicateurs associés à un état de la base de données à un instant donné.

Il n'est imposé aucune structure spécifique pour les données incluses dans ces indicateurs.

On peut citer par exemple les besoins suivants :

- Suivre la liste des stations du réseau autoroutier
- (autres exemples à indiquer)

Le calcul des indicateurs temporels doit pouvoir être réalisé en optimisant les temps de calcul et le volume de données stockées (il serait, par exemple, couteux de calculer une valeur annuelle à partir de données horaires).

#### Principes d'historisation

L'historisation ne fait l'objet d'aucun traitement statistique ni de retraitement temporel.

#### Périodicité

L'historisation peut s'effectuer avec une périodicité quelconque.

Pour un indicateur, on historise une valeur principale ainsi qu'un ensemble de valeurs additionnelles.

- valeur principale :
  - valeur numérique spécifique de chaque indicateur
- valeurs additionnelles :
  - ensemble de valeurs spécifique de chaque indicateur

#### Mise en oeuvre

Le résultat de l'indicateur d'état est identique à la valeur historisée.

Un indicateur d'état est donc défini par :

- l'indicateur de base à utiliser,
- la date de l'état pris en compte,
- la périodicité,
- la valeur historisée,

```{admonition} Exemple
L'indicateur de la liste des stations du réseau autoroutier au 01/01/2024 est défini par :

- l'indicateur de base : 'e1---04',
- l'intervalle : entre le 01/01/2023 et le 01/01/2024,
- la périodicité : mensuelle,
- la fonction : taux d'évolution (valeur mensuelle fin - valeur mensuelle début) / valeur mensuelle début.

Le résultat est obtenu en appliquant les traitements suivants:

- calcul quotidien de l'indicateur 'i4--04' sur les données statiques courantes,
- chaque jour, historisation du résultat du calcul,
- chaque mois, historisation du jeu de valeurs mensuel obtenu à partir des données quotidiennes,
- calcul du taux d'évolution sur les données de l'historisation mensuelle.
```

#### Indicateurs retenus

Les indicateurs temporels identifiés (voir présentation des indicateurs) sont les suivants :

| id  | nom                                              | Pr  | base   | fonction       |
| --- | ------------------------------------------------ | --- | ------ | -------------- |
| d1  | Taux d'évolution du nombre de stations           | 1   | i4     | taux évolution |

## Historisation

L'historisation est à effectuer pour les indicateurs suivants (voir chapitre listant les indicateurs): 

- infrastructure - typologie (mensuel) : t1, t5, t7, t8, t9
- infrastructure - quantitatif (mensuel) : i1, i4, i7
- infrastructure - autoroute (mensuel) : a5, a6
- usage - quantitatif: u1 (mensuel), u3 (quotidien)
- usage - qualité de service : q1 (quotidien), q2 (quotidien), q5 (mensuel)
- état : e1 (mensuel)

Pour tenir compte de la variabilité des propriétés à historiser, celles-ci sont stockées dans un champ JSON.

Plusieurs solutions sont envisageables (pour chaque niveau d'historisation):

- solution 1 : une table avec les résultats des indicateurs (plusieurs lignes par indicateur)
- solution 1bis : une table avec un champ JSON pour les valeurs (plusieurs lignes par indicateur)
- solution 2 : une table avec une valeur JSON par indicateur (une ligne par indicateur)
- solution 3 : une table avec une valeur JSON pour l'ensemble des indicateurs (une ligne pour tous les indicateurs)

### Solution 1

Chaque résultat d'un indicateur a une structure identique, on peut donc stocker tous les résultats d'un indicateur dans une table.
Les indicateurs temporels s'appuient sur les indicateurs historisés, il suffit donc d'effectuer une recherche par rapport à un indicateur.

Pour faciliter les purges, on peut avoir une table par périodicité, la purge peut alors s'effectuer simplement par tri sur le timestamp.

Une table comporte les champs suivants :

Propriétés

- value (JSON)
  - quantite
  - moyenne
  - variance (optionnel)
  - mini (optionnel)
  - maxi (optionnel)
  - dernier (optionnel)

Regroupement

- crit_v : valeur du critère (ex. niveau de puissance, implantation)

Indicateur (ex. 't1-01-93-04)

- query: (ex. 't1')
- périmètre: (ex. '01')
- valeur de périmètre: (ex. '93')
- critère: (ex.'04')

Datation

- timestamp

exemple du nombre mensuel de stations par opérateur en PACA :

| quantite | moyenne | crit_v  | query | perim | perim_v | crit | timestamp |
| -------- | ------- | ------- | ----- | ----- | ------- | ---- | --------- |
| 30       | 50      | 'oper1' | 't8'  | '01'  | '93'    | ''   | xxxxxxx   |
| 30       | 80      | 'oper2' | 't8'  | '01'  | '93'    | ''   | xxxxxxx   |
| 30       | 100     | 'oper3' | 't8'  | '01'  | '93'    | ''   | xxxxxxx   |

L'opérateur 'oper1' dispose pour le mois 'xxxxxxx' d'une moyenne de 50 stations :

```{admonition} Exemple d'utilisation
indicateur d1 : 'taux d'évolution du nombre de stations par département' sur 12 mois au 01/01/2024 '

- recherche dans la table mensuelle les lignes correspondant à 't4-00-00-04' et avec un timestamp entre le 01/01/2023 et le 01/01/2024
- calcul du taux d'évolution pour chaque département (1 - valeur moyenne du dernier mois / valeur moyenne du premier mois)

Le passage d'une table à une autre s'effectue en calculant les nouvelles valeurs 'nombre' et 'somme' pour chaque couple indicateur - 'crit_v' avec un timestamp compris dans l'intervalle de la période à historiser.
```

### Solution 1bis

Idem Solution 1 mais avec les propriétés stockée dans le champ JSON 'value'.

:::{admonition} Exemple
'nombre de station par opérateur'

| value    | crit_v  | query | perim | perim_v | crit | timestamp |
| -------- | ------- | ----- | ----- | ------- | ---- | --------- |
| json_op1 | 'oper1' | 't8'  | '01'  | '93'    | ''   | xxxxxxx   |
| json_op2 | 'oper2' | 't8'  | '01'  | '93'    | ''   | xxxxxxx   |
| json_op3 | 'oper3' | 't8'  | '01'  | '93'    | ''   | xxxxxxx   |

avec json_op1 :

```json
    {'nombre ': 30, 'moyenne': 50} 
```

:::

### Solution 2

Idem Solution 1bis mais avec une ligne par indicateur stocké dans un JSON.

:::{admonition} Exemple
'nombre de station par opérateur'

| result   | query | perim | perim_v | crit | timestamp |
| -------- | ----- | ----- | ------- | ---- | --------- |
| json_res | 't8'  | '01'  | '93'    | ''   | xxxxxxx   |

avec json_res :

```json
[
    {'crit_v': 'oper1', 'value': {'nombre ': 30, 'moyenne': 50}},
    {'crit_v': 'oper2', 'value': {'nombre ': 28, 'moyenne': 52.1}},
    {'crit_v': 'oper3', 'value': {'nombre ': 31, 'moyenne': 55 }}
]
```

:::

### Solution 3

Idem solution 2 mais avec une ligne commune pour tous les indicateurs, les résultats des indicateurs sont stockés dans un JSON

:::{admonition} Exemple
JSON commun avec les indicateurs du nombre de stations (i4), de points de charge (i1) et la puissance installée (i7) pour chaque commune, département, opérateur et région.

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

```python
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

:::

### Avantages - inconvenients

Les solutions sont comparées sur la base des fonctions suivantes :

- historisation initiale des données
- changement d'échelle de temps
- calcul de l'indicateur temporel
- purge des données
- évolutivité

#### solution 1

historisation :

- fonction générique : le format de stockage est identique au résultat de la requête

changement d'échelle

- fonction générique : calcul des nouvelles données par requête (nombre, somme)

calcul de l'indicateur

- indépendant de la périodicité
- générique / spécifique : à préciser

purge des données

- suppression de lignes en fonction de la valeur du timestamp

évolutivité

- ajout d'indicateur sans reconfiguration nécessaire

#### solution 2

historisation :

- fonction générique : conversion au format Json du résultat des requêtes

changement d'échelle

- fonction générique : à préciser (traitement par pandas nécessaire ?)

calcul de l'indicateur

- indépendant de la périodicité
- générique / spécifique : à préciser (conversion json nécessaire)

purge des données

- suppression de lignes en fonction de la valeur du timestamp

évolutivité

- ajout d'indicateur sans reconfiguration nécessaire

#### solution 3

historisation :

- ne peut se faire indicateur par indicateur
- nécessite de construire le json global (mapping entre indicateur et les 'key' du json)

changement d'échelle

- décodage préalable du format json et traitement de chaque 'key'

calcul de l'indicateur

- indépendant de la périodicité
- décodage préalable du format json et traitement de chaque 'key'

purge des données

- suppression de lignes en fonction de la valeur du timestamp

évolutivité

- l'ajout d'indicateur nécessite de reconfigurer le format JSON. La cohabitation de plusieurs formats JSON différents est à étudier