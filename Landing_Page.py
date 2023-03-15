import streamlit as st


# global settings
st.set_page_config(
   page_title="The Ballow Vegas Guidebook",
   page_icon="♣",
   layout="wide",
   initial_sidebar_state="expanded"
   )

# vegas visual
st.markdown("# Welcome to the :red[Ballow Vegas Guidebook]")
st.image(
    image="./media/vegas_sign.gif",
    caption="Image source: https://gifer.com/en/826I"
   )

# disccussion
st.markdown("""
   #### Thank you so much for visiting this streamlit application!

   Hello, I'm James Michael Ballow. A software engineer and machine learnist
   that likes to do fun projects on the side to learn more software techniques
   and application strategies. I made this application for fun, and I'm not
   accepting any donations or other financial incentives for creating this
   site.

   This application was made as a tool to help plan a trip to Las Vegas.
   This is a sample application using Streamlit that can perhaps be a
   starting point for someone else's project! I had fun making this app
   and I hope to correct/perfect it as time goes on. Feel free to take
   what I have here in this application and make something of your own!

   #### Special Shout Out to Public and Semi-free APIs
   The following APIs helped to make this project happen.

   - [https://geocode.maps.co/] - Provides coordinates (LAT/LON) given any
                                  kind of address.
   - [https://www.thecocktaildb.com/] - Provides information on alcoholic
                                        drinks and provides images of
                                        those drinks.
   - [https://rapidapi.com/weatherapi/api/weatherapi-com/] - Provides a
                     variety of weather-related data, of which I use a
                     3-day forecast of weather in Vegas.

""")

st.sidebar.caption("Made by: :red[James Michael Ballow]")
st.sidebar.markdown("LinkedIn: [james-michael-ballow]"
                    "(https://www.linkedin.com/in/james-michael-ballow)")
