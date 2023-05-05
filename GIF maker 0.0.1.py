# EP - docstring goes here
# EP - do not name file with semver, it shoudl be gif_maker.py

# EP - run isort to sort the imports 
import pandas as pd
from pandas_datareader import wb
import warnings
import country_converter as coco
import numpy as np
import plotly.graph_objs as go
import plotly.io as pio
import imageio
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
import os
import shutil
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
import imageio
from tqdm import tqdm
from moviepy.video.io.VideoFileClip import VideoFileClip
from sklearn.utils._testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning

# warnings.simplefilter(action='ignore', category=FutureWarning)
"""
    def giffer creates an animated GIF from World Bank data for a specified variable and countries over a specified period of time.
    The function acquires the data from the World Bank, cleans it, and plots it on a world map. The resulting plot is
    saved as a series of PNG images, which are then converted into an animated GIF.

    Parameters: EP - of which function?
    variable (str): The name of the variable to retrieve data for. Example: "Mobile cellular subscriptions (per 100 people)"
    countries (str or list): A string or list of strings containing the names of the countries to retrieve data for. Example: ['US', 'CN', 'JP']
    start_date (str): The start date for the time period to retrieve data for (in YYYY-MM-DD format). Example: "1980-01-01"
    end_date (str): The end date for the time period to retrieve data for (in YYYY-MM-DD format). Example: "1980-01-01"
    duration (float): The duration of the resulting animated GIF, in seconds. Example: 0.5
"""

# EP: not clear variable vs name
def acquire_data(variable, name, countries, start_date, end_date):
    # EP - можно сделать вспомогатлельной функций, котрая этот словарь выдает  
    variables_dict = {
        "GDP per capita (constant 2010 US$)": "NY.GDP.PCAP.KD",
        "GDP growth (annual %)": "NY.GDP.MKTP.KD.ZG",
        "Inflation, consumer prices (annual %)": "FP.CPI.TOTL.ZG",
        "Trade (% of GDP)": "NE.TRD.GNFS.ZS",
        "Foreign direct investment, net inflows (% of GDP)": "BX.KLT.DINV.WD.GD.ZS",
        "Net migration": "SM.POP.NETM",
        "Population, total": "SP.POP.TOTL",
        "Urban population (% of total population)": "SP.URB.TOTL.IN.ZS",
        "Rural population (% of total population)": "SP.RUR.TOTL.ZS",
        "Life expectancy at birth, total (years)": "SP.DYN.LE00.IN",
        "Mortality rate, under-5 (per 1,000 live births)": "SH.DYN.MORT",
        "Prevalence of undernourishment (% of population)": "SN.ITK.DEFC.ZS",
        "CO2 emissions (metric tons per capita)": "EN.ATM.CO2E.PC",
        "Renewable energy consumption (% of total final energy consumption)": "EG.FEC.RNEW.ZS",
        "Electric power consumption (kWh per capita)": "EG.USE.ELEC.KH.PC",
        "Mobile cellular subscriptions (per 100 people)": "IT.CEL.SETS.P2",
        "Internet users (per 100 people)": "IT.NET.USER.P2",
        "Labor force participation rate, total (% of total population ages 15+)": "SL.TLF.TOTL.IN.ZS",
        "Unemployment, total (% of total labor force)": "SL.UEM.TOTL.ZS",
    }

    df = wb.download(
        indicator=variable, country=countries, start=start_date, end=end_date
    )
    df = df.reset_index().sort_values("country").set_index("country")
    df = df.pivot(columns="year")
    columns = [
        f"{year}_{col}".format(col, year) for year in df.columns for col in variable
    ]
    df = df.reset_index()
    df.rename(columns={variable: name}, inplace=True)
    df.columns = ["{} {}".format(col[0], col[1]) for col in df.columns]
    df.rename(columns={"countryYear": "Country"})
    df["Country Code"] = coco.convert(names=df["country "], to="ISO3")
    df = df.where(df["Country Code"] != "not found")
    df = df.apply(lambda row: row.ffill().bfill(), axis=1)
    cols = list(df.columns)
    cols = [cols[-1]] + cols[:-1]
    df = df[cols]
    return df


def plot_data(df, variable_name, duration, output_dir="gifs"):
    # EP: весь этот блок с подготвокой директории тянет на отдельную функцию
    #     если вам эти файлы не очень нужны и удаляются, можно через 
    #     https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryDirectory
    #     создавать и чистить
    # Создаем директорию для сохранения гифок
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # EP: очень опасная функция - не надо так - кто-нибудь вызватл у себя в длиректориии и потер все файлы    
    # Удаляем все предыдущие изображения из директории
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    pio.renderers.default = "png"
    png_files = []

    # numeric_cols = df.select_dtypes(include=np.number)
    numeric_cols = df.select_dtypes(include=[np.number, "object"])
    numeric_cols = numeric_cols.apply(pd.to_numeric, errors="coerce")
    numeric_cols = df.loc[:, numeric_cols.notna().any()]
    # Преобразуем все ячейки в числа, игнорируя ошибки
    values = []
    for col in numeric_cols.columns:
        col_values = pd.to_numeric(numeric_cols[col], errors="coerce").dropna().tolist()
        if col_values:
            values.extend(col_values)
    # вычисляем квантили
    if values:
        q_min = np.quantile(values, 0.05)
        q_max = np.quantile(values, 0.95)
    else:
        q_min = 20
        q_max = 80
    years = range(1960, 2025)
    for year in tqdm(years, desc="Processing years"):
        year_str = str(year)
        col_name = f"{variable_name} {year_str}"
        if col_name not in df.columns:
            continue
        # Создать карту
        map_data = dict(
            type="choropleth",
            locations=df["Country Code"],
            z=df[col_name],
            text=df["country "],
            zmin=q_min,
            zmax=q_max,
        )

        map_layout = dict(title=col_name, geo=dict(showframe=True))
        map_actual = go.Figure(data=[map_data], layout=map_layout)
        # EP: если смотерть строго, то операции с данными и запись в файл
        #     они на разном уровне абстракции работают одна функция по идее
        #     начала работать с данными - выдала данные, другая взяла 
        #     - выдала картинку, третья, например, записала картинку в файл 
        filename = f"{col_name}.png"
        filepath = os.path.join(output_dir, filename)
        png_files.append(filepath)
        pio.write_image(map_actual, filepath)
    gif_filename = os.path.join(output_dir, f"{variable_name}.gif")
    with imageio.get_writer(gif_filename, mode="I", duration=duration) as writer:
        for filename in png_files:
            image = imageio.imread(filename)
            writer.append_data(image)
    # Remove PNG files
    for filename in png_files:
        os.remove(filename)
    # Convert the GIF animation to another GIF file using moviepy
    clip = VideoFileClip(gif_filename)
    clip_duration = clip.duration
    if clip_duration < duration:
        raise ValueError(
            "Duration of the clip is less than the duration of the animation"
        )
    start_time = duration
    end_time = clip_duration - duration
    subclip = clip.subclip(start_time, end_time)
    subclip.write_gif(os.path.join(output_dir, f"{variable_name}_final.gif"), loop=True)


def giffer(
    variable_name,
    duration=0.1,
    countries="all",
    start_date="1960-01-01",
    end_date="2022-12-31",
):
    # EP - variables_dict откуда сюда прилетает? Это какая-то глобальная переменная? 
    variable = variables_dict[variable_name]
    df = acquire_data(variable, variable_name, countries, start_date, end_date)
    plot_data(df, variable_name, duration)


giffer(
    "Mobile cellular subscriptions (per 100 people)",
    duration=0.5,
    start_date="1980-01-01",
)
