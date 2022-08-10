from fastapi import FastAPI
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



