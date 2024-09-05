
import geopandas as gpd
import pandas as pd
import json
import shapely

def get_geom(filename):
    file = open(filename)
    contour = json.load(file)
    file.close()
    geom = []
    for feature in contour['features']:
        code = feature['properties']['code']
        try: 
            poly = shapely.from_geojson(json.dumps(feature['geometry']))
        except: 
            poly = None
        geom.append((code, poly))
    return pd.DataFrame.from_records(geom, columns=['code', 'geometry'])

chemin = "D:/philippe/python ESstandard/IRVE/sources/data_quali/"
# df_geo = get_geom(chemin + 'communes-100m.geojson')
df_geo = get_geom(chemin + 'regions-100m.geojson')
print(df_geo)

gdf_geo = gpd.GeoDataFrame(df_geo, crs=4326).to_crs(5490)
# gdf_geo = gpd.GeoDataFrame(df_geo, crs=4326).to_crs(4471)
gdf_geo['area'] = gdf_geo['geometry'].area

print(gdf_geo)

'''
crs (hors territoires outre-mer):
    metropole 2154 / 9794
    antilles 4559 / 5490
    guyane 2972
    mayotte 4471

tests : 
    
    briord 01064 12.3 km2 -> resultat 12.24 (crs 2154 / 9794)
    pointe à pitre 97120 2.66 km2 -> resultat 2.657 (crs 4559)
    cayenne 97302 23.6 km2 -> resultat 24.91 (crs 2972)
    mamoudzou 97611 41.94 km2 -> resultat 41.71 (crs 4471)
    
    
    bourgogne 27  47784 km2 -> résultat 47981 (crs 2154) 
    guadeloupe 01 1628 km2 -> résultat 1632 (crs 4559)
    guyane 03 83534 km2 -> résultat 83200 (crs 2972)
    mayotte 06 374 km2 -> résultat 365 (crs 4471)


autres
    st pierre 4467
    polynésie 3297

saint pierre 97502 25 km2 -> résultat  absent
'''

