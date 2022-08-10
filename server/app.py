import statistics
from fastapi import FastAPI
import regionmask
import geopandas
from shapely import geometry
import requests

app = FastAPI()


def get_median(climate_data, year):
    items = []
    for item in climate_data:
        if item['year'] == year:
            items.append(item['value'])
    return statistics.median(items)


# address = '1600 Pennsylvania Ave NW, Washington DC'

def get_address_region(address):
    query = {'access_key': '240b12f8fe3aa36cca02b35684d69055', 'query': address}
    response = requests.get('http://api.positionstack.com/v1/forward', params=query)
    data = response.json()['data']
    location = data[0]

    sample_point = geometry.Point(location['longitude'], location['latitude'])
    dataframe = regionmask.defined_regions.ar6.all.to_geodataframe()
    for i, row in dataframe.iterrows():
        if row['geometry'].contains(sample_point):
            return i, location

def get_projections(region_index, year_1, year_2, location):
    query = {
        'region': 'AR6',
        'ids': region_index,
        'project': 'CMIP6',
        # 'scenario': 'ssp585',
        'variable': 'tx35',
        'valueType': 'VALUE',
        'temporalFilter': 'year',
        'period': 2,
        # 'baseline': 'preIndustrial',
        'landMask': 'false',
        'mountainMask': 'false'
    }
    result = {'year_1': {'year': year_1}, 'year_2': {'year': year_2}, 'location': location}
    for scenario in ['ssp245', 'ssp370', 'ssp585']:
        scenario_query = query | {'scenario': scenario}
        response = requests.get('https://interactive-atlas.ipcc.ch/temporal/serie', params=scenario_query)
        data = response.json()
        result['year_1'][scenario] = get_median(data, year_1)
        result['year_2'][scenario] = get_median(data, year_2)
        print(f"Mean days above 35°C/95°F in {year_1}: {get_median(data, year_1)}")
        print(f"Mean days above 35°C/95°F in {year_2}: {get_median(data, year_2)}")
    return result


@app.get('/data')
def get_climate_data(address: str):
    region_index, location = get_address_region(address)
    result = get_projections(region_index, 2022, 2040, location)

    return result






