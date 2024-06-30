# Modèle prédictif

L'analyse des séries temporelles permet d'identifier la dépendance entre des séries et de la modéliser.

Les méthodes de machine learning (en particulier les régressions) appliquées à ces séries (après élimination des "bruits") permettent de mesurer explicitement ces dépendances.

La modélisation permet alors de prédire leur évolution.

Par exemple:

- le taux d'indisponibilité d'une station est peut-être corrélé avec son niveau de consommation (rapporté à la puissance installée)
- Sur autoroute, il est peut-être également corrélé avec le niveau du trafic.

  Si ces dépendances sont avérées, il serait alors possible en fonction des données de trafic d'identifier les zones avec des infrastructures insuffisantes et les périodes à risque.