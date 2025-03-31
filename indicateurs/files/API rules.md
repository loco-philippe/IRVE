# API rules

## data model rules

In a set of static items, certain fields must be identical for each item :

- with the same `id_pdc_itinerance`:
  - nom_amenageur, siren_amenageur, contact_amenageur
  - nom_operateur, contact_operateur, telephone_operateur
  - nom_enseigne
  - nom_station, implantation_station, integer nbre_pdc, condition_acces, horaires, station_deux_roues, date_maj, num_pdl, id_station_local, raccordement, date_mise_en_service
  - coordonneesXY, adresse_station, code_insee_commune

- with the same `coordonneesXY`:
  - adresse_station, code_insee_commune

If one of these cases occurs,

- with the bulk API type, the API returns an error,
- With the simple post/put API, the field value overwrites the existing value.
