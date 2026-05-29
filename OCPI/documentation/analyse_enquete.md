# Analyse des données fournies par l'enquête

## Données TESLA

2 fichiers (locations et tariffs)

- locations : 262 stations
- tariffs : 262 tarifs

Exemple

- locations/evses/evse_id : "FR\*TSL\*EA4QY2C"
  - location/evses/connectors/tariff_ids : "5fa1c37d-9aa9-4778-805b-8a1c1299765d" (id du tariff dans le fichier des tarifs)
- tariffs/5fa1c37d-9aa9-4778-805b-8a1c1299765d :
  - "start_date_time": "2026-03-25T23:00:00Z"
  - "last_updated": "2026-03-26T01:20:54Z"
- qualicharge : FRTSLEA4QY2C (id_pdc_itinerance)
