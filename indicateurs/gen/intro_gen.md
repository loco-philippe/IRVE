# Structuration

Les indicateurs sont obtenus par une combinaison de cinq notions:

- filtrage (sélection des données suivant un critère),
- agrégation (regroupement des données suivant un critère),
- valorisation (calcul d'un indicateur)
- évolution (écart entre deux valorisations)
- restitution (visualisation sous forme graphique)

Ils permettent de produire les indicateurs de référence ainsi que les indicateurs dédiés à un usage spécifique.

*Exemple:*

- *Pour la région PACA (filtrage), restitution du nombre de points de recharge (valorisation) par département (agrégation) et par opérateur (agrégation) au 1/1/2024 (filtrage)*
- *Même demande mais avec l'écart entre le 1/1/2024 et le 1/6/2024 (évolution)*

Le filtrage s'effectue via les API de de la base de données Qualicharge.
L'objectif est de pouvoir construire ces indicateurs dans l'outil de BI Metabase

Si besoin, les fonction d'agrégation ou de valorisation peuvent être validées au préalable via les outils d'analyse de données (ex. Pandas).
