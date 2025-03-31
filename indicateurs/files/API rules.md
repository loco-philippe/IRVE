# API rules

## data model rules

In a set of static items, some fields must be identical :

- for each item with the same `id_pdc_itinerance`:
    - nom_amenageur, siren_amenageur, contact_amenageur
    - nom_operateur, contact_operateur, telephone_operateur
    - nom_enseigne
    - nom_station, implantation_station, integer nbre_pdc, condition_acces, horaires, station_deux_roues, date_maj, num_pdl, id_station_local, raccordement, date_mise_en_service
    - coordonneesXY, adresse_station, code_insee_commune

- for each item with the same `coordonneesXY`:
    - adresse_station, code_insee_commune

With the bulk API endpoint, if one of those cases appears, the API return an error.
With the simple post / put API endpoints, if one of those case appears the value of the field replaces the existing value.

