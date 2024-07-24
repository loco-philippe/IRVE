# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 22:34:43 2024

@author: a lab in the Air
"""

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
            box = shapely.bounds(poly).tolist()
        except: 
            poly = None
            box = [0.0, 0.0, 0.0, 0.0]
        geom.append((code, box, poly))
    return pd.DataFrame.from_records(geom, columns=['code', 'box', 'poly'])

def in_box(point, box):
    return box[0] <= point[0] <= box[2] and box[1] <= point[1] <= box[3]

def get_com(coord, data_ref):
    reg, dpt, com, reg_geo, dpt_geo, com_geo, comidx = data_ref
    reg_ok = reg_geo.apply(lambda x: in_box(coord, x['box']), axis=1)
    reg_geo_ok = list(reg_geo[reg_ok]['code'])
    
    dpt_sel = list(dpt[dpt['REG'].isin(reg_geo_ok)]['DEP'])
    dpt_sel_geo = dpt_geo[dpt_geo['code'].isin(dpt_sel)]
    dpt_ok = dpt_sel_geo.apply(lambda x: in_box(coord, x['box']), axis=1)
    dpt_geo_ok = list(dpt_sel_geo[dpt_ok]['code'])

    com_sel = list(com[com['DEP'].isin(dpt_geo_ok)]['COM'])
    com_sel_geo = com_geo[com_geo['code'].isin(com_sel)]
    com_ok = com_sel_geo.apply(lambda x: in_box(coord, x['box']), axis=1)
    com_geo_ok = list(com_sel_geo[com_ok]['code'])
    
    for commune in com_geo_ok:
        poly = com_geo.loc[com_geo['code'] == commune, :]['poly'].iloc[0]
        if shapely.contains_xy(poly, coord[0], coord[1]):
            com_att=comidx.loc[commune]
            return (commune, com_att['DEP'], com_att['REG'])
    return (None, None, None)
        
    
chemin = "D:/philippe/python ESstandard/IRVE/sources/data_quali/"
columns=['code', 'box', 'poly']
reg_geo = get_geom(chemin + 'regions-version-simplifiee.geojson')
dpt_geo = get_geom(chemin + 'departements-version-simplifiee.geojson')
com_geo = get_geom(chemin + 'communes-version-simplifiee.geojson')
reg = pd.read_csv(chemin + 'v_region_2024.csv')
dpt = pd.read_csv(chemin + 'v_departement_2024.csv').astype('str')
com = pd.read_csv(chemin + 'v_commune_2024.csv', dtype='str')
comidx = com.set_index('COM')
data_ref = (reg, dpt, com, reg_geo, dpt_geo, com_geo, comidx)

coord = [5, 47]
com_ok, dep_ok, reg_ok = get_com(coord, data_ref)

print(com_ok, dep_ok, reg_ok)
print(com_geo[com_geo['code']==com_ok]['box'].iloc[0])


'''
loc = pd.read_csv('./data_quali/query_result_2024-07-24_loc.csv')
#print(len(df))
nb = len(loc)
print(nb)
df = set_localisation(nb)
loc_adm = pd.concat([loc, df], axis=1)
loc_adm.to_csv('./data_quali/loc_adm.csv')

print(loc_adm)
print(df['region'].dtype)
#print(df.columns)
#print([random.randint(0,2) for i in range(442)])
'''