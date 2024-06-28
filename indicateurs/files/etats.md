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
    init(déclaré) -->|début charge| occ(occupé)   
    subgraph fonctionnement
        direction TB
        occ --> |fin charge si ouverture| lib(libre)
        occ --> |fin charge| ina(inactif)
        ina -->|début ouverture| lib
        lib -->|fin ouverture| ina
    end    
    lib -->|début charge| occ 
```

*figure 1 :* *Diagramme d'états fonctionnement*

```{mermaid}
flowchart TD
    fonc[fonctionnement] -->|début défaut| pan(panne)
    pan -->|fin défaut| fonc
    pan -->|début OT| maint(maintenance)
    fonc -->|début OT| maint
    maint -->|fin OT| fonc
```

*figure 2 :* *Diagramme d'états non fonctionnement*
