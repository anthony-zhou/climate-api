import statistics
from fastapi import FastAPI
import requests
from time import time
import os
from dotenv import load_dotenv

from lib.thredds import get_average_temperature

load_dotenv()

app = FastAPI(title="Climate API", description="Downscaled climate projections from NASA's Global Daily Downscaled "
                                               "Projections (GDDP) dataset. Uses the GISS-E2-1-G model with the SSP2 "
                                               "4.5 emissions pathway.")

def get_median(climate_data, year):
    items = []
    for item in climate_data:
        if item['year'] == year:
            items.append(item['value'])
    return statistics.median(items)


# 1600%20Pennsylvania%20Ave%20NW%2C%20Washington%20DC
# address = '1600 Pennsylvania Ave NW, Washington DC'

def get_address_lat_lng(address):
    maps_api_key = os.environ.get('MAPS_API_KEY')
    params = {'key': maps_api_key, 'address': address}
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
    location = response.json()['results'][0]['geometry']['location']
    return location['lat'], location['lng']
#
#     sample_point = geometry.Point(location['longitude'], location['latitude'])
#     dataframe = regionmask.defined_regions.ar6.all.to_geodataframe()
#     for i, row in dataframe.iterrows():
#         if row['geometry'].contains(sample_point):
#             return i, location


# def get_projections(region_index, year_1, year_2, location):
#     query = {
#         'region': 'AR6',
#         'ids': region_index,
#         'project': 'CMIP6',
#         # 'scenario': 'ssp585',
#         'variable': 'tx35',
#         'valueType': 'VALUE',
#         'temporalFilter': 'year',
#         'period': 2,
#         # 'baseline': 'preIndustrial',
#         'landMask': 'false',
#         'mountainMask': 'false'
#     }
#     result = {'year_1': {'year': year_1}, 'year_2': {'year': year_2}, 'location': location}
#     for scenario in ['ssp245', 'ssp370', 'ssp585']:
#         scenario_query = query | {'scenario': scenario}
#         response = requests.get('https://interactive-atlas.ipcc.ch/temporal/serie', params=scenario_query)
#         data = response.json()
#         result['year_1'][scenario] = get_median(data, year_1)
#         result['year_2'][scenario] = get_median(data, year_2)
#         print(f"Mean days above 35°C/95°F in {year_1}: {get_median(data, year_1)}")
#         print(f"Mean days above 35°C/95°F in {year_2}: {get_median(data, year_2)}")
#     return result


@app.get('/average_temp')
def get_climate_data(address: str, years: str):
    coords = get_address_lat_lng(address)
    years = [int(year) for year in years.split(',')]
    result = get_average_temperature(coords, years)

    return {
        "variable": "tas",
        "unit": "°C",
        "data": result
    }


@app.get("/")
def read_root():
    return {"Hello": "World"}



