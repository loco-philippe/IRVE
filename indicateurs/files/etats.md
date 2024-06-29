# Etat des stations et points de recharge

## Etats des points de recharge

Les états sont les suivants :

- déclaré: Identifié dans Qualicharge mais avec aucune charge effectuée
- inactif: En fonctionnement, hors période d'ouverture ou sur arrêt volontaire
- libre: En fonctionnement, non occupé et pendant la période d'ouverture
- occupé: En charge
- en panne: Présence d'un défaut depuis moins de 24h (deux types de pannes: pannes courtes < 2h, pannes longues (< 24h))
- en maintenance: Arrété pour intervention de maintenance corrective ou préventive (deux niveaux : arrêt < 7j, arrêt > 7j)

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

Si les évènements d'arrêt distinguent les défauts et les OT (ordre de travail de maintenance préventive ou corrective), le mode hors service serait le suivant:

```{mermaid}
flowchart TD
flowchart TB
    subgraph hors_service
        pan(panne) -->|début OT| maint(maintenance)
    end
    fonc[en_service] -->|début défaut| pan
    fonc -->|début OT| maint
    hors_service -->|remise en service| fonc
```

*figure 2 :* *Diagramme d'états non fonctionnement*
