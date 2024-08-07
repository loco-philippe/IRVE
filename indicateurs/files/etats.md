# Etat des stations et points de recharge

## Etats des points de recharge

Trois états principaux sont définis :

- libre: En fonctionnement, non occupé et pendant la période d'ouverture
- occupé: En charge
- hors service: Mise à l'arrêt (ex. maintenance) ou arrêt intempestif (défaillance : statut erreur ou inconnu). Quatre niveaux définis en fonction du temps de présence dans cet état sont retenus:

  - interruption courte < 2h,
  - interruption longue < 24h,
  - arrêt court < 7j,
  - arrêt long > 7j.

Deux états complémentaires peuvent être ajoutés:

- déclaré: Identifié dans Qualicharge mais avec aucune charge encore effectuée
- désactivé: Identifié dans Qualicharge mais non pris en compte dans le suivi d'usage.

```{mermaid}
flowchart TB
    déclaré -->|début charge| occ   
    occ -->|arrêt| hs
    subgraph en_service
        direction RL
        lib(libre) -->|début charge| occ(occupé)
        occ -->|fin charge| lib
    end  
    hs(hors service) -->|fin arrêt| lib
    hs -->|désactivation| desactivé 
```

*figure 1 :* *Diagramme d'états*

Chacun des trois états (libre, occupé, hors service) est doublé pour tenir compte des périodes d'ouverture du point de recharge.

- requis: pendant la période d'ouverture,
- non requis: hors période d'ouverture.

```{mermaid}
flowchart LR
    req(requis\n occupé, libre, hors service) -->|fin ouverture| nreq(non requis\n occupé, libre, hors service)
    nreq --> |début ouverture| req 
```

*figure 2 :* *Diagramme d'états ouverture*

Le suivi des états permet d'enregistrer dans une table dédiée les durées passées dans chaque état successif (mode non échantillonné) ou bien l'état pour chaque pas de temps (mode échantillonné).

Il suppose que les évènements suivant soient bien enregistrés:

- début et fin de charge (table 'session'),
- mise hors service et remise en service (table à construire)
- désactivation

Le calcul de la qualité de service (disponibilité opérationnelle, taux d'utilisation, saturation) s'effectue alors par cumul des durées dans les états associés aux indicateurs.

## Etats des stations

A préciser
