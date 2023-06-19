import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
pd.set_option('display.max_rows',100)
np.random.seed(42)

areas = {
    'Africa': 'CAF',
    'China': 'CHN',
    'India': 'IND',
    'Asia (excl. China and India)': 'THA',
    'Europe': 'AUT',
    'Middle East (GCP)': 'IRN',
    'Oceania': 'AUS',
    'South America': 'BOL',
    'Central America (GCP)': 'NIC',
    'North America': 'USA'
}
x = 200
# Get the data, remove old records
df_co2 = pd.read_csv("data/co2-data.csv")
df_ISO_CODES = pd.read_csv("data/iso_codes.csv")
df_co2 = df_co2[df_co2['year'] >= 1900]


# Coutry historica
df_co2_countries = df_co2.dropna(subset=['iso_code'])[['year', 'co2', 'country', 'iso_code']]
# World historical
df_co2_global = df_co2_countries.groupby('year')['co2'].aggregate('sum').reset_index()

##### Getting the latest (2021)
df_co2_2021 = df_co2[df_co2['year'] == 2021]

# Country latest
df_co2_latest_by_country = df_co2_2021.dropna(subset=['iso_code', 'co2'])[['country', 'iso_code', 'co2', 'co2_per_capita', 'year']]
df_co2_latest_by_country['x'] = np.random.randint(0,20, size=len(df_co2_latest_by_country))
df_co2_latest_by_country['y'] = np.random.randint(0,20, size=len(df_co2_latest_by_country))
df_co2_latest_by_country = df_co2_latest_by_country.sort_values(by=['co2'])
df_co2_latest_by_country['colour'] = range(1, 1+len(df_co2_latest_by_country) * x, x)

df_co2_latest_by_country = df_co2_latest_by_country.merge(df_ISO_CODES, how='left', left_on=['iso_code'], right_on=['alpha-3'])

df_co2_latest_by_country['isAus'] = df_co2_latest_by_country['iso_code'] == 'AUS'

# World latest
df_co2_latest_global = df_co2_2021[df_co2_2021['country'].isin(['World'])][['country', 'co2', 'co2_per_capita', 'year']]
df_co2_latest_global['iso_code'] = 'CAF'
df_co2_latest_global['colour'] = range(1, 1+len(df_co2_latest_global) * x, x)
df_co2_latest_global['co2'] = df_co2_latest_global['co2'] / 1000

# Area latest
df_co2_latest_by_area = df_co2_2021[df_co2_2021['country'].isin(list(areas.keys()))][['country', 'co2', 'co2_per_capita', 'year']]
df_co2_latest_by_area['iso_code'] = df_co2_latest_by_area['country'].map(areas)
df_co2_latest_by_area = df_co2_latest_by_area.sort_values(by=['co2'])

df_co2_latest_by_area['colour'] = range(1, 1+len(df_co2_latest_by_area) * x, x)


# By sector
df_co2_by_sector = pd.read_csv("data/co2-by-sector-2016.csv")

# Mining specific
mining = [
    "Iron & Steel",
    "Non-ferous metals",
    "Machinery",
    "Energy in industry"
]
df_co2_by_sector['mining'] = df_co2_by_sector[['Subsector', 'Category', 'Sector']].isin(mining).any(axis=1)


# Sanity check
# print(df_ISO_CODES)
# print(df_co2_latest_by_country)
