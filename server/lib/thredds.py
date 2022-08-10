import numpy as np
import xml.etree.ElementTree as ElementTree
from netCDF4 import Dataset


def _fetch_dataset_urls():
    # Parse dataset URLs from the XML file
    dataset_urls = []
    total_storage_req = 0.0
    tree = ElementTree.parse('./lib/giss_catalog.xml')
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

    print(f"Found {len(dataset_urls)} dataset URLs. Total storage required: {total_storage_req} MB.")
    return dataset_urls


def _load_datasets(years):
    """
    Load NetCDF Dataset objects for each year in `years`.
    """
    def get_year(u):
        return int(u[-7:-3])

    def years_includes(u):
        return get_year(u) in years

    dataset_urls = _fetch_dataset_urls()
    datasets = {get_year(url): Dataset(url) for url in dataset_urls if years_includes(url)}
    return datasets


def get_average_temperature(coords: tuple, years: list[int], window_size=60):
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
    datasets = _load_datasets(years)
    result = {}
    for year, data in datasets.items():
        jj = np.argmin((data['lat'][:] - lat) ** 2)
        ii = np.argmin((data['lon'][:] - lon) ** 2)

        total = 0.0
        sample_days = range(0, 365, window_size)
        for day in sample_days:
            total += data['tas'][day, jj, ii]
        result[year] = total / len(sample_days) - 273.15

    for year in years:
        if year not in result:
            result[year] = "Not found"

    return result
