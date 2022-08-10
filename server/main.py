from fastapi import FastAPI, Query
import requests
import os
from dotenv import load_dotenv

from lib.thredds import get_average_temperature

load_dotenv()

app = FastAPI(title="Climate API", description="Downscaled climate projections from NASA's Global Daily Downscaled "
                                               "Projections (GDDP) dataset. Uses the GISS-E2-1-G model with the SSP2 "
                                               "4.5 emissions pathway.")


# 1600%20Pennsylvania%20Ave%20NW%2C%20Washington%20DC
# address = '1600 Pennsylvania Ave NW, Washington DC'

def get_address_lat_lng(address):
    maps_api_key = os.environ.get('MAPS_API_KEY')
    params = {'key': maps_api_key, 'address': address}
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=params)
    location = response.json()['results'][0]['geometry']['location']
    return location['lat'], location['lng']


@app.get('/average_temp')
def average_yearly_temperature(
        address: str = Query(..., description="Street address. Example: `1600 Pennsylvania Ave NW, Washington DC`"),
        years: str = Query(..., description="Comma-separated list of years. Example: `2020,2060`")
):
    coords = get_address_lat_lng(address)
    years = [int(year) for year in years.split(',')]
    result = get_average_temperature(coords, years)

    return {
        "variable": "tas",
        "unit": "°C",
        "data": result
    }


@app.get("/")
def api_status():
    return {"Status": "Operational"}



