"""TODO: add docstring here - what the module does, how to invoke."""

# Refactoring ideas (EP):
# - separate data aquisition and plotting into two functions
# - make hardcoded constants function arguments
# - write temp *.png files to temporary directory

import pandas as pd
from pandas_datareader import wb

pd.options.display.max_columns = 1000
pd.options.display.max_rows = 1000
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
from sklearn.utils._testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning


@ignore_warnings(category=ConvergenceWarning)
def giffer(variable, name):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
    indicators = [
        variable
    ]  # Gini coefficient, GDP per capita, Employment rate, Education level
    country = ["US", "CN", "JP"]  # United States, China, Japan
    start = "1960-01-01"
    end = "2020-12-31"

    # Download the data from World Bank
    df = wb.download(indicator=indicators, country="all", start=start, end=end)

    # Sort the data by country
    df = df.reset_index().sort_values("country").set_index("country")

    # Pivot the data so that years are in columns and countries are in rows
    df = df.pivot(columns="year")

    # Rename the columns using the indicators and years
    columns = [
        f"{year}_{col}".format(col, year) for year in df.columns for col in indicators
    ]

    # Reset the index to turn countries into a column
    df = df.reset_index()
    df.rename(
        columns={
            variable: name,
            "NY.GDP.PCAP.CD": "GDP per capita",
            "SL.UEM.TOTL.ZS": "Employment rate",
            "SE.PRM.ENRR": "Education level",
            "NY.GDP.TOTL.RT.ZS": "Resources rent",
        },
        inplace=True,
    )

    df.columns = ["{} {}".format(col[0], col[1]) for col in df.columns]

    df.rename(columns={"countryYear": "Country"})
    import country_converter as coco
    import pandas as pd

    # Add a new column for country codes
    df["Country Code"] = coco.convert(names=df["country "], to="ISO3")
    df = df.where(df["Country Code"] != "not found")

    import numpy as np

    df = df.apply(lambda row: row.ffill().bfill(), axis=1)
    cols = list(df.columns)
    cols = [cols[-1]] + cols[:-1]

    df = df[cols]

    import plotly.graph_objs as go
    import plotly.io as pio
    import imageio

    # Set the default renderer to PNG
    pio.renderers.default = "png"

    # Create a list to hold the filenames of the saved PNG files
    png_files = []

    # Loop through the columns of the dataframe
    for i in range(len(df.columns)):
        # Create the choropleth visualization
        map_data = dict(
            type="choropleth",
            locations=df["Country Code"],
            z=df[df.columns[i]],
            text=df["country "],
            zmin=20,
            zmax=60,
        )
        map_layout = dict(title=df.columns[i], geo=dict(showframe=True))
        map_actual = go.Figure(data=[map_data], layout=map_layout)

        # map_data = dict(type='choropleth', locations=dff['Country Code'], z=df[df.columns[i]], text=dff['country '], colorbar={'title': df.columns[i]})
        # map_layout = dict( title='Абсолютное расхождение', geo=dict(showframe=True) )
        # map_actual = go.Figure(data=[map_data], layout=map_layout)

        # Save the visualization as a PNG file
        filename = f"plot_{df.columns[i]}.png"
        png_files.append(filename)
        pio.write_image(map_actual, filename)

    # Set the output filename for the GIF
    gif_filename = "output.gif"

    # Create the GIF using the saved PNG files
    images = []
    for filename in png_files:
        images.append(imageio.imread(filename))

    imageio.mimsave(gif_filename, images, duration=0.2)

    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
    from moviepy.editor import VideoFileClip

    clip = VideoFileClip("output.gif")
    clip = clip.subclip(3)
    clip = clip.subclip(0, clip.duration - 2)
    clip.write_gif("example.gif")


giffer("SI.POV.GINI", "Gini coefficient")
