# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 15:06:09 2024

@author: philippe.thomy@beta.gouv.fr
"""

import json
import ntv_pandas as npd
import pathlib
import matplotlib.pyplot as plt


import pandas as pd
from util_carto import Cart

#chemin = str(pathlib.Path(npd.__file__).parent.parent.parent/"Environmental-Sensing"/"python"/"Validation"/"irve"/"Analyse")

def indicateurs(chemin):
    dic = {}
    with open(chemin + '/' + 'logfile.txt', 'r', encoding="utf-8") as f:
        for line in f:
            if len(line) > 3:
                log = json.loads(line)
                dic[log['date_irve']] = log
    return list(tuple(zip(*sorted(zip(list(dic.keys()),dic.values()))))[1])

def defaut_integrite(indic):
    '''génération d'un graphe présentant la répartition des défauts d'intégrité''' 
    seuil = 1 # les valeurs inférieures à ce pourcentage ne sont pas prises
    defauts = ['Pdc non unique', 'Station multi-operateurs', 'Station multi-enseignes', 'Station multi-localisations', 
               'Pdc multi-stations', 'station avec plusieurs noms', 'station multi-implantations', 
               'nombre de pdc par station incoherent', 'station multi-acces', 'station multi-horaires', 
               'acces deux-roues incoherent', 'localisation multi-adresses']
    val = dict(item for item in indic[-1].items() if item[0] in defauts and item[1] > 0)
    val = dict(sorted(val.items(), key=lambda item:item[1], reverse=False))
    date = indic[-1]['date_irve']
    total = indic[-1]['IRVE_itinerance_residuel' + date + '.csv']
    operateurs = [oper.split(sep='@')[1].split('.')[0] for oper in indic[-1]['operateurs']] + ['autres']
    defauts = indic[-1]['erreurs_operateurs'] + [total - sum(indic[-1]['erreurs_operateurs'])]
    mini = min(list(val.values()).index(value) for value in val.values() if value / sum(val.values()) *100 > seuil)

    fig, (ax, ax2) = plt.subplots(2, 1, layout='constrained', figsize=(8, 7))
    ax.pie(list(val.values())[mini:], autopct='%.0f%%', labels=list(val.keys())[mini:])
    ax.set_title("Répartition des défauts d'intégrité - " + date)
    ax2.bar(operateurs, defauts, width=0.5)
    plt.setp(ax2.get_xticklabels(), rotation=20, ha="right")
    ax2.set_title("Principaux défauts par opérateur")
    plt.show()
    return date

def doublons(log):
    '''génération d'un graphe présentant l'évolution du nombre de doublons pdc + stations'''
    
    dic = {}
    for i, indic in enumerate(log):
        if i == 0:
            dic['date'] = []
            dic['pdc doublon'] = []
            dic['pdc sans doublon'] = []
            dic['pdc doublon %'] = []
        else:
            date = indic['date_irve']
            dic['date'].append(date)
            doublon = indic['IRVE_itinerance_doublons' + date + '.csv']
            dic['pdc doublon'].append(doublon)
            dic['pdc sans doublon'].append(indic['IRVE_itinerance_complet'   + date + '.csv'] - doublon)
            dic['pdc doublon %'].append(100 * dic['pdc doublon'][-1] / (dic['pdc doublon'][-1] + dic['pdc sans doublon'][-1]))
    fig, (ax2, ax1) = plt.subplots(2, 1, layout='constrained', figsize=(8, 6))
    ax1.plot(dic['date'], dic['pdc doublon %'])
    ax1.set_title('Evolution du % de doublons pdc')
    plt.setp(ax1.get_xticklabels(), rotation=40, ha="right")
    bottom = [0] * (len(log) - 1)
    ax2.bar(dic['date'], dic['pdc sans doublon'], width=0.5, label='pdc sans doublon', bottom=[0] * (len(log) - 1))
    ax2.bar(dic['date'], dic['pdc doublon'], width=0.5, label='pdc avec doublon', bottom=dic['pdc sans doublon'])
    ax2.set_title("Evolution du nombre de points de recharge IRVE (avec doublons)")
    plt.setp(ax2.get_xticklabels(), rotation=40, ha="right")
    ax2.legend(loc="lower right")
    plt.show()

def evolution(log):
    '''génération d'un graphe présentant l'évolution du nombre de pdc valides ou présentant des défauts'''
    
    dic = {}
    for i, indic in enumerate(log):
        if i == 0:
            dic['date'] = []
            dic['pdc defaut'] = []
            dic['pdc valide'] = []
            dic['pdc defaut %'] = []
            dic['pdc'] = []
        else:
            date = indic['date_irve']
            dic['date'].append(date)
            dic['pdc defaut'].append(indic['IRVE_itinerance_residuel' + date + '.csv'])
            dic['pdc valide'].append(indic['IRVE_itinerance_valide'   + date + '.csv'])
            dic['pdc defaut %'].append(100 * dic['pdc defaut'][-1] / (dic['pdc defaut'][-1] + dic['pdc valide'][-1]))
            dic['pdc'].append(dic['pdc defaut'][-1] + dic['pdc valide'][-1])
    pd.DataFrame(dic).to_csv('evolution.csv')
    print('pdc valide : ', dic['pdc valide'][-1])
    print('pdc defaut : ', dic['pdc defaut'][-1])
    fig, (ax2, ax1, ax3) = plt.subplots(3, 1, layout='constrained', figsize=(8, 9))
    ax1.plot(dic['date'], dic['pdc defaut %'])
    ax1.set_title('Evolution du % de pdc en défaut (hors doublons)')
    plt.setp(ax1.get_xticklabels(), rotation=40, ha="right")
    
    ax3.bar(dic['date'], dic['pdc defaut'], width=1, label='pdc defaut', bottom=[0] * (len(log) - 1))
    ax3.set_title('Evolution du nombre de pdc en défaut')
    plt.setp(ax3.get_xticklabels(), rotation=40, ha="right")
    
    # bottom = [0] * (len(log) - 1)
    ax2.bar(dic['date'], dic['pdc valide'], width=0.5, label='pdc valide', bottom=[0] * (len(log) - 1))
    ax2.bar(dic['date'], dic['pdc defaut'], width=0.5, label='pdc avec défaut', bottom=dic['pdc valide'])
    ax2.set_title("Evolution du nombre de points de recharge IRVE (hors doublons)")
    plt.setp(ax2.get_xticklabels(), rotation=40, ha="right")
    ax2.legend(loc="lower right")
    plt.show()  
    
def defaut_carte(date, chemin):
    '''génération d'une carte folium des stations présentant des défauts d'intégrité'''
    
    file = 'IRVE_itinerance_residuel'+date+'.csv'
    irve = pd.read_csv(chemin + '/' + file, sep=',', low_memory=False)
    
    principal = [17, 18, 19, 20, 21]
    irve['principal'] = True
    for ind in principal:
        irve['principal'] &= irve.iloc[:,ind]
    irve_p = irve[~irve['principal']].drop_duplicates('id_station_itinerance').reset_index(drop=True)
    
    secondaire = [22, 23, 24, 25, 26, 27, 28]
    irve['secondaire'] = True
    for ind in secondaire:
        irve['secondaire'] &= irve.iloc[:,ind]
    irve['secondaire'] |= (~irve['principal'] & ~irve['secondaire'])
    irve_s = irve[~irve['secondaire']].drop_duplicates('id_station_itinerance').reset_index(drop=True)
    
    popup = [[], []]
    locat = [[], []]
    vide = {'  ': '  '}
    for ind, irve in enumerate((irve_p, irve_s)):
        for i in range(len(irve)):
            defauts = {irve_p.columns[col]: False  for col in range(17, 29) if not irve.iloc[i,col]}
            popup[ind].append( {'id_station': irve['id_station_itinerance'][i], 
                               'id_pdc': irve['id_pdc_itinerance'][i],
                               'contact_operateur': irve['contact_operateur'][i],
                               'nom_enseigne': irve['nom_enseigne'][i],
                               'nom_station': irve['nom_station'][i],
                               'adresse_station': irve['adresse_station'][i],
                               'fichier des écarts': '<a href="https://github.com/loco-philippe/Environmental-Sensing/blob/main/python/Validation/irve/Analyse/">IRVE_itinerance_residuel</a>',
                               'date du fichier': date } | vide | defauts )
            coord = json.loads(irve['coordonneesXY'][i])
            coord.reverse()
            locat[ind].append(coord)

    cart = Cart([47, 2.5], zoom_start=6)
    cart.add_markers(locat[0], popup=popup[0], color='red', group='écarts entités', max_width=250)
    cart.add_markers(locat[1], popup=popup[1], color='orange', group='écarts attributs', max_width=250, icon='bug')
    return cart
