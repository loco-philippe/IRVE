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

- début et fin de charge,
- mise hors service et remise en service
- désactivation

Le calcul de la qualité de service (disponibilité opérationnelle, taux d'utilisation, saturation) s'effectue alors par cumul des durées dans les états associés aux indicateurs.

::::{note}
Si les évènements d'arrêt distinguent les défauts et les OT (ordre de travail de maintenance préventive ou corrective), le mode hors service serait le suivant:
:::{mermaid}
flowchart TB
    fonc[en_service] -->|défaut| pan
    pan -->|fin défaut| fonc
    fonc -->|mise à l'arrêt| maint
    maint --mise en service--> fonc
    subgraph hors_service
        pan(panne) -->|intervention / OT| maint(maintenance)
    end
:::
*figure 3 :* *Diagramme d'états non fonctionnement*
::::

## Etats des stations

A préciser
