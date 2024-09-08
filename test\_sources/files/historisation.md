# Solutions pour l'historisation des données et les indicateurs temporels

Proposition de différentes solutions pour calculer des indicateurs temporels à des échelles de temps variables.

## Indicateurs temporels

### Caractéristiques

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

Les principes proposés pour cela sont les suivants :

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

### Mise en oeuvre

Chaque périodicité peut être associée à une (ou plusieurs) table purgée avec une fréquence spécifique. Par exemple, un stockage horaire pourrait être purgé chaque semaine ou chaque mois.

Le passage d'une périodicité à une autre est réalisé de façon automatique en appliquant une fonction simple. On distingue notamment:

- les données cumulables dont le passage à l'échelle se traduit par un cumul (somme). C'est le cas du nombre de session dont la valeur annuelle peut être calculée comme la somme des sessions mensuelles elles-mêmes calculées comme la somme des sessions quotidiennes,
- les données ajustables dont le passage à l'échelle se traduit par un ensemble de valeurs (moyenne, maxi, mini, dernière). Par exemple, la puissance moyenne installée de l'année peut être calculée à partir de la moyenne des puissances installées du mois elles-mêmes calculées à partir de la moyenne des puissances installées quotidiennes.

Le résultat de l'indicateur peut prendre plusieurs formes :

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
- la valeur historisée : dernière,
- la fonction : taux d'évolution (1 - valeur mensuelle début / valeur mensuelle fin).

Le résultat est obtenu en appliquant les traitements suivants:

- calcul quotidien de l'indicateur 'i4--04' sur les données statiques courantes,
- chaque jour, historisation du résultat du calcul,
- chaque mois, historisation du jeu de valeurs mensuel (moyenne, maxi, mini, dernière) obtenu à partir des données quotidiennes,
- calcul du taux d'évolution sur les données de l'historisation mensuelle (dernière valeur).
```
### Identification

Les indicateurs temporels identifiés sont les suivants :

| id  | nom                                              | Pr  | base | valeur   | fonction       |
| --- | ------------------------------------------------ | --- | ---- | -------- | -------------- |
| d1  | Taux d'évolution du nombre de stations           | 1   | i4   | dernière | taux évolution |
| d2  | Evolution du nombre de points de recharge        | 1   | i1   | dernière | historique     |
| d3  | Nombre de sessions par point de recharge         | 2   | u3   | somme    | historique     |
| d4  | Taux de disponibilité par catégorie de puissance | 2   | q7   | somme    | historique     |
| d5  | Taux de points de recharge avec indispo > 7 j    | 3   | q7   | moyenne  | historique     |

Nota : Seule la périodicité est intégrée à la codification (voir chapitre 'codification'), l'intervalle doit donc être ajouté à l'indicateur pour fournir un résultat.

```{admonition} Exemples
- Evolution du nombre mensuel de points de recharge pour 2024 par département : (d2-m---04, entre 01/01/2023 et le 01/01/2024)
```

## Historisation des données

L'historisation est à effectuer pour les indicateurs suivants (voir chapitre listant les indicateurs): 

- infrastructure - typologie (mensuel) : t1, t5, t7, t8, t9
- infrastructure - quantitatif (mensuel) : i1, i4, i7
- infrastructure - autoroute (mensuel) : a5, a6
- usage - quantitatif: u1 (mensuel), u3 (quotidien)
- usage - qualité de service : q1 (quotidien), q2 (quotidien), q5 (mensuel)

Plusieurs solutions sont envisageables :

- solution 1 : une table avec les paramètres et les résultats des indicateurs
- solution 2 : une table avec une valeur JSON par indicateur
- solution 3 : une table avec une valeur JSON    pour l'ensemble des indicateurs

### Solution 1

Chaque résultat d'un indicateur a une structure identique, on peut donc stocker tous les résultats d'un indicateur dans une table. 
Les indicateurs temporels s'appuient sur les indicateurs historisés, il suffit donc d'effectuer une recherche par rapport à un indicateur.

Pour faciliter les purges, on peut avoir une table par périodicité, la purge peut alors s'effectuer simplement par tri sur le timestamp.

Une table comporte les champs suivants :

Valeurs historisées

- min : valeur mini (ou 0 si donnée cumulée)
- max : valeur maxi (ou 0 si donnée cumulée)
- val : valeur moyenne (ou somme si donnée cumulée)
- last : dernière valeur (ou 0 si donnée cumulée)

Regroupement

- crit_v : valeur du critère (ex. niveau de puissance, implantation)

Indicateur (ex. 't1-01-93-04)

- query: (ex. 't1')
- périmètre: (ex. '01')
- valeur de périmètre: (ex. '93')
- critère: (ex.'04')

Datation

- timestamp

exemple du nombre de stations par oéprateur en PACA

| min | max | val | last | crit_v  | query | perim | perim_v | crit | timestamp |
| --- | --- | --- | ---- | ------- | ----- | ----- | ------- | ---- | --------- |
| 52  | 75  | 60  | 75   | 'oper1' | 't8'  | '01'  | '93'    | ''   | xxxxxxx   |
| 32  | 55  | 40  | 55   | 'oper2' | 't8'  | '01'  | '93'    | ''   | xxxxxxx   |
| 72  | 95  | 80  | 95   | 'oper3' | 't8'  | '01'  | '93'    | ''   | xxxxxxx   |

```{admonition} Exemple
'taux d'évolution du nombre de stations sur 12 mois au 01/01/2024 par département ' :

- recherche dans la table mensuelle les lignes avec 't4-00-00-04' avec un timestamp entre le 01/01/2023 et le 01/01/2024
- calcul du taux d'évolution pour chaque département ('val') à partir de la valeur 'last'

Le passage d'une table à une autre s'effectue en calculant les nouvelles valeurs min, max, val, last pour chaque couple indicateur - 'crit_v' avec un timestamp compris dans l'intervalle de la période à historiser.
```

### Solution 2

Idem Solution 1 mais avec une ligne par indicateur, le résultat de l'indicateur étant stocké dans un JSON.

:::{admonition} Exemple
'nombre de station par opérateur'

| json    | query | perim | perim_v | crit | timestamp |
| ------- | ----- | ----- | ------- | ---- | --------- |
| json_op | 't8'  | '93'  | '13'    | ''   |  xxxxxxx  |


avec json_op :
```
 [
    {'crit_v': 'oper1', 'min': 52, 'max': 75, 'val': 60, 'last': 75},
    {'crit_v': 'oper2', ...},
    ...
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

- fonction générique : calcul des nouvelles données par requête (min, max, mean), à préciser pour 'last'

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

## Indicateurs étendus

Ils concernent le couplage des données avec des jeux de données complémentaires (à définir dans un second temps):

- couplage consommation / trafic
- couplage nombre de véhicules électriques vendus/immatriculés
- couplage consommation / relevés ENEDIS des points de livraison
