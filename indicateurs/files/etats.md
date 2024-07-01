# Etat des stations et points de recharge

## Etats des points de recharge

Les états sont les suivants :

- déclaré: Identifié dans Qualicharge mais avec aucune charge encore effectuée
- inactif: En fonctionnement, hors période d'ouverture
- libre: En fonctionnement, non occupé et pendant la période d'ouverture
- occupé: En charge
- hors service: Mise à l'arrêt (ex. maintenance) ou arrêt intempestif (défaillance : statut erreur ou inconnu). Quatre niveaux définis en fonction du temps de présence dans cet état sont retenus:

  - pannes courtes < 2h,
  - pannes longues < 24h,
  - arrêt < 7j,
  - arrêt > 7j.

- désactivé: Identifié dans Qualicharge mais non pris en compte dans le suivi d'usage.

Le diagramme d'état correspondant à ces états est présenté ci-dessous. Il suppose que les évènements suivant sont bien enregistrés:

- début et fin de charge,
- mise hors service et remise en service
- désactivation

Le suivi des états permet d'enregistrer dans une table dédiée les durées passées dans chaque état successif.
Le calcul de la disponibilité et du taux d'utilisation s'effectue alors par cumul de ces durées.

```{mermaid}
flowchart TB
    déclaré -->|début charge| occ(occupé)   
    occ --> |fin charge| en_service
    lib -->|début charge| occ 
    subgraph en_service
        lib(libre) -->|fin ouverture| ina
        ina(inactif) -->|début ouverture| lib
    end  
    arr(hors service) -->|fin arrêt| en_service
    occ -->|arrêt| arr
    arr -->|désactivation| desactivé 
```

*figure 1 :* *Diagramme d'états fonctionnement*

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
*figure 2 :* *Diagramme d'états non fonctionnement*
::::
