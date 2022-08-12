# Climate API + Heat Map

Enter a street address to see climate projections for that area.

Variables included in the API:
- Average yearly temperature
- Total yearly precipitation
- Relative humidity
- Specific humidity
- Maximum yearly temperature
- Minimum yearly temperature

## Why it matters

Typically, climate models predict macro trends for our climate, at a continent or region-scale resolution. 
From a local perspective, these models are not useful. As a result, scientists have developed downscaled models, which
take these global climate projections and compute values at a local (up to 0.25 deg by 0.25 deg) resolution. 

Downscaled climate data has only recently become good enough to start informing regional climate adaptation strategies. 
However, downscaled climate datasets are hard to access. They typically require you to download terabytes of data hidden behind outdated 
fileservers. 

The goal of this project is to develop an easy-to-use API for accessing downscaled climate projections. This API serves 
as a layer of abstraction over downscaled datasets, making it easy for developers to access data and derive actionable insights. 

A secondary goal is to create a web app demonstrating the usage of this API.

## Demo
- The Climate API is deployed at https://2nnrmg.deta.dev/. For docs, see https://2nnrmg.deta.dev/docs.

Note: the web app interface is not currently deployed because the API spec is still changing. 

## Installation

To install python dependencies, set up a virtual environment in `server` and run `pip install -r requirements.txt`. 

The Jupyter notebooks contain a set of dependencies separate from the main API, so you should set up a second virtual 
environment if you want to run those. 

## How it works

The Climate API is built using Python with FastAPI and deployed on Deta. Climate data comes from the NASA Earth Exchange
Global Daily Downscaled Projections dataset, using the CMIP6 scenarios.

## File Structure

- The `client` folder contains code for the web app demo (incomplete)
- The `server` folder contains code for serving the climate API:
  - `main.py` serves the main API layer
  - `lib` contains modules for business logic, primarily loading and processing the data. 
  - `notebooks` contains some experiments with downloading and processing climate data.

## Next Steps

Currently, the API is very slow for some types of requests. This is because we are computing yearly statistics from 
daily projections. We could speed up the API greatly by computing yearly statistics (averages/sums/extremes) ahead of 
time and storing them in a separate database.

Perhaps more importantly, we would like to serve more than just the basic variables listed above. Implementing the 
`xclim` (https://github.com/Ouranosinc/xclim) library for this API will let us estimate other important variables, like 
frequency of heat waves, intensity of cold spells, and drought codes.
