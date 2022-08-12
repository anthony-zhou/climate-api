from fastapi import FastAPI, Query
import requests
import os
from dotenv import load_dotenv
import urllib.parse

from lib.thredds import get_average_temperature, get_yearly_precipitation, get_average_humidity

load_dotenv()

description = """
Downscaled climate projections from NASA's Global Daily Downscaled Projections (GDDP) CMIP6 dataset. 
Uses the GISS-E2-1-G model with the SSP2 4.5 emissions pathway.
"""

app = FastAPI(title="Climate API", description="")


# 1600%20Pennsylvania%20Ave%20NW%2C%20Washington%20DC
# address = '1600 Pennsylvania Ave NW, Washington DC'

def get_address_lat_lng(address):
    maps_api_key = os.environ.get('MAPS_API_KEY')
    params = {'key': maps_api_key, 'limit': 1}
    address = urllib.parse.quote(address)
    response = requests.get(f'https://api.tomtom.com/search/2/geocode/{address}.json', params=params)
    results = response.json()['results']
    if len(results) == 0:
        return "Location not found"
    location = results[0]['position']
    return location['lat'], location['lon']


@app.get('/average_temp')
def average_yearly_temperature(
        address: str = Query(..., description="Street address. Example: `1600 Pennsylvania Ave NW, Washington DC`"),
        years: str = Query(..., description="Comma-separated list of years. Example: `2020,2060`")
):
    coords = get_address_lat_lng(address)
    years = [int(year) for year in years.split(',')]
    result = get_average_temperature(coords, years)

    return {
        "name": "Average yearly surface temperature",
        "variable": "tas",
        "unit": "°C",
        "data": result
    }


@app.get('/total_precipitation')
def total_yearly_precipitation(
        address: str = Query(..., description="Street address. Example: `1600 Pennsylvania Ave NW, Washington DC`"),
        years: str = Query(..., description="Comma-separated list of years. Example: `2020,2060`")
):
    coords = get_address_lat_lng(address)
    if coords == "Location not found":
        return {
            "message": "Location not found. Either specify more of the address, or try a different address."
        }
    years = [int(year) for year in years.split(',')]
    result = get_yearly_precipitation(coords, years)

    return {
        "name": "Total yearly precipitation",
        "variable": "pr",
        "unit": "inches",
        "data": result
    }


@app.get('/average_humidity')
def average_yearly_humidity(
        address: str = Query(..., description="Street address. Example: `1600 Pennsylvania Ave NW, Washington DC`"),
        years: str = Query(..., description="Comma-separated list of years. Example: `2020,2060`"),
        units: str = Query('relative', description="Either `specific` or `relative` humidity. Default is `relative`")
):
    coords = get_address_lat_lng(address)
    if coords == "Location not found":
        return {
            "message": "Location not found. Either specify more of the address, or try a different address."
        }
    var_name = "hurs" if units == 'relative' else 'huss'
    if units != 'relative' and units != 'specific':
        return {
            "message": "Invalid `units` value. Please specify either `relative` or `specific`. "
        }
    years = [int(year) for year in years.split(',')]
    result = get_average_humidity(coords, years, var_name)

    return {
        "name": "Average " + units + " humidity",
        "variable": var_name,
        "unit": "%" if units == 'relative' else 'kg / kg',
        "data": result
    }


@app.get("/")
def api_status():
    return {"Status": "Operational"}
