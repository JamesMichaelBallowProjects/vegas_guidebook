import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from datetime import datetime

# globals
GEOCODE_API = r"https://geocode.maps.co/search?q="
WEATHER_API = (r"https://weatherapi-com.p.rapidapi.com"
               r"/forecast.json?q=las+vegas&lang=en&days=3")
LAS_VEGAS_LON = -115.148516
LAS_VEGAS_LAT = 36.1672559

# secrets -> headers
weatherHeaders = {
    "X-RapidAPI-Key": os.environ.get("WEATHER_API_KEY"),
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

# initialization
lat = LAS_VEGAS_LAT + 0.00000001
lon = LAS_VEGAS_LON
session = requests.Session()
date = datetime.now()


# functions
@st.cache_data
def fetch(url, _, headers={}):
    try:
        result = session.get(url, headers=headers)
        return result.json()
    except Exception:
        return {}


def format_address(address):
    address = address.split()
    f_address = ""
    for a in address:
        f_address += f"{a}+"
    return f_address[:-1]


def get_lon_lat_connect_points(coord1, coord2):
    # get slope, intercept
    m = (coord1[1] - coord2[1]) / (coord1[0] - coord2[0])
    b = coord1[1] - m * coord1[0]

    # get independent variable
    xVals = np.linspace(
        start=coord1[0],
        stop=coord2[0],
        endpoint=True,
        num=50
    )

    # get dependent variables
    yVals = m * xVals + b

    # pacakge in dataframe
    return pd.DataFrame(list(zip(xVals, yVals)), columns=['lat', 'lon'])


# --------------------- CODE ---------------------------
# sidebar
with st.sidebar.form("my_form"):
    # address
    st.caption(
        body="Address of Departure"
    )
    city = st.text_input(
        label="City",
        value="Orlando",
        help="Keep blank if not applicable."
    ).replace(" ", "+")
    state = st.text_input(
        label="State",
        value="FL",
        help="Keep blank if not applicable."
    ).replace(" ", "+")
    country = st.text_input(
        label="Country",
        value="USA",
        help="Keep blank if not applicable."
    ).replace(" ", "+")
    address = ""
    for a in [city, state, country]:
        if a != "":
            address += f"{a}+"
    address = address[:-1]
    st.caption(body="---")

    # # dates of trip
    # st.caption(
    #     body="Dates of Visit"
    # )
    # firstDay = st.date_input(label="First Day in Vegas")
    # lastDay = st.date_input(label="Last Day in Vegas")

    # submit button
    submitted = st.form_submit_button("Submit")

# --- caption for author and update
st.sidebar.caption(body="Made by: :red[James Michael Ballow]")
st.sidebar.caption(body="Last Updated: :red[March 2023]")


# visuals
# --- general
st.header("Travel Path and Vegas Weather")
st.markdown(body="---")

# --- fetch data based on travel's address
if submitted:
    data = fetch(
        f"{GEOCODE_API}{address}",
        f"{date.month}-{date.day}-{date.year}",
        headers={}
    )
    if data:
        try:
            lon = float(data[0]["lon"])
            lat = float(data[0]["lat"])
        except Exception:
            lon = LAS_VEGAS_LON
            lat = LAS_VEGAS_LAT
    else:
        st.error("Error")

# --- map showing travel path
dots = get_lon_lat_connect_points(
    coord1=[lat, lon],
    coord2=[LAS_VEGAS_LAT, LAS_VEGAS_LON]
)
st.map(dots)
st.markdown(body="---")

# --- weather
# fetch data
weatherData = fetch(
    WEATHER_API,
    date,
    headers=weatherHeaders
)
if not weatherData:
    st.error(body="Unfortunately, WeatherAPI is not working right now.")
st.header(":red[3 Day Forecast]")

# visualize
weather = []
for forecast in weatherData["forecast"]["forecastday"]:
    weather.append({
        "date": forecast["date"],
        "oatMaxF": forecast["day"]["maxtemp_f"],
        "oatMinF": forecast["day"]["mintemp_f"],
        "oatAvgF": forecast["day"]["avgtemp_f"],
        "probOfRain": forecast["day"]["daily_chance_of_rain"],
        "totalPrecipIn": forecast["day"]["totalprecip_in"],
        "probOfSnow": forecast["day"]["daily_chance_of_snow"],
        "totalSnowCm": forecast["day"]["totalsnow_cm"],
        "conditionText": forecast["day"]["condition"]["text"].title(),
        "conditionIcon": "http:" + forecast["day"]["condition"]["icon"]
    })

col1, col2, col3 = st.columns(3)
for idx, col in enumerate(st.columns(3)):
    with col:
        weatherObj = weather[idx]
        st.header(f"{weatherObj['date']}")
        st.image(
            image=weatherObj["conditionIcon"],
            caption=weatherObj["conditionText"],
            width=124,
        )
        st.markdown(
            f"""
            >:violet[Outdoor Air Temperature]
            - Low - :blue[{weatherObj["oatMinF"]} °F]
            - Avg - :blue[{weatherObj["oatAvgF"]} °F]
            - High - :blue[{weatherObj["oatMaxF"]} °F]

            >:violet[Rain]
            - Probability: :green[{weatherObj["probOfRain"]} %]
            - Amount: :green[{weatherObj["totalPrecipIn"]} in]

            >:violet[Snow]
            - Probability: :green[{weatherObj["probOfSnow"]} %]
            - Amount: :green[{weatherObj["totalSnowCm"]} cm]

            """
        )
