# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 11:11:23 2024

@author: phili
"""

import pandas as pd

url = 'https://unpkg.com/@etalab/decoupage-administratif@4.0.0/data/communes.json'
pop = pd.read_json(url).loc[:,['code', 'population']]
print(pop)