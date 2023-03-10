import streamlit as st
import pandas as pd
import numpy as np
import requests

# globals
GEOCODE_API = r"https://geocode.maps.co/search?q="
LAS_VEGAS_LON = -115.148516
LAS_VEGAS_LAT = 36.1672559

# initialization
lat = 28.3824072  # disney world
lon = -81.56170781271818  # disney world
session = requests.Session()


# functions
@st.cache_data
def fetch(url):
    try:
        result = session.get(url)
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

    # dates of trip
    st.caption(
        body="Dates of Visit"
    )
    firstDay = st.date_input(label="First Day in Vegas")
    lastDay = st.date_input(label="Last Day in Vegas")

    # submit button
    submitted = st.form_submit_button("Submit")


# visuals
# --- map of travel
if submitted:
    data = fetch(f"{GEOCODE_API}{address}")
    if data:
        lon = float(data[0]["lon"])
        lat = float(data[0]["lat"])
    else:
        st.error("Error")

# map showing travel path
dots = get_lon_lat_connect_points(
    coord1=[lat, lon],
    coord2=[LAS_VEGAS_LAT, LAS_VEGAS_LON]
)
st.map(dots)
