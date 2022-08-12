from fastapi import FastAPI, Query
import requests
import os
from dotenv import load_dotenv
import urllib.parse

from lib.thredds import get_average_temperature, get_yearly_precipitation, get_average_humidity, get_extreme_temperatures

load_dotenv()

description = """
Downscaled climate projections from NASA's Global Daily Downscaled Projections (GDDP) CMIP6 dataset. 
Uses the GISS-E2-1-G model with the SSP2 4.5 emissions pathway.

Note that these values are projections using a single climate model, 
and are more useful for understanding general trends than as specific predications. 
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
    if coords == "Location not found":
        return {
            "message": "Location not found. Either specify more of the address, or try a different address."
        }
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


@app.get('/extremes')
def extreme_temperatures(
        address: str = Query(..., description="Street address. Example: `1600 Pennsylvania Ave NW, Washington DC`"),
        years: str = Query(..., description="Comma-separated list of years. Example: `2020,2060`"),
        var_name: str = Query('tasmax', description="Either `tasmax` for maximum temperature or `tasmin` for minimum "
                                               "temperature. Default is `tasmax`")
):
    coords = get_address_lat_lng(address)
    if coords == "Location not found":
        return {
            "message": "Location not found. Either specify more of the address, or try a different address."
        }
    if var_name != 'tasmax' and var_name != 'tasmin':
        return {
            "message": "Invalid `var_name` value. Please specify either `tasmax` or `tasmin`. "
        }
    years = [int(year) for year in years.split(',')]
    result = get_extreme_temperatures(coords, years, var_name)

    return {
        "name": "Maximum temperature" if var_name == 'tasmax' else 'Minimum temperature',
        "variable": var_name,
        "unit": "°C",
        "data": result
    }


@app.get("/")
def api_status():
    return {"Status": "Operational"}
