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

   This application was made to help you plan your trip to Las Vegas.
   There are many things that are still in the works in this application,
   and you can expect that there will be some modifications and additions
   to the application as I find the time to do them. I'm hoping to have
   a very good tool that you find both entertaining and informative.

   #### Special Shout Out to Public and Semi-free APIs
   The following APIs helped to make this project happen.

   - [https://geocode.maps.co/] - Provides coordinates (LAT/LON) given any
                                  kind of address.
   - [https://www.thecocktaildb.com/] - Provides information on alcoholic
                                        drinks and provides images of
                                        those drinks.

""")

st.sidebar.caption("Made by: :red[James Michael Ballow]")
st.sidebar.markdown("LinkedIn: [james-michael-ballow]"
                    "(https://www.linkedin.com/in/james-michael-ballow)")
