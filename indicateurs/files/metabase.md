# utilisation de Metabase

## Choroplethe

1 - Admin settings / Maps / add a map

saisie : name, URL (geojson), id (property geojson), name (property geojson)

exemple : https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-version-simplifiee.geojson (property_id = code_region)

2 - `Model` (table simplifiée) avec un champ correspondant au id + champ valeur

mode simple : upload .csv dans une `collection`

exemple (COG) : https://www.insee.fr/fr/information/7766585 (csv avec code_region )

3 - Création de la `question`

A partir du `model`, choisir uniquement la visualisation de type map, choisir la map créée en 1, associer les champs

4 - Résultat

## exemple requête SQL

```sql
SELECT
  loc_with_commune_20240725082159.commune,
  SUM(PointDeCharge.puissance_nominale) AS "sum"
FROM
  PointDeCharge
  INNER JOIN Station ON PointDeCharge.station_id = Station.id
  INNER JOIN loc_with_commune_20240725082159 ON Station.localisation_id :: text = loc_with_commune_20240725082159.id
GROUP BY
  loc_with_commune_20240725082159.commune
  ```
