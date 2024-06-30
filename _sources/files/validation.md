# Anomalie de consommation

La quantité d'énergie déclarée par un opérateur correspond à la somme des consommations de chaque session. Les anomalies recherchées concernent les surestimations de consommation (conduisent à une surévaluation des subventions).

Les causes peuvent être :

- un périmètre erroné (prise en compte de point de recharge externes)
- un nombre de sessions surévalué,
- des sessions avec des consommations surévaluées

La première analyse consiste à comparer la consommation totale des sessions à la consommation des points de livraison associé aux stations considérées. Pour que la comparaison soit valide, il est nécessaire de disposer dans QualiCharge des informations permettant ce calcul. En particulier:

- l'ensemble des consommations des sessions
- les évènements qui affectent les stations (ex. changement d'opérateur ...)

Un deuxième niveau consiste à analyser la série temporelle des consommations de chaque point de recharge ou de chaque station de façon à identifier des paramètres caractéristiques (analyse spectrale, auto-corélation, filtrage, corrélation entre points de recharge d'une même station). Les variations anormales de ces paramètres peuvent être enregistrées sous forme d'anomalies. Les indicateurs d'anomalies permettent de cibler des analyses approfondies à engager.
