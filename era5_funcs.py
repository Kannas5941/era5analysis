import shutil
import cdsapi
import os
import xarray as xr
import numpy as np
import pandas as pd
import platform
from datetime import datetime
import matplotlib.pyplot as plt


# Downloading ERA5 data
def download_ERA5(initial_date, final_date, extent_coords, frequency, analysis):
    """Function to download ERA5 data from the Climate Change Service (CDS) API. 
    The default product is set as "reanalysis-era5-single-levels", 
    however it can be changed to others by checking the datasets available 
    on the CDS web: https://cds.climate.copernicus.eu/cdsapp#!/search?type=dataset .

    Args:
        initial_date (str): Initial date of the ERA5 data in the format: "YYYY-mm-dd"
        final_date (str): Final date of the ERA5 data in the format: "YYYY-mm-dd"
        extent_coords (list): Coordiantes to extract the data. 
                            If analysis="time_series" use: [LAT, LON]. 
                            If analysis="spatial" : [LAT_NORTH, LON_WEST, LAT_SOUTH, LON_EAST].

        frequency (str): This is the frequency in which the data is sampled. Only two 
                            options are: "hourly" and "monthly".
        analysis (str): This is the type of analysis to be performed, which can be 
                        "spatial" for maps or "time_series" for time series.
    """
    # This sets the api key in the home directory to be able to download the data
    file_path = os.path.realpath(__file__)  # script full name
    current_dir = os.path.dirname(file_path)  # script directory
    os.chdir(current_dir)
    apikey = '/.cdsapirc'

    if platform.system() == "Windows":
        home = os.environ["HomePath"]
    # elif platform.system() in ['Darwin', 'Linux']
    elif platform.system() == "Darwin":
        home = os.environ["HOME"]
    elif platform.system() == "Linux":
        home = os.environ["HOME"]

    shutil.copy(
        current_dir + '/../docs' + apikey, home + apikey
    )  # Copying the API key in the home directory.

    # Defining the data product
    if frequency == "hourly":
        product = "reanalysis-era5-single-levels"
        if (
            abs(
                (
                    datetime.strptime(final_date, "%Y-%m-%d")
                    - datetime.strptime(initial_date, "%Y-%m-%d")
                ).days
            )
            > 365
        ):
            print(
                'WARNING: This download might take a long time to be completed, for long-term \
                    analysis consider using monthly data: frequency = "monthly"'

            )
    elif frequency == "monthly":
        product = "reanalysis-era5-single-levels-monthly-means"

    if analysis == "time_series":
        if len(extent_coords) != 2:
            raise ValueError(
                "For time series analysis only input one latitude and one longitude: \
                    extent_coords = [LAT, LON]"
            )
        extent_coords = [
            extent_coords[0],
            extent_coords[1],
            extent_coords[0],
            extent_coords[1],
        ]
    elif analysis == "spatial":
        if len(extent_coords) != 4:
            raise ValueError(
                "For spatial analysis four inputs are required: \
                     extent_coords = [LAT1, LON1, LAT2, LON2]"
            )

    tight_coords = (
        str(extent_coords)
        .replace("[", "")
        .replace("]", "")
        .replace(",", "")
        .replace(" ", "")
    )  # To format the outputfile

    # Setting the request
    c = cdsapi.Client()
    c.retrieve(
        "{}".format(product),
        {
            "product_type": "reanalysis",
            "format": "netcdf",
            "variable": [
                "100m_u_component_of_wind",
                "100m_v_component_of_wind",
                "10m_u_component_of_wind",
                "10m_v_component_of_wind",
            ],
            "date": "{}/{}".format(initial_date, final_date),
            "area": extent_coords,
        },
        "{}-{}-{}-{}.nc".format(
            product,
            initial_date.replace("-", ""),
            final_date.replace("-", ""),
            tight_coords,
        ),
    )


# Processing ERA5 data
def processing_ERA5(file, analysis):
    """Function to preprocess ERA5 data, calculate the wind speed module [m/s] and
    the wind direction [degrees], and depending on the type of analysis, return \ 
    a xarray dataset or a pandas dataframe.

    Args:
        file (str): Full file name: path+filename.
        analysis (str): Type of analysis to perform: "spatial" retrieves a 3D dataset \
             (time, lat, lon). "time_series" retrieves a dataframe with \
             columns (time, ws, wd).


    Returns:
        (object): Returns a dataset or dataframe depending what kind of analysis
                 is being performed.
    """
    file_path = os.path.realpath(__file__)  # script full name
    current_dir = os.path.dirname(file_path)  # script directory
    os.chdir(current_dir)
    
    ds = xr.open_dataset(file)
    ds["WS10m"] = np.sqrt(ds.u10 ** 2 + ds.v10 ** 2)
    ds["WS100m"] = np.sqrt(ds.u100 ** 2 + ds.v100 ** 2)

    wdrad_10m = np.rad2deg(np.arctan2(
        ds.v10 / ds["WS10m"], ds.u10 / ds["WS10m"]))
    ds["WD10m"] = np.mod((270.0 - wdrad_10m), 360.0)
    wdrad_100m = np.rad2deg(np.arctan2(
        ds.v100 / ds["WS100m"], ds.u100 / ds["WS100m"]))
    ds["WD100m"] = np.mod((270.0 - wdrad_100m), 360.0)
    ds = ds.drop(["u100", "v100", "u10", "v10"])

    if analysis == "spatial":
        preproc_data = ds
    elif analysis == "time_series":
        df = ds["WS10m"][:, 0, 0].to_dataframe().drop(
            columns=["latitude", "longitude"])
        df["WS100m"] = ds["WS100m"][:, 0, 0].values
        df["WD10m"] = ds["WD10m"][:, 0, 0].values
        df["WD100m"] = ds["WD100m"][:, 0, 0].values
        preproc_data = df

    return preproc_data
