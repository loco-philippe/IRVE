# Planification écologique

## Disponibilité d'un réseau

Les bornes sont regroupées sur un graphe orienté (une station est un sommet, un arc est un trajet entre deux stations défini par une distance).

Le traitement consiste à :

- associer un état à chaque sommet : le sommet est valide si la station est disponible
- associer un état à chaque arc : l'arc est non valide s'il n'existe aucun sommet aval valide à moins de 60 km

L'application concerne principalement le réseau autoroutier en intégrant les stations de recharge situées sur les aires de l'autoroute ainsi que celles situées à moins de 3 km d'une sortie.

La mise en oeuvre nécessite:

- d'identifier les stations de recharge sur l'emprise de l'autoroute et celles incluses dans une bande de 3 km de part et d'autre,
- de construire le réseau entre les stations internes et les sorties de l'autoroute,
- d'jouter des arcs entre les stations externes et les sorties les plus proches,
- d'associer les stations à un sens de circulation (pour les stations internes),