"""
The `create_query` module includes query generators and indicator genarator for QualiCharge indicators.

Each 'query_xx' function is defined with:

Parameters
----------
param: tuple of two or three str 
    Indicator parameters (see indicator codification)
simple: boolean (default False)
    If False, additional columns are added in the result Table
gen: boolean (default False)
    If True, the query is generic (with variables) else the query is specific (with values)

Returns
-------
String
    SQL query to apply
"""

import pandas as pd
import sys

create_query = sys.modules[__name__]

P_TAB = """puissance(p_range, p_cat) AS (
        VALUES 
            (numrange(0, 15.0), 1), 
            (numrange(15.0, 26.0), 2), 
            (numrange(26, 65.0), 3),
            (numrange(65, 175.0), 4),
            (numrange(175, 360.0), 5),
            (numrange(360, NULL), 6)
    )"""
JOIN_P = "LEFT JOIN puissance ON puissance_nominale::numeric <@ p_range "
PDC_ALL = f"""pointdecharge 
    LEFT JOIN station ON station.id = station_id 
    LEFT JOIN localisation ON localisation_id = localisation.id"""
STAT_ALL = "station LEFT JOIN localisation ON localisation_id = localisation.id "
ISIN_GEOM = 'ST_Within("coordonneesXY", geometry) '
CITY_COG = f"""
    x_city AS (SELECT geometry, code AS c_code, department_id, epci_id  FROM city),
    x_department AS (SELECT id as d_id, code AS d_code, region_id FROM department),
    x_epci AS (SELECT id as e_id, code AS e_code FROM epci),
    x_region AS (SELECT id as r_id, code AS r_code FROM region),
    city_cog AS (SELECT geometry, c_code, d_code, e_code, r_code from x_city LEFT JOIN x_department ON x_department.d_id = department_id LEFT JOIN x_epci ON x_epci.e_id = epci_id LEFT JOIN x_region ON region_id = x_region.r_id)"""
TABLE = {'00': 'national', '01': 'region', '02': 'department', '03': 'epci', '04': 'city'}
G_OVERHEAD = f"""QUERY,
    VAL,
    LEVEL,
    AREA"""
STAT_NB_PDC = f"""stat_nb_pdc AS (
    SELECT
      count(station_id) AS nb_pdc,
      localisation_id
    FROM
      pointdecharge
      LEFT JOIN station ON station.id = station_id
    GROUP BY
      station_id,
      localisation_id
)
"""
# URL_POP = 'https://unpkg.com/@etalab/decoupage-administratif@4.0.0/data/communes.json'
# POP = None 

def to_indicator(engine, indicator, simple=True, histo=False, format='pandas', histo_timest=None, json_orient='split',
                 table_name=None, table_option="replace", query_gen=False):
    """create data for an indicator
    
    Parameters
    ----------
    engine: sqlalchemy object
        Connector to postgreSQL database
    indicator: str 
        Indicator name (see indicator codification)
    simple: boolean, default False
        If False, additional columns are added
    histo: boolean, default False
        If True, timestamp additional column is added (with others additional columns)
    format: enum ('pandas', 'query', 'histo', 'json', 'table'), default 'pandas'
        Define the return format:
        - 'pandas'-> query result Dataframe
        - 'query'-> postgreSQL query String
        - 'json'-> json query result string
        - 'table' -> Dataframe (table creation confirmation with the number of lines created)
    json_orient: string, default 'split'
        Json structure (see 'orient' option for 'DataFrame.to_json').
    histo_timest: string (used if histo=True), default None
        Value of timestamp. If None the timestamp is the execution query timestamp.
    table_name: string (used if format='table'), default None
        Name of the table to create (format='table'). If None the name is the indicator name.
    table_option: string (used if format='table'), default 'replace'
        Option if table exists ('replace' or 'append')
    query_gen: boolean (default False)
        If True, the query is generic (with variables) else the query is specific (with values)

    Returns
    -------
    String or Dataframe
        see 'format' parameter
    """
    indic = indicator + '-00'
    simple = False if histo else simple
    query = getattr(create_query, 'query_' + indic.split('-')[0])(*indic.split('-')[1:], simple=simple, gen=query_gen)
    if histo:
        query = create_query.query_histo(query, timestamp=histo_timest)
    if format == 'query':
        return query
    with engine.connect() as conn:
        data_pd = pd.read_sql_query(query, conn)
    if format == 'pandas':
        return data_pd
    if format == 'json':
        return '{"' + indicator + '": ' + data_pd.to_json(index=False, orient=json_orient) + "}"
    if format == 'table':
        table_name = table_name if table_name else indicator
        return indic_to_table(data_pd, table_name, engine, table_option=table_option)

def indic_to_table(pd_df, table_name, engine, table_option="replace"):
    """ Load a DataFrame in a Table
    
    Parameters
    ----------
    engine: sqlalchemy object
        Connector to postgreSQL database
    pd_df: DataFrame 
        Data to load
    table_name: string
        Name of the table to create.
    table_option: string (used if format='table'), default 'replace'
        Option if table exists 'replace' or 'append'

    Returns
    -------
    Dataframe
        Table creation confirmation with the number of lines created.
    """
    pd_df.to_sql(table_name, engine, if_exists=table_option, index=False)
    return pd.read_sql_query('SELECT COUNT(*) AS count FROM "' + table_name + '"', engine)

def query_histo(query, timestamp=None):

    if timestamp:
        datation = "datation(timest) AS (VALUES ('" + timestamp + "'::timestamp)) "
    else:
        datation = "datation(timest) AS (VALUES (CURRENT_TIMESTAMP)) "

    return " WITH query AS (" + query + "), " + datation + " SELECT * FROM query, datation "

def init_param_txx(simple, gen, indic,  *param):
    '''parameters initialization for 'query_ixx' functions  '''
    
    perim, val, zone = (param + ('00', '00', '00'))[:3]
    perim = perim.rjust(2, '0')
    val = val.rjust(2, '0')
    zone = zone.rjust(2, '0')


    g_overhead = "" if simple else f"{G_OVERHEAD},"
    s_overhead = "" if simple else f"""'{indic}' AS QUERY,
    '{perim}' AS LEVEL,
    '{val}' AS VAL,
    '{zone}' AS AREA"""
    table_perim = "" if perim == '00' else f"{TABLE[perim]},"
    table_perim_code = "" if perim == '00' else f"{TABLE[perim]}.code"
    where_isin_perim = "" if perim == '00' else f"""WHERE
    {table_perim_code} = '{val}'
    AND ST_Within ("coordonneesXY", {TABLE[perim]}.geometry)"""
    
    if gen:
        s_overhead = "" if simple else f"""'{{indic}}' AS QUERY,
    '{{perim}}' AS LEVEL,
    '{{val}}' AS VAL,
    '{{zone}}' AS AREA"""
        table_perim = "" if perim == '00' else f"{{TABLE[perim]}},"
        table_perim_code = "" if perim == '00' else f"{{TABLE[perim]}}.code"
        where_isin_perim = "" if perim == '00' else f"""WHERE
    {table_perim_code} = '{{val}}'
    AND ST_Within ("coordonneesXY", {{TABLE[perim]}}.geometry)"""
        
    return (perim, table_perim_code, g_overhead, s_overhead, where_isin_perim, table_perim)

def query_t1(*param, simple=True, gen=False):
    '''Create SQL query for 't1' indicators (see parameters in module docstring)'''

    indic = 't1'
    (perim, table_perim_code, g_overhead, s_overhead, where_isin_perim, table_perim
     ) = init_param_txx(simple, gen, indic, *param)

    coma1 = "" if f"{table_perim_code}{s_overhead}" == "" else ","
    coma2 = "" if f"{table_perim_code}" == "" else ","
    coma3 = "" if f"{s_overhead}" == "" or f"{table_perim_code}" == "" else ","

    return f"""
WITH 
    {P_TAB}
SELECT
    count(id_pdc_itinerance) AS nb_pdc,
    p_range{coma1}
    {table_perim_code}{coma3}
    {s_overhead}
FROM
    {table_perim}
    {PDC_ALL}
    {JOIN_P}
{where_isin_perim}
GROUP BY
    {g_overhead}
    p_range{coma2}
    {table_perim_code}
ORDER BY
    nb_pdc DESC"""

def query_t2(*param, simple=True, gen=False):
    '''Create SQL query for 't2' indicators (see parameters in module docstring)'''
    
    indic = 't2'
    (perim, table_perim_code, g_overhead, s_overhead, where_isin_perim, table_perim
     ) = init_param_txx(simple, gen, indic, *param)

    code = "" if perim == '00' else "code"
    coma1 = "" if f"{code}{s_overhead}" == "" else ","
    # coma3 = "" if s_overhead == "" else ","
    coma3 = "" if f"{s_overhead}" == "" or f"{code}" == "" else ","

    return f"""WITH 
    t1 AS (
        {query_t1(*param, simple=simple, gen=gen)}
    )
SELECT
    nb_pdc / (
        SELECT 
            sum(nb_pdc) 
        FROM 
            t1
    ) * 100 AS pct_nb_pdc,
    p_range{coma1}
    {code}{coma3}
    {s_overhead}
FROM 
    t1"""

def query_t3(*param, simple=True, gen=False):
    '''Create SQL query for 't3' indicators (see parameters in module docstring)'''

    indic = 't3'
    (perim, table_perim_code, g_overhead, s_overhead, where_isin_perim, table_perim
     ) = init_param_txx(simple, gen, indic, *param)

    coma1 = "" if f"{table_perim_code}{s_overhead}" == "" else ","
    coma2 = "" if f"{table_perim_code}" == "" else ","
    coma3 = "" if f"{s_overhead}" == "" or f"{table_perim_code}" == "" else ","

    return f"""
WITH 
    {STAT_NB_PDC}
SELECT
    count(nb_pdc) AS nb_stations,
    nb_pdc{coma1}
    {table_perim_code}{coma3}
    {s_overhead}
FROM
    {table_perim}
    stat_nb_pdc
    LEFT JOIN localisation ON localisation_id = localisation.id
{where_isin_perim}
GROUP BY
    {g_overhead}
    nb_pdc{coma2}
    {table_perim_code}
ORDER BY
    nb_stations DESC"""

'''
SELECT
    count(nbre_pdc) AS nb_stations,
    nbre_pdc{coma1}
    {table_perim_code}{coma3}
    {s_overhead}
FROM
    {STAT_ALL}
    {COG_ALL}
{where_isin_perim}
GROUP BY
    {g_overhead}
    nbre_pdc{coma2}
    {table_perim_code}
ORDER BY
    nb_stations DESC'''

def query_t4(*param, simple=True, gen=False):
    '''Create SQL query for 't4' indicators (see parameters in module docstring)'''
    
    indic = 't4'
    (perim, table_perim_code, g_overhead, s_overhead, where_isin_perim, table_perim
     ) = init_param_txx(simple, gen, indic, *param)
    code = "" if perim == '00' else "code"
    coma1 = "" if f"{code}{s_overhead}" == "" else ","
    coma3 = "" if f"{s_overhead}" == "" or f"{code}" == "" else ","

    return f"""WITH 
    t3 AS (
        {query_t3(*param, simple=simple, gen=gen)}
    )
SELECT
    nb_stations / (
        SELECT 
            sum(nb_stations) 
        FROM 
            t3
    ) * 100 AS pct_nb_stations,
    nb_pdc{coma1}
    {code}{coma3}
    {s_overhead}
FROM 
    t3"""

def query_t5(*param, simple=True, gen=False):
    '''Create SQL query for 't5' indicators (see parameters in module docstring)'''
    
    indic = 't5'
    (perim, table_perim_code, g_overhead, s_overhead, where_isin_perim, table_perim
     ) = init_param_txx(simple, gen, indic, *param)

    coma1 = "" if f"{table_perim_code}{s_overhead}" == "" else ","
    coma2 = "" if f"{table_perim_code}" == "" else ","
    coma3 = "" if f"{s_overhead}" == "" or f"{table_perim_code}" == "" else ","

    return f"""
SELECT
    count(id_station_itinerance) AS nb_stations,
    implantation_station{coma1}
    {table_perim_code}{coma3}
    {s_overhead}
FROM
    {table_perim}
    {STAT_ALL}
{where_isin_perim}
GROUP BY
    {g_overhead}
    implantation_station{coma2}
    {table_perim_code}
ORDER BY
    nb_stations DESC"""

def query_t6(*param, simple=True, gen=False):
    '''Create SQL query for 't6' indicators (see parameters in module docstring)'''

    indic = 't6'
    (perim, table_perim_code, g_overhead, s_overhead, where_isin_perim, table_perim
     ) = init_param_txx(simple, gen, indic, *param)
    code = "" if perim == '00' else "code"
    coma1 = "" if f"{code}{s_overhead}" == "" else ","
    coma3 = "" if f"{s_overhead}" == "" or f"{code}" == "" else ","

    return f"""WITH 
    t5 AS (
        {query_t5(*param, simple=simple, gen=gen)}
    )
SELECT
    nb_stations / (
        SELECT 
            sum(nb_stations) 
        FROM 
            t5
    ) * 100 AS pct_nb_stations,
    implantation_station{coma1}
    {code}{coma3}
    {s_overhead}
FROM 
    t5"""

def init_param_ixx(simple, gen, indic,  *param):
    '''parameters initialization for 'query_ixx' functions  '''
    
    perim, val, zone = (param + ('00', '00', '00'))[:3]
    perim = perim.rjust(2, '0')
    val = val.rjust(2, '0')
    zone = zone.rjust(2, '0')

    zone = perim if zone == '00' else zone

    coma = "" if simple else ","
    g_overhead = "" if simple else f"{G_OVERHEAD},"
    s_overhead = "" if simple else f"""'{indic}' AS QUERY,
    '{perim}' AS LEVEL,
    '{val}' AS VAL,
    '{zone}' AS AREA"""
    table_perim = "" if perim == zone or perim == '00' else f"{TABLE[perim]},"
    where_isin_perim = "" if perim == '00' else f"""WHERE
    {TABLE[perim]}.code = '{val}'
    AND ST_Within ("coordonneesXY", {TABLE[perim]}.geometry)"""
    table_zone = f"{TABLE[zone]}"
    
    if gen:
        s_overhead = "" if simple else f"""'{{indic}}' AS QUERY,
    '{{perim}}' AS LEVEL,
    '{{val}}' AS VAL,
    '{{zone}}' AS AREA"""
        table_perim = "" if perim == zone or perim == '00' else f"{{TABLE[perim]}},"
        where_isin_perim = "" if perim == '00' else f"""WHERE
    {{TABLE[perim]}}.code = '{{val}}'
    AND ST_Within ("coordonneesXY", {{TABLE[perim]}}.geometry)"""
        table_zone = f"{{TABLE[zone]}}"

    return (perim, val, zone, coma, g_overhead, s_overhead, where_isin_perim, table_perim, table_zone)

def query_i1(*param, simple=True, gen=False):
    '''Create SQL query for 'i1' indicators (see parameters in module docstring)'''

    indic = 'i1'
    (perim, val, zone, coma, g_overhead, s_overhead, where_isin_perim, table_perim, table_zone
     ) = init_param_ixx(simple, gen, indic, *param)

    if perim == zone == '00':
        return f"""
SELECT
    count(id_pdc_itinerance) AS nb_pdc{coma}
    {s_overhead}
FROM
    pointdecharge"""

    return f"""
SELECT
    count(id_pdc_itinerance) AS nb_pdc,
    {table_zone}.code{coma}
    {s_overhead}
FROM
    {table_perim}
    {PDC_ALL}
    LEFT JOIN {table_zone} ON ST_Within ("coordonneesXY", {table_zone}.geometry)
{where_isin_perim}
GROUP BY
    {g_overhead}
    {table_zone}.code
ORDER BY
    nb_pdc DESC"""

def query_i4(*param, simple=True, gen=False):
    '''Create SQL query for 'i4' indicators (see parameters in module docstring)'''

    indic = 'i4'
    (perim, val, zone, coma, g_overhead, s_overhead, where_isin_perim, table_perim, table_zone
     ) = init_param_ixx(simple, gen, indic, *param)

    if perim == zone == '00':
        return f"""
SELECT
    count(id_station_itinerance) AS nb_stat{coma}
    {s_overhead}
FROM
    station"""

    return f"""
SELECT
    count(id_station_itinerance) AS nb_stat,
    {table_zone}.code{coma}
    {s_overhead}
FROM
    {table_perim}
    {STAT_ALL}
    LEFT JOIN {table_zone} ON ST_Within ("coordonneesXY", {table_zone}.geometry)
{where_isin_perim}
GROUP BY
    {g_overhead}
    {table_zone}.code
ORDER BY
    nb_stat DESC"""

def query_i7(*param, simple=True, gen=False):
    '''Create SQL query for 'i7' indicators (see parameters in module docstring)'''

    indic = 'i7'
    (perim, val, zone, coma, g_overhead, s_overhead, where_isin_perim, table_perim, table_zone
     ) = init_param_ixx(simple, gen, indic, *param)

    if perim == zone == '00':
        return f"""
SELECT
    sum(puissance_nominale) AS p_nom{coma}
    {s_overhead}
FROM
    pointdecharge"""

    return f"""
SELECT
    sum(puissance_nominale) AS p_nom,
    {table_zone}.code{coma}
    {s_overhead}
FROM
    {table_perim}
    {PDC_ALL}
    LEFT JOIN {table_zone} ON ST_Within ("coordonneesXY", {table_zone}.geometry)
{where_isin_perim}
GROUP BY
    {g_overhead}
    {table_zone}.code
ORDER BY
    p_nom DESC"""

"""def create_table_pop(engine):
    '''create temporay table with population'''
    pop = pd.read_json(URL_POP).loc[:,['code', 'population']]
    pop.rename(columns={'code': 'p_code'}, inplace=True)
    indic_to_table(pop, 'tmp_pop', engine, table_option="replace")

def query_i2(*param, simple=True, gen=False):
    '''Create SQL query for 't2' indicators (see parameters in module docstring)'''

    perim, val, zone = (param + ('00', '00', '00'))[:3]
    perim = perim.rjust(2, '0')
    val = val.rjust(2, '0')
    zone = zone.rjust(2, '0')
"""
'''
    pdc_cog_pop = f"""
        {CITY_COG},
        pdc_all AS (SELECT * from {PDC_ALL}),
        pdc_cog_pop AS (SELECT * from pdc_all LEFT JOIN city_cog ON {ISIN_GEOM } LEFT JOIN temp_pop ON c_code)
        """

    FIELD = {'00': 'all_data', '01': 'r_code', '02': 'd_code', '03': 'e_code', '04': 'c_code'}
    zone = perim if zone == '00' else zone

    return f"""
    WITH {pdc_cog_pop}, 
         perimeter(level, all_data) AS (VALUES ('{zone}', '00')),
         tot_pop AS (
            SELECT count(id_pdc_itinerance) AS nb_pdc, sum(population) AS nb_pop, level, {FIELD[zone]} AS x_code
            FROM perimeter, pdc_cog_pop
            WHERE {FIELD[perim]} = '{val}'
            GROUP BY level, x_code ORDER BY nb_pdc DESC)
    SELECT nb_pdc / nb_pop * 100000 AS ratio_nb_pdc_per_pop, p_cat, p_range, level, code
    FROM tot_pop"""
'''
