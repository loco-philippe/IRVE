# Critères de filtrage ou d'agrégation

Les types de critères à appliquer pour sélectionner les données sont les suivants

- géographique :

  - Filtres identifiés : région, *département*
  - Dans un premier temps le code postal peut être utilisé, un découpage plus fin ou différent (arrondissement, IRIS, ...) ou spécifique (ex. boite englobante) n'est pas nécessaire dans un premier temps
  - Si un niveau de granularité différent du CP est retenu, il devra être représenté par un attribut dans la base de données pour faciliter les requètes. Le calcul de cet attribut pourra alors s'effectuer à partir des coordonnées (test d'appartenance d'un point dans un contour).
  - La décision sera prise en fonction de l'analyse des données existantes (comparaison code postal / coordonnées)

- temporel :
  Les critères sont liés aux précisions ci-dessous

  - horodatage données statiques : Le niveau retenu est la date (précision supérieure à confirmer suivant la gestion de l'historique des données) pour notamment permettre une comparaison entre deux dates
  - horodatage données dynamiques : seconde (précision supérieure : type datetime)
  - période : semaine, mois, trimestre, année, entre deux dates

- organisation :

  - opérateur (email): seule l'adresse email est obligatoire
  - enseigne (nom): seul le nom commercial du réseau est obligatoire

- stations :

  - attributs du modèle statique (implantation, condition d'accès, horaires, station 2 roues): les autres attributs sont facultatifs

- point de recharge :

  - site d'implantation (parking privé/public, voirie, charge rapide). Quelle disponibilité pour les autres infos Avere (ex. commerce, entreprise) ?
  - puissance. Classification à définir. Ex. 0-7,4 / 7,4-22 / 22-50 / 50-150 / 150-350 / > 350
  - alimentation AC/DC, ce critère est intéressant mais n'est pas disponible actuellement
  - l'analyse des données est à effectuer au préalable pour connaître la répartition (sites / puissance)

- usage :
  - *type de session*. A définir. Ex. Non réussie, partielle (charge interrompue), réussie
  - *type de charge*. Typologie à construire à partir des caractéristiques de la charge (durée, puissance, période) en fonction des relevés (ex. forte charge et rapide (autoroute), lente et longue de nuit (résidentiel)...)
  - *tarification*. A préciser.

- disponibilité d'un point de recharge (ce point est à regarder en liaison avec les chartes et définition de l'AFIREV):

  - *phases*. Typologie à définir. Ex. occupée, libre, pannes courtes (< 2h), pannes longues (< 24h), maintenance (< 7j), maintenance longue (> 7j), fermée (hors panne, hors maintenance et hors ouverture)
  - temps dans une phase / temps d'ouverture (ex. 80% du temps en fonctionnement)
  - nombre de périodes (ex. nombre de pannes longues sur un mois)

- disponibilité d'une station (ce point est à regarder en liaison avec les chartes et définition de l'AFIREV):

  - *phases*. Typologie à définir. Ex. accessible (> 1 pdc libre), peu accessible (1 pdc libre), occupée (0 pdc libre), en panne (tous les pdc en panne ou en maintenance), fermée