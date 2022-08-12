from time import time

import numpy as np
import xml.etree.ElementTree as ElementTree
from netCDF4 import Dataset


def _fetch_dataset_urls(var_name):
    # Parse dataset URLs from the XML file
    dataset_urls = []
    total_storage_req = 0.0
    tree = ElementTree.parse(f'./lib/giss_catalogs/{var_name}_catalog.xml')
    root = tree.getroot()

    xmlns = "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0"
    ns = {
        "ns": xmlns
    }
    for item in root.findall('ns:dataset/', ns):
        if 'dataset' in item.tag:
            dataset_url = 'https://ds.nccs.nasa.gov/thredds2/dodsC/' + item.attrib['urlPath']
            dataset_urls.append(dataset_url)

            data_size = item.find('ns:dataSize', ns)
            total_storage_req += float(data_size.text)

    return dataset_urls


def _load_datasets(years, var_name):
    """
    Load NetCDF Dataset objects for each year in `years`.
    """
    def get_year(u):
        return int(u[-7:-3])

    def years_includes(u):
        return get_year(u) in years

    dataset_urls = _fetch_dataset_urls(var_name)
    datasets = {get_year(url): Dataset(url) for url in dataset_urls if years_includes(url)}
    return datasets


def get_average_temperature(coords: tuple, years: list[int], window_size=40):
    """
    Get downscaled surface temperature projections for the given years.
    Arguments:
        coords: a latitude, longitude pair.
        years: a list of years to find values for.
        window_size: the number of days to skip over when averaging
            (e.g., for window_size = 60, we would use day 60, 120, 180, etc. when averaging)
    Returns:
        A dictionary with years as keys and average values in Celsius as values.
    """
    lat = coords[0]
    lon = coords[1] if coords[1] > 0 else 360 + coords[1]
    print(lat, lon)

    datasets = _load_datasets(years, var_name='tas')

    result = {}

    for year, data in datasets.items():
        # This is a more general form of finding closest coordinates.
        jj = np.argmin((data['lat'][:] - lat) ** 2)
        ii = np.argmin((data['lon'][:] - lon) ** 2)

        # Here's a slightly faster version assuming 0.25 degree spacing.
        # It sacrifices generality for only ~1.2x speed improvement,
        # which is pretty insignificant in the grand scheme of things.
        # jj = round((lat - data['lat'][0]) * 4)
        # ii = round((lon - data['lon'][0]) * 4)
        print(jj)
        print(ii)

        # Note: accessing data using ::window_size is much faster than using a for loop with range().
        time_series = data['tas'][::window_size, jj, ii]
        avg = np.sum(time_series) / len(time_series) - 273.15
        result[year] = avg

    for year in years:
        if year not in result:
            result[year] = "Not found"

    return result


def get_yearly_precipitation(coords: tuple, years: list[int], window_size=2):
    lat = coords[0]
    lon = coords[1] if coords[1] > 0 else 360 + coords[1]
    datasets = _load_datasets(years, var_name='pr')

    result = {}
    for year, data in datasets.items():
        jj = np.argmin((data['lat'][:] - lat) ** 2)
        ii = np.argmin((data['lon'][:] - lon) ** 2)

        # Sample one out of every window_size precipitation rates.
        time_series = data['pr'][::window_size, jj, ii]

        # Convert precipitation flux to inches
        result[year] = np.sum(time_series).item() * window_size * 86400 / 25.4

    for year in years:
        if year not in result:
            result[year] = "Not found"

    return result
